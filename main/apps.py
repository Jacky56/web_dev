from django.apps import AppConfig
from keras.models import load_model
from mtcnn import MTCNN
from django.conf import settings
class MainConfig(AppConfig):
    name = 'main'

    FACE_DETECTOR = MTCNN()
    model_v1 = "Res_267k_64_label_25.h5"
    #MODEL = load_model("{}/main/static/main/nn/face/{}".format(settings.BASE_DIR, model_v1))
    MODEL = load_model("{}/main/nn/face/{}".format(settings.STATIC_ROOT, model_v1))

    # label size = 25
    LABELS = ['Arched Eyebrows', 'Attractive', 'Bags Under Eyes', 'Bald',
              'Bangs', 'Big Lips', 'Big Nose', 'Bushy Eyebrows', 'Chubby',
              'Double Chin', 'Gray Hair', 'Heavy Makeup', 'High Cheekbones',
              'Male', 'Narrow Eyes', 'Oval Face', 'Pale Skin', 'Pointy Nose',
              'Receding Hairline', 'Rosy Cheeks', 'Smiling', 'Straight Hair',
              'Wavy Hair', 'Wearing Lipstick', 'Young']
