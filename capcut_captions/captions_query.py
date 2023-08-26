import requests

headers = {
    'Host': 'editor-api-sg.capcut.com',
    'content-type': 'application/json',
    'appvr': '2.4.0',
    'device-time': '1692810523',
    'lan': 'en',
    'loc': 'VN',
    'pf': '4',
    'sign': '456f6494cf21597b859e28c1b4637a3f',
    'sign-ver': '1',
    'tdid': '7270531146617849345',
    'x-tt-trace-id': '00-235eb3381064e61d8e92920601c3ffff-235eb3381064e61d-01',
    'user-agent': 'Cronet/TTNetVersion:01594da2 2023-03-14 QuicVersion:46688bb4 2022-11-28',
}

json_data = {
    'id': '477f8422-6f5a-446c-9ad5-f895238d3685',
    'pack_options': {
        'need_attribute': True,
    },
}

response = requests.post('https://editor-api-sg.capcut.com/lv/v1/audio_subtitle/query', headers=headers, json=json_data)
print(response.json())