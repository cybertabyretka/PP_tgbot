import asyncio
import os
import cv2
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType, FSInputFile
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from results_handler2YOLO import handle_results
from ultralytics import YOLO


FACES_MAX_COUNT = 20

API_TOKEN = ""

MMPI_MODEL_PATH = "models/2/mmpi.pt"
MBTI_MODEL_PATH = "models/2/mbti.pt"

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

mbti_model = YOLO(MBTI_MODEL_PATH)
mmpi_model = YOLO(MMPI_MODEL_PATH)
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(F.content_type == ContentType.DOCUMENT)
async def handle_photo_doc(message: Message):
    await message.answer("Отправяйте не файлом")


async def send_reply_on_photo(message: Message, file, answer):
    str_answer = ''
    for result in answer:
        probability = str(round(float(result[4]), 4)).replace('.', ',')
        str_answer += f'<a href="{result[2]}">{result[0]}</a> <a href="{result[3]}">{result[1]}</a>, Вероятность: {probability}\n'
    await message.answer_photo(file, str_answer, parse_mode="HTML")


def preprocess_image(image):
    image = Image.fromarray(image).convert("RGB")
    image = image.resize((64, 64))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array


@dp.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message):
    await message.answer("Обработка...")
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = f"downloads/{photo.file_id}.jpg"

    try:
        await bot.download_file(file_info.file_path, destination=file_path)

        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            await message.answer("Лица не обнаружены на изображении.")
        else:
            for i, (x, y, w, h) in enumerate(faces):

                if i > FACES_MAX_COUNT:
                    break

                face = image[y:y + h, x:x + w]

                mbti_prediction = mbti_model(face)
                mmpi_prediction = mmpi_model(face)
                prediction = [(
                    mbti_prediction[0].probs.top5[i] + 1,
                    mmpi_prediction[0].probs.top5[i] + 1,
                    mbti_prediction[0].probs.top5conf[i],
                    mmpi_prediction[0].probs.top5conf[i]) for i in range(len(mbti_prediction[0].probs.top5))]
                predictions = []
                for i in range(5):
                    for j in range(5):
                        predictions.append((prediction[i][0], prediction[j][1], prediction[i][2] * prediction[j][3]))
                predictions.sort(key=lambda x: x[2], reverse=True)
                answer = handle_results(predictions[:5])

                face_path = f"downloads/face_{photo.file_id}_{i}.jpg"
                cv2.imwrite(face_path, face)

                input_file = FSInputFile(face_path)
                await send_reply_on_photo(message, input_file, answer)

                os.remove(face_path)

        os.remove(file_path)
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        await message.answer(f"Ошибка при обработке изображения")
        if os.path.exists(file_path):
            os.remove(file_path)


@dp.message(F.text == "/start")
async def send_welcome(message: Message):
    await message.answer("Привет! Отправь мне фото, и я обработаю его с помощью нейросети. (Максимум лиц на фото - 20)")


async def main():
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
