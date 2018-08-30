# -*- coding: utf-8 -*-
import os
import uuid
import requests

SERVICE_URL = 'http://172.20.10.6:5000/graph/recognition'   # run command: python3 service.py
SPLASH_URL = 'http://172.20.10.8:8050/execute'
# TARGET_URL = 'http://172.20.10.6:7000/outmoded_browser'
TARGET_URL = 'https://passport.hupu.com/pc/login?project=www&from=pc'

with open(os.path.realpath(os.path.join(__file__, '..', 'login.lua')), 'r') as lua_file:
    login_lua = lua_file.read()

result = requests.post(SPLASH_URL, json={
    # 'js_source': '',
    'lua_source': login_lua,
    # lua args ----
    'url': TARGET_URL,
    'api': SERVICE_URL,
    'boundary': uuid.uuid4().hex,   # post（multipart/form-data）的 boundary 值
})

print(result.text)
