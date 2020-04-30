from PIL import Image
import numpy as np


def get_sqaure(x, y, w, h):
    if h > w:
        diff1 = max((h - w) // 2, 0)
        nx = max(x - diff1, 0)
        nxw = (h )

        return nx, y, nxw, h
    else:
        diff1 = max((w - h) // 2, 0)
        ny = max(y - diff1, 0)
        nyh = (w)

        return x, ny, w, nyh


def get_face(img: Image, size: int, faces_rects):
    x, y, width, height = faces_rects[0]['box']
    x, y, width, height = get_sqaure(x, y, width, height)
    img = img.crop((x, y, width + x, height + y))
    img = img.resize((size, size), Image.ANTIALIAS)
    return img


def down_size_image(img: Image, size, interpolation=Image.ANTIALIAS):
    w, h = img.size
    # down size the image if too big for detecting
    while max(w, h) > size:
        img = img.resize((w // 2, h // 2), interpolation)
        w, h = img.size

    return img


def to_np_image(img: Image) -> np.array:
    np_img = np.array(img)

    # for greyscale
    if len(np_img.shape) == 2:
        return np.stack((np_img,)*3, axis=-1)

    #remove alpha
    return np_img[:, :, :3]


def format_predictions(predictions, labels):
    attributes = [e[1] for e in zip(predictions, labels) if e[0] > 0.1]
    return attributes


