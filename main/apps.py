from django.apps import AppConfig
from keras.models import load_model
import cv2

class MainConfig(AppConfig):
    name = 'main'
    v1 = "haarcascade_profileface.xml"
    v2 = "haarcascade_frontalface_default.xml"
    v3 = "haarcascade_frontalface_alt.xml"
    FACE_DETECTOR = cv2.CascadeClassifier("main/static/main/nn/face/{}".format(v1))

    model_v1 = "discriminator_2x2_dense_label_25.h5"
    MODEL = load_model("main/static/main/nn/face/{}".format(model_v1))

    LABELS = ['Arched_Eyebrows', 'Attractive', 'Bags_Under_Eyes', 'Bald',
              'Bangs', 'Big_Lips', 'Big_Nose', 'Bushy_Eyebrows', 'Chubby',
              'Double_Chin', 'Gray_Hair', 'Heavy_Makeup', 'High_Cheekbones',
              'Male', 'Narrow_Eyes', 'Oval_Face', 'Pale_Skin', 'Pointy_Nose',
              'Receding_Hairline', 'Rosy_Cheeks', 'Smiling', 'Straight_Hair',
              'Wavy_Hair', 'Wearing_Lipstick', 'Young']