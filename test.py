import Util

if __name__ == '__main__':
    # 获取命令行和配置文件
    cmd = Util.Command()
    config = cmd.config_dict
    dyheaders = cmd.dyheaders

    # 异步下载作品
    Util.asyncio.run(Util.Profile(config, dyheaders).get_Profile('https://www.douyin.com/user/MS4wLjABAAAAR_5M3pI3k9fFHapqTrrroWXnTvSrLtZxW6bwS5BaInw'))
    # input("[  提示  ]:下载完成，输入任意键退出。")