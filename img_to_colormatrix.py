from PIL import Image  # or Keras
from numpy import asarray


def img_to_colormatrix(image_name):
    # load the image
    image = Image.open(image_name)
    # convert image to numpy array
    data = asarray(image)
    print(type(data))
    # summarize shape
    print(data.shape)
    return data