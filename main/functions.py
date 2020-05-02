from typing import List
from PIL import Image
import numpy as np

class Functions:

    def __init__(self):
        pass

    def get_sqaure(self, x, y, w, h):
        if h > w:
            diff1 = max((h - w) // 2, 0)
            nx = max(x - diff1, 0)
            nxw = (h)

            return nx, y, nxw, h
        else:
            diff1 = max((w - h) // 2, 0)
            ny = max(y - diff1, 0)
            nyh = (w)

            return x, ny, w, nyh

    def get_face(self, img: Image, size: int, faces_rects, interpolation=Image.ANTIALIAS) -> Image:
        x, y, width, height = faces_rects[0]['box']
        x, y, width, height = self.get_sqaure(x, y, width, height)
        img = img.crop((x, y, width + x, height + y))
        img = img.resize((size, size), interpolation)
        return img

    def down_size_image(self, img: Image, size, interpolation=Image.ANTIALIAS) -> Image:
        w, h = img.size
        # down size the image if too big for detecting
        size_ratio = max(w, h) / size
        if size_ratio > 1:
            img = img.resize((int(w // size_ratio), int(h // size_ratio)), interpolation)

        return img

    def to_np_image(self, img: Image) -> np.array:
        np_img = np.array(img)
        # for greyscale
        if len(np_img.shape) == 2:
            return np.stack((np_img,) * 3, axis=-1)
        # remove alpha
        return np_img[:, :, :3]

    def format_predictions(self, predictions, labels) :
        attributes = [e[1] for e in zip(predictions, labels) if e[0] > 0.1]
        return attributes

    def find_slug(self, slugs: List[str], slug: str, kwargs) -> bool:
        # check if slug exist
        if slug in kwargs:
            # check if slug exist in table
            if kwargs[slug] in slugs:
                return True
        return False



