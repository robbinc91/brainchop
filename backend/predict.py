import nibabel
from losses import *
from keras.models import load_model
from keras_contrib.layers import InstanceNormalization


def model_loading(model_path):
    try:
        model = load_model(model_load, custom_objects={
            'dice_coefficient': dice_coefficient, 'dice_loss': dice_loss})
    except:
        model = load_model(lesions_model, custom_objects={
                        'dice_coefficient': dice_coefficient, 'dice_loss': dice_loss, 'InstanceNormalization': InstanceNormalization})

    return model


def predict(model_path, image):
    model = model_loading(model_path)
    output = model.predict(image[None, None, ...])
    return output.squeeze()
