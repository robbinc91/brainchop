import json
import os
#from keras.models import load_model
#from keras_contrib.layers import InstanceNormalization
#from backend.dice import calc_aver_dice_loss, soft_dice_loss, soft_dice_score


custom_items_mapper = {
    'soft_dice_score': None,# soft_dice_score,
    'soft_dice_loss': None,# soft_dice_loss,
    'InstanceNormalization': None,# InstanceNormalization,
    'calc_aver_dice_loss': None#calc_aver_dice_loss
}


class Predictor():
    def __init__(self, base_path='.\models'):
        self.base_path = base_path
        self.models = []
        self.model_dirs = []
        self.loaded_model = -1
        self.model = None
        self.get_available_models(self.base_path)

    def empty(self):
        self.models = []
        self.model_dirs = []
        self.loaded_model = -1
        self.model = None

    def get_available_models(self, path):
        self.empty()
        for item in os.listdir(path):
            _item = os.path.join(path, item)
            if os.path.isdir(_item):
                
                meta = os.path.join(_item, 'meta.json')
                if os.path.exists(meta):
                    metadata = json.load(open(meta))
                    self.models.append(metadata)
                    self.model_dirs.append(_item)

        return self.models

    def load_model(self, index):
        if index >= len(self.models):
            return None
        if index != self.loaded_model:

            custom_objects = {
                item: custom_items_mapper[item] for item in self.models[index]['custom_items']
            }
            model = load_model(os.path.join(
                self.model_dirs[index], 'model.h5'), custom_objects=custom_objects)

            self.model = model
            self.loaded_model = index

        return self.model

    def predict(self, data):
        if self.loaded_model != -1:
            logits = self.model.predict(data[None, None, ...])
            logits = logits.squeeze()

            return logits

        return None
