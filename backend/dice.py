# -*- coding: utf-8 -*-

from functools import partial
from keras import backend as K



def _calc_aver_dice(image1, image2, axis=(-3, -2, -1), eps=0.001):
    """Calculate average Dice across channels
    
    Args:
        image1, image2 (Tensor): The images to calculate Dice
        axis (tuple of int or int): The axes that the function sums across
        eps (float): Small number to prevent division by zero

    Returns:
        dice (float): The average Dice

    """
    intersection = K.sum(image1 * image2, axis=axis)
    sum1 = K.sum(image1, axis=axis)
    sum2 = K.sum(image2, axis=axis)
    dices = 2 * (intersection + eps) / (sum1 + sum2 + eps)
    dice = K.mean(dices)
    return dice


def calc_aver_dice_loss(y_true, y_pred, **kwargs):
    return 1 - _calc_aver_dice(y_true, y_pred, **kwargs)


def soft_dice_score(image1, image2, axis=(-3, -2, -1), eps=0.001):
    intersection = K.sum(K.abs(image1 * image2), axis=axis)
    dices = (2. * intersection + eps) / (K.sum(K.square(image1),
                                               axis) + K.sum(K.square(image2), axis) + eps)
    dice = K.mean(dices)
    return dice

def soft_dice_loss(y_true, y_pred):
    return 1-soft_dice_score(y_true, y_pred)