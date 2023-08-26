import requests

headers = {
    'Host': 'editor-api-sg.capcut.com',
    'content-type': 'application/json',
    'appvr': '2.4.0',
    'device-time': '1692810521',
    'lan': 'en',
    'loc': 'VN',
    'pf': '4',
    'sign': 'fca64c5df5bf84d571290404936a09f3',
    'sign-ver': '1',
    'tdid': '7270531146617849345',
    'x-tt-trace-id': '00-235eae471064e61d8e929206019effff-235eae471064e61d-01',
    'user-agent': 'Cronet/TTNetVersion:01594da2 2023-03-14 QuicVersion:46688bb4 2022-11-28',
}

json_data = {
    'adjust_endtime': 200,
    'audio': 'tos-alisg-v-2f54d9-sg/oMUYXNA7EhimGgABDayeoz7BdEWtQ5AtgwUfDC',
    'caption_type': 0,
    'client_request_id': 'e85fc69c-1ecc-424c-8be5-e50061bace53',
    'language': 'zh-CN',
    'max_lines': 1,
    'songs_info': [
        {
            'end_time': 11000,
            'id': '',
            'start_time': 0,
        },
    ],
    'words_per_line': 15,
}

response = requests.post('https://editor-api-sg.capcut.com/lv/v1/audio_subtitle/submit', headers=headers, json=json_data)

print(response.json())