# -*- coding: utf-8 -*-
import os
from . import test_path
from example.graph import recognition


def test_recognition():
    """ 图片（滑动块位置）辩识测试（允许左右各5px的偏差） """
    result = recognition(os.path.join(test_path, '6.jpg'))
    centre_x = 465  # 滑块中心点基准值
    assert result >= centre_x - 5
    assert result <= centre_x + 5

    result = recognition(os.path.join(test_path, '7.jpg'))
    centre_x = 271  # 滑块中心点基准值
    assert result >= centre_x - 5
    assert result <= centre_x + 5

