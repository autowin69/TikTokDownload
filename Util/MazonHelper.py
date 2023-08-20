import requests
import os
import shutil
home_page="https://mazon.click/api"
def validateAweme(aweme_data):
    url=f"{home_page}/douyin/video/validate"
    return requests.post(url, json=aweme_data).json()
def addUser(url_uid, awee):
    url = f"{home_page}/douyin/user/add"
    data = {'url': url_uid, 'uid': awee['uid'],  'nickname': awee['nickname'], 'aweme_count': awee['aweme_count']}
    return requests.post(url, json=data).json()

def moveFile(path):
    config_path = os.path.join(os.getcwd(), "doy_config.txt")
    cmd = f"rclone --config {config_path} move \"{path}\" r2sync:doy/res/"
    os.system(cmd)

def createR2Tmp():
    tmp_sync_dir = os.path.join(os.getcwd(), 'tmp_sync_r2')
    if not os.path.exists(tmp_sync_dir):
        os.makedirs(tmp_sync_dir)
    return tmp_sync_dir
def syncR2TmpFolder():
    config_path = os.path.join(os.getcwd(), "doy_config.txt")
    tmp_sync_dir = createR2Tmp()
    cmd = f"rclone --config {config_path} move \"{tmp_sync_dir}/\" r2sync:doy/res/ --include \"*\""
    os.system(cmd)
def moveFile2TmpFolder(path):
    basename = os.path.basename(path)
    tmp_sync_dir = createR2Tmp()
    new_path=os.path.join(tmp_sync_dir,basename)
    shutil.move(path,new_path)
