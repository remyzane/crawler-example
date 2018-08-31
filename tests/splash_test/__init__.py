# -*- coding: utf-8 -*-
import os

from tests import test_dir
from example.utility import splash_get_lua_source


def test_get_lua_source():
    result = splash_get_lua_source('source.lua', 'source.js', folder=__path__[0])
    with open(os.path.join(test_dir, 'splash_test', 'target.lua'), 'r') as target_file:
        target = target_file.read()
    assert result == target
