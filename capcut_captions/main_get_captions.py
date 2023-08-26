import time

import requests
import zlib
from requests_auth_aws_sigv4 import AWSSigV4
import random


def crc32(content):
    prev = 0
    prev = zlib.crc32(content, prev)
    return ("%X" % (prev & 0xFFFFFFFF)).lower().zfill(8)
def uploadAudio(video_path):
    video_content=None
    if "http" in video_path:
        if requests.head(video_path).status_code==200:
            video_content = requests.get(video_path, allow_redirects=True).content
    else:
        with open(video_path, "rb") as f:
            video_content = f.read()
    if not video_content:
        return None
    session=requests.session()
    headers = {
        'Host': 'editor-api-sg.capcut.com',
        'app-sdk-version': '2.4.0',
        'content-type': 'application/json',
        'appid': '359289',
        'appvr': '2.4.0',
        'device-time': '1692803434',
        'lan': 'en',
        'loc': 'VN',
        'pf': '4',
        'sign': '8d47a947b370ecf620499f18da59e0e2',
        'sign-ver': '1',
        'tdid': '7270531146617849345',
        'x-tt-trace-id': '00-22f288a11064e61d8e9292060129ffff-22f288a11064e61d-01',
        'user-agent': 'Cronet/TTNetVersion:01594da2 2023-03-14 QuicVersion:46688bb4 2022-11-28',
    }
    json_data = {
        'biz': 'capcut-pc-resource',
        'key_version': 'v5',
    }
    response = session.post('https://editor-api-sg.capcut.com/lv/v1/upload_sign', headers=headers, json=json_data)
    upload_sign=response.json()
    access_key= upload_sign['data']['access_key_id']
    secret_key= upload_sign['data']['secret_access_key']
    session_token= upload_sign['data']['session_token']
    request_parameters = f'Action=ApplyUploadInner&SpaceName=capcut-pc-resource-sg&UseQuic=false&Version=2020-11-19&device_platform=win'
    url='https://vas-alisg16.byteoversea.com/top/v1'
    aws_auth = AWSSigV4('vod',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
        region='sdwdmwlll'
    )
    r = session.get(f"{url}?{request_parameters}", auth=aws_auth)

    file_size = len(video_content)
    upload_node = r.json()["Result"]["InnerUploadAddress"]["UploadNodes"][0]
    video_id = upload_node["Vid"]
    store_uri = upload_node["StoreInfos"][0]["StoreUri"]
    video_auth = upload_node["StoreInfos"][0]["Auth"]
    upload_host = upload_node["UploadHost"]
    session_key = upload_node["SessionKey"]

    # Start video upload

    url = f"https://{upload_host}/{store_uri}?uploads"
    rand = ''.join(random.choice(['0','1','2','3','4','5','6','7','8','9']) for _ in range(30))
    headers = {
        "Authorization": video_auth,
        "Content-Type": f"multipart/form-data; boundary=---------------------------{rand}"
    }
    data = f"-----------------------------{rand}--"
    r = session.post(url, headers=headers, data=data)
    upload_id = r.json()["payload"]["uploadID"]
    # Split file in chunks of 5242880 bytes
    chunk_size = 5242880
    chunks = []
    i = 0
    while i < file_size:
        chunks.append(video_content[i:i+chunk_size])
        i += chunk_size

    # Upload chunks
    crcs = []
    for i in range(len(chunks)):
        chunk = chunks[i]
        crc = crc32(chunk)
        crcs.append(crc)
        url = f"https://{upload_host}/{store_uri}?partNumber={i+1}&uploadID={upload_id}"
        headers = {
            "Authorization": video_auth,
            "Content-Type": "application/octet-stream",
            "Content-Disposition": 'attachment; filename="undefined"',
            "Content-Crc32": crc
        }
        r = session.post(url, headers=headers, data=chunk)

    url = f"https://{upload_host}/{store_uri}?uploadID={upload_id}"
    headers = {
        "Authorization": video_auth,
        "Content-Type": "text/plain;charset=UTF-8",
    }
    data = ','.join([f"{i+1}:{crcs[i]}" for i in range(len(crcs))])
    r = requests.post(url, headers=headers, data=data)


    url = "https://vas-alisg16.byteoversea.com/top/v1"
    request_parameters = f'Action=CommitUploadInner&SpaceName=capcut-pc-resource-sg&Version=2020-11-19&device_platform=win'
    data = '{"SessionKey":"'+session_key+'","Functions":[]}'
    response = session.post(f"{url}?{request_parameters}", data=data, auth=aws_auth).json()
    if "Result" in response:
        return response['Result']['Results'][0]['VideoMeta']
    return None

def cc_request(audio_uri, end_time, lang='zh-CN'):
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
        'audio': audio_uri,
        'caption_type': 0,
        'client_request_id': 'e85fc69c-1ecc-424c-8be5-e50061bace53',
        'language': lang,
        'max_lines': 1,
        'songs_info': [
            {
                'end_time': end_time,
                'id': '',
                'start_time': 0,
            },
        ],
        'words_per_line': 15,
    }

    response = requests.post('https://editor-api-sg.capcut.com/lv/v1/audio_subtitle/submit', headers=headers,
                             json=json_data).json()
    if "errmsg" in response and response['errmsg'] =='success':
        return response['data']['id']
    return None
def cc_query(id):
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
        'id': id,
        'pack_options': {
            'need_attribute': True,
        },
    }

    response = requests.post('https://editor-api-sg.capcut.com/lv/v1/audio_subtitle/query', headers=headers,
                             json=json_data).json()
    if "errmsg" in response and response['errmsg'] =='success':
        return response['data']
    return None

def getCCData(url):
    videoMeta = uploadAudio(url)
    if videoMeta:
        uri = videoMeta['Uri']
        duration = int(videoMeta['Duration'] * 1000)
        cc_id = cc_request(uri, duration)
        if cc_id:
            cc_data = None
            while not cc_data:
                time.sleep(5)
                cc_data = cc_query(cc_id)
            return cc_data
    return None
if __name__=="__main__":
    print("start")
    # domain="http://127.0.0.1:8000"
    domain="https://mazon.click"

    while 1:
        try:
            url_get_job=f"{domain}/api/douyin/video/captions/get-job"
            url_update_job = f"{domain}/api/douyin/video/captions/update"
            obj = requests.get(url_get_job).json()
            if "id" in obj:
                aweme_id = obj['aweme_id']
                print("processing: "+str(aweme_id))
                url_video=f"https://doy.69hot.info/res/{aweme_id}_video.mp4"
                cc_data=getCCData(url_video)
                if cc_data:
                    obj['captions'] = cc_data
                    obj['status'] = 3
                else:
                    obj['status'] = 4
                rs = requests.post(url_update_job,json= obj).json()
                print(rs)
        except:
            pass
        time.sleep(3)
