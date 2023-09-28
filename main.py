import os

import Util
import time, requests
if __name__ == '__main__':
    # 获取命令行和配置文件
    cmd = Util.Command()
    config = cmd.config_dict
    dyheaders = cmd.dyheaders
    cnt=0
    while 1:
        try:
            rs = requests.get("https://mazon.click/api/douyin/user/crawl/get").json()
            if "url" in rs:
                Util.asyncio.run(Util.Profile(config, dyheaders).get_Profile(rs['url']))
        except:
            pass
        time.sleep(5)
        cnt+=1
        if(cnt>86400/5):
            os.system("reboot")
            break