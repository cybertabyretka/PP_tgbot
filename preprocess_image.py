from PIL import Image


def preprocess_image(image):
    image = Image.fromarray(image).convert("RGB")
    image = image.resize((64, 64))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array
