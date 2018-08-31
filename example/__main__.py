# -*- coding: utf-8 -*-
import uuid
import requests

import example
from example import SPLASH_URL, SERVICE_URL, LOGIN_URL
from example.utility import splash_get_lua_source


def login():
    login_lua = splash_get_lua_source('login.lua', 'login.js', example.__path__[0])
    result = requests.post(SPLASH_URL, json={
        'lua_source': login_lua,
        # lua args ----
        'url': LOGIN_URL,
        'api': SERVICE_URL,
        'load_time': 4,                 # 加载时间
        'boundary': uuid.uuid4().hex,   # post（multipart/form-data）的 boundary 值
    })

    print('aaaa', result.text)


login()
