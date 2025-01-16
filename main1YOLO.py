import asyncio
import os
import cv2
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType, FSInputFile
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from results_handler1YOLO import handle_results
from ultralytics import YOLO
from aiogram.types import BotCommand

from buttons_and_keyboards import MMPI_keyboard, MBTI_keyboard
from preprocess_image import preprocess_image


FACES_MAX_COUNT = 20

API_TOKEN = ""

MODEL_PATH = "models/3/best.pt"

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

model = YOLO(MODEL_PATH)

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.callback_query()
async def handle_callback(callback_query):
    action = callback_query.data
    if action == 'entp':
        await callback_query.message.answer('Полемисты – это любопытные и гибкие мыслители, которые не могут противостоять интеллектуальным вызовам.\n<a href="https://www.16personalities.com/ru/lichnost-entp">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'isfp':
        await callback_query.message.answer('Артисты – это гибкие и обаятельные люди, всегда готовые исследовать и испытать что-то новое.\n<a href="https://www.16personalities.com/ru/lichnost-isfp">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'esfj':
        await callback_query.message.answer('Консулы – это очень заботливые, социальные, думающие об обществе люди, которые всегда готовы помочь.\n<a href="https://www.16personalities.com/ru/lichnost-esfj">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'intj':
        await callback_query.message.answer('Стратеги – это творческие и стратегические мыслители, у которых на все есть план.\n<a href="https://www.16personalities.com/ru/lichnost-intj">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'enfj':
        await callback_query.message.answer('Тренеры – это вдохновляющие оптимисты, готовые сразу действовать, чтобы сделать то, что считают правильным.\n<a href="https://www.16personalities.com/ru/lichnost-enfj">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'istj':
        await callback_query.message.answer('Администраторы – это практичные и опирающиеся на факты личности, в надежности которых сложно усомниться.\n<a href="https://www.16personalities.com/ru/lichnost-istj">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'infp':
        await callback_query.message.answer('Посредники – это поэтичные, добрые и альтруистичные люди, всегда готовые помочь в хорошем деле.\n<a href="https://www.16personalities.com/ru/lichnost-infp">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'estp':
        await callback_query.message.answer('Дельцы – это сообразительные, энергичные и очень проницательные люди, которым действительно нравится жить на грани.\n<a href="https://www.16personalities.com/ru/lichnost-estp">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'intp':
        await callback_query.message.answer('Ученые – это изобретатели-новаторы с неутолимой жаждой знаний.\n<a href="https://www.16personalities.com/ru/lichnost-intp">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'esfp':
        await callback_query.message.answer('Развлекатели – это спонтанные, энергичные энтузиасты, рядом с которыми жизнь никогда не бывает скучной.\n<a href="https://www.16personalities.com/ru/lichnost-esfp">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'entj':
        await callback_query.message.answer('Командиры – это смелые люди с хорошим воображением и силой воли, они всегда найдут путь или проложат его сами.\n<a href="https://www.16personalities.com/ru/lichnost-entj">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'isfj':
        await callback_query.message.answer('Защитники – это очень преданные и заботливые защитники, всегда готовые оберегать своих близких.\n<a href="https://www.16personalities.com/ru/lichnost-isfj">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'estj':
        await callback_query.message.answer('Менеджеры – это отличные организаторы, знающие толк в управлении вещами или людьми.\n<a href="https://www.16personalities.com/ru/lichnost-estj">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'infj':
        await callback_query.message.answer('Активисты – это тихие мечтатели, часто являющиеся вдохновляющими и неутомимыми идеалистами.\n<a href="https://www.16personalities.com/ru/lichnost-infj">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'enfp':
        await callback_query.message.answer('Борцы – это энтузиасты, креативные и социальные люди, которые всегда найдут причину, чтобы улыбнуться.\n<a href="https://www.16personalities.com/ru/lichnost-enfp">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'istp':
        await callback_query.message.answer('Виртуозы – это новаторы и практичные экспериментаторы, мастера на все руки.\n<a href="https://www.16personalities.com/ru/lichnost-istp">Источник</a>', parse_mode='HTML', reply_markup=MBTI_keyboard)
    elif action == 'sh':
        await callback_query.message.answer('У таких личностей идет расщепление между своим внутренним миром и окружающим. Также людям свойственно чувство отстраненности как от какой-то части себя, так и от внешнего мира.\n<a href="https://stakanchik.media/article/8-tipov-xaraktera-osobennosti-vospriyatiya-i-obshheniya-s-kazhdym-tipom">Источник</a>', parse_mode='HTML', reply_markup=MMPI_keyboard)
    elif action == 'pa':
        await callback_query.message.answer('Такие личности часто видят угрозу в окружающем мире, они склонны к тотальному недоверию, подозрительности, повышенной тревожности и чувствительности. Им часто кажется, что их все предают, бросают, используют, поэтому они боятся открываться другим людям.\n<a href="https://stakanchik.media/article/8-tipov-xaraktera-osobennosti-vospriyatiya-i-obshheniya-s-kazhdym-tipom">Источник</a>', parse_mode='HTML', reply_markup=MMPI_keyboard)
    elif action == 'na':
        await callback_query.message.answer('Это те люди, которые поддерживают свою самооценку через одобрение окружающих. У них преувеличенное чувство собственного достоинства, они озабочены лишь собой, не замечая чувств других людей.\n<a href="https://stakanchik.media/article/8-tipov-xaraktera-osobennosti-vospriyatiya-i-obshheniya-s-kazhdym-tipom">Источник</a>', parse_mode='HTML', reply_markup=MMPI_keyboard)
    elif action == 'ps':
        await callback_query.message.answer('Люди с таким типом характера не способны испытывать к кому-то настоящую привязанность. Они манипулируют и используют других для достижения своих целей, не испытывая при этом чувства вины или стыда.\n<a href="https://stakanchik.media/article/8-tipov-xaraktera-osobennosti-vospriyatiya-i-obshheniya-s-kazhdym-tipom">Источник</a>', parse_mode='HTML', reply_markup=MMPI_keyboard)
    elif action == 'ko':
        await callback_query.message.answer('Подобные люди могут иметь навязчивые мысли или действия. Характеризуются навязчивостью, но одновременно изоляцией, если видят негатив в свой адрес.\n<a href="https://stakanchik.media/article/8-tipov-xaraktera-osobennosti-vospriyatiya-i-obshheniya-s-kazhdym-tipom">Источник</a>', parse_mode='HTML', reply_markup=MMPI_keyboard)
    elif action == 'is':
        await callback_query.message.answer('Это гиперчувствительные и тревожные личности, которые гиперболизируют любую свою эмоцию. Другим людям они могут казаться поверхностными или наигранными, но на самом деле личность действительно может страдать от переизбытка эмоциональности.\n<a href="https://stakanchik.media/article/8-tipov-xaraktera-osobennosti-vospriyatiya-i-obshheniya-s-kazhdym-tipom">Источник</a>', parse_mode='HTML', reply_markup=MMPI_keyboard)
    elif action == 'de':
        await callback_query.message.answer('В депрессивном состоянии свою злость люди направляют не на другого, а на себя. Они очень долго и болезненно переживают собственные ошибки или недостатки, отрицая свою хорошие поступки или качества.\n<a href="https://stakanchik.media/article/8-tipov-xaraktera-osobennosti-vospriyatiya-i-obshheniya-s-kazhdym-tipom">Источник</a>', parse_mode='HTML', reply_markup=MMPI_keyboard)
    elif action == 'ma':
        await callback_query.message.answer('Такие люди любят страдать, жаловаться на жизнь, склонны к самопожертвованию и обесцениванию. За этим скрывается подсознательное желание мучить не только себя, но и других своими страданиями, потому что они редко переживают свои чувства тихо в одиночестве, стремясь поделиться с миром своей болью.\n<a href="https://stakanchik.media/article/8-tipov-xaraktera-osobennosti-vospriyatiya-i-obshheniya-s-kazhdym-tipom">Источник</a>', parse_mode='HTML', reply_markup=MMPI_keyboard)
    await callback_query.answer()


async def set_commands():
    commands = [
        BotCommand(command="/personality", description="Показать типы личности"),
        BotCommand(command="/character", description="Показать типы характера"),
        BotCommand(command="/info", description="Показать ограничения отправки изображений")
    ]
    await bot.set_my_commands(commands)


async def send_reply_on_photo(message: Message, file, answer):
    str_answer = ''
    for result in answer:
        probability = str(round(float(result[4]), 4)).replace('.', ',')
        str_answer += f'<a href="{result[2]}">{result[0]}</a> <a href="{result[3]}">{result[1]}</a>, Вероятность: {probability}\n'
    await message.answer_photo(file, str_answer, parse_mode="HTML")


@dp.message(F.content_type == ContentType.DOCUMENT)
async def handle_photo_doc(message: Message):
    await message.answer("Отправляйте не файлом (отправляйте со сжатием)")


@dp.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message):
    processing_message = await message.answer("Обработка...")
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = f"downloads/{photo.file_id}.jpg"

    try:
        await bot.download_file(file_info.file_path, destination=file_path)

        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        await bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)

        if len(faces) == 0:
            await message.answer("Лица не обнаружены на изображении.")
        else:
            for i, (x, y, w, h) in enumerate(faces):

                if i > FACES_MAX_COUNT:
                    break

                face = image[y:y + h, x:x + w]

                prediction = model(face)
                prediction = [(prediction[0].probs.top5[i], prediction[0].probs.top5conf[i]) for i in range(len(prediction[0].probs.top5))]
                answer = handle_results(prediction)

                face_path = f"downloads/face_{photo.file_id}_{i}.jpg"
                cv2.imwrite(face_path, face)

                input_file = FSInputFile(face_path)
                await send_reply_on_photo(message, input_file, answer)

                os.remove(face_path)

        os.remove(file_path)
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        await message.answer(f"Ошибка на сервере при обработке изображения, попробуйте позже")
        if os.path.exists(file_path):
            os.remove(file_path)


@dp.message(F.text == "/start")
async def send_welcome(message: Message):
    await message.answer('Привет! Отправь мне фото лица человека, и я определю типы личности и характера этого человека с помощью нейросети. (Максимум лиц на фото - 20) (Максимальное количество фото в одном сообщении - 1) <a href="https://www.16personalities.com/ru/tipy-lichnosti">Типы личности</a>, <a href="https://stakanchik.media/article/8-tipov-xaraktera-osobennosti-vospriyatiya-i-obshheniya-s-kazhdym-tipom">Типы характера</a>', parse_mode='HTML')


@dp.message(F.text == "/personality")
async def send_MBTI_keyboard(message: Message):
    await message.answer('Выберите тип личности', reply_markup=MBTI_keyboard)


@dp.message(F.text == "/character")
async def send_MMPI_keyboard(message: Message):
    await message.answer('Выберите тип характера', reply_markup=MMPI_keyboard)


@dp.message(F.text == "/info")
async def send_info(message: Message):
    await message.answer('Количество фото в одном сообщении - 1\nКоличество возвращаемых лиц - 20\nФото отправлять со сжатием')


async def main():
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    await set_commands()

    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
