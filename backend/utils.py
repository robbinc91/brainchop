import numpy as np
import nibabel as nib
import cv2 as cv
import SimpleITK as sitk
import numpy as np
from skimage.measure import label
from scipy import ndimage
from skimage.morphology import black_tophat, skeletonize, convex_hull_image 
from skimage import morphology
from skimage.segmentation import clear_border

try:
    from deepbrain import Extractor
except:
    print('deepbrain library could not be loaded')


def normalize(data):
    return (data - data.mean()) / data.std()


def convex_hull_3d(data, axe=2):

    if axe == 2:
        for slice_index in range(data.shape[2]):
            data[:, :, slice_index] = convex_hull_image(
                data[:, :, slice_index])

    if axe == 1:
        for slice_index in range(data.shape[1]):
            data[:, slice_index, :] = convex_hull_image(
                data[:, slice_index, :])

    if axe == 0:
        for slice_index in range(data.shape[0]):
            data[slice_index, :, :] = convex_hull_image(
                data[slice_index, :, :])

    return data


def get_cdf_hist(image_input):
    """
    Method to compute histogram and cumulative distribution function
    :param image_input: input image
    :return: cdf
    """
    hist, bins = np.histogram(image_input.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    return cdf_normalized


def fill_holes_single_slice(data):
    print(data.shape)
    for slice_index in range(data.shape[0]):
        data[slice_index, :, :] = np.round(scipy.ndimage.binary_fill_holes(
            data[slice_index, :, :])).astype(np.uint8)
    return data


def remove_small_objects(data):
    data = morphology.remove_small_objects(data.astype(
        bool), min_size=20, connectivity=1).astype(np.uint8)

    for slice_index in range(data.shape[2]):
        data[:, :, slice_index] = morphology.remove_small_objects(
            data[:, :, slice_index], min_size=2, connectivity=1)

    for slice_index in range(data.shape[1]):
        data[:, slice_index, :] = morphology.remove_small_objects(
            data[:, slice_index, :], min_size=2, connectivity=1)

    for slice_index in range(data.shape[0]):
        data[slice_index, :, :] = morphology.remove_small_objects(
            data[slice_index, :, :], min_size=2, connectivity=1)

    return data.astype(np.uint8)


def histeq(data):
    for slice_index in range(data.shape[2]):
        data[:, :, slice_index] = cv.equalizeHist(data[:, :, slice_index])
    return data


def to_uint8(data):
    data = data.astype(np.float)
    data[data < 0] = 0
    return ((data - data.min()) * 255.0 / data.max()).astype(np.uint8)


def conform_image(path, shape, pixel_sp):
    return nib.processing.conform(nib.load(path), shape, pixel_sp)


def crop3d(image, bbox):
    roi = np.asarray(image.dataobj[bbox[0], bbox[1], bbox[2]])
    return roi


def uncrop3d(image, source_shape, source_bbox):
    uncropped = np.zeros(source_shape, dtype=image.dtype)
    uncropped[tuple(source_bbox)] = image[:, :, :]
    return uncropped


def load_stages_from_json(json_path=None):
    # TODO: read stages from specified json file and return a list of stages
    pass


def load_model_names(path=None):
    # TODO: load model names and return a list
    pass


def to_uint8():
    pass


def onehot(label_image, num_labels=None):
    """Performs one-hot encoding.

    Args:
        label_image (numpy.ndarray): The label image to convert to be encoded.
        num_labels (int): The total number of labels. If ``None``, it will be
            calcualted as the number of unique values of input ``label_image``.

    Returns:
        numpy.ndarray: The encoded label image. The first dimension is channel.

    """
    if num_labels is None:
        num_labels = len(np.unique(label_image)) - 1  # without background 0
    result = np.zeros((num_labels + 1, label_image.size), dtype=bool)
    result[label_image.flatten(), np.arange(label_image.size)] = 1
    result = result.reshape(-1, *label_image.shape)
    return result


def get_data(path):
    return nib.load(path).get_data()


def get_data_with_skull_scraping(path, PROB=0.5):
    arr = nib.load(path).get_data()
    ext = Extractor()
    prob = ext.run(arr)
    mask = prob > PROB
    arr = arr * mask
    return arr


def save_image(original_image_path, data, output_path):
    _img = nib.load(original_image_path)
    output_img = nib.Nifti1Image(
        data, affine=_img.affine, header=_img.header)
    nib.save(output_img, output_path)


def largest_connected_component(data):
    label_im, nb_labels = ndimage.label(data)
    sizes = ndimage.sum(data, label_im, range(nb_labels + 1))
    mask = sizes == max(sizes)
    lcc = mask[label_im]
    return lcc
