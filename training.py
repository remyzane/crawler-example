# -*- coding: utf-8 -*-
""" 图像样本训练（执行一次即可） """
import dlib
from example import samples_xml, samples_svm


def training():
    """ 训练样本 """
    print('training samples ...')
    options = dlib.simple_object_detector_training_options()
    # 要识别的图形是否左右对称
    options.add_left_right_image_flips = True
    # C越大表示更好地去拟合训练集，当然也有可能造成过拟合。通过尝试不同C在测试集上的效果得到最佳值
    options.C = 5
    # 训练数据时开启的线程数
    options.num_threads = 2
    # 是否输出详细日志
    options.be_verbose = False

    dlib.train_simple_object_detector(samples_xml, samples_svm, options)
    print('finished.')


training()
