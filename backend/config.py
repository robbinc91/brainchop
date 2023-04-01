from enum import Enum
from predict import predict
from utils import *
import json


class StageNames(Enum):
    IMAGE_LOADING = 'image_loading'
    PREPROCESSING = 'preprocessing'
    N4_BIAS_CORRECTION = 'n4_bias_correction'
    MNI_NORMALIZATION = 'mni_normalization'
    HISTOGRAM_EQUALIZATION = 'histogram_equalization'
    UINT8_DATA_CALCULATION = 'uint8_data_calculation'
    CROPPING = 'cropping'
    MODEL_LOADING = 'model_loading'
    PREDICTING = 'predicting'
    POSTPROCESSING = 'postprocessing'
    LARGEST_CONNECTED_COMPONENT_EXTRACTION = 'largest_connected_component_extraction'
    UNCROPPING = 'uncropping'


class Stage:
    def __init__(self, **data):
        for key in data:
            setattr(self, key, data[key])

        if not hasattr(self, 'output_image'):
            # TODO: allow to do this automatically
            pass


    def __str__(self):
        return self.dict()

    def check_save_processed_image(self, processed):
        # TODO: check this stuff
        if hasattr(self, 'output_path'):
            self.save(processed, self.output_path)

    def run(self, **data):

        if self.name == StageNames.UINT8_DATA_CALCULATION:
            image = get_data(self.input_image)
            processed = to_uint8(image)
            self.save_image(processed)
            return processed
            
        if self.name == StageNames.HISTOGRAM_EQUALIZATION:
            # TODO: define histeq variants
            pass

        if self.name == StageNames.PREDICTING:
            image = get_data(self.input_image)
            processed = predict(self.model_path, image)
            self.save_image(processed)
            return processed

    def save_image(self, data):
        save_image(self.input_image, data, self.output_image)


def build_stage_list(filename, use_partials=True):
    stages = []
    with json.loads(filename) as json_file:
        for item in json_file:
            stages.append(Stage(**item))

    return stages

def process_stages(stage_list):
    for stage in stage_list:
        yield stage.name
        stage.run()
    
    yield 'finished'



stages = [
    {
        'name': StageNames.PREDICTING,
        'input_image': './sample/a34-histeq.nii.nii.gz',
        'model_path': './sample/binpmodel-cerebellum_lesions_augm-120.h5',
        'output_path': './sample/output.nii.gz'
    }
]


if __name__ == '__main__':

    stagedata = {
        'name': 'configstage',
        'somevalue': 10
    }
    stage = Stage(**stagedata)
    print(stagedata)
    print(stage.name)
    stage.run()
