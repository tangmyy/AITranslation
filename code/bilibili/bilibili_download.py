from bilibili_api import select_client
import asyncio
import time
from bilibili_api import video
from bilibili_api.video import (
    VideoStreamDownloadURL,
    VideoDownloadURLDataDetecter,
    VideoQuality,
)

from bilibili_api import Credential, HEADERS, get_client
import os
from dotenv import load_dotenv


class BilibliDownloader:
    def __init__(self, bvid: str):
        self.bvid = bvid
        self.credential = Credential(
            sessdata=os.getenv("SESSDATA"),
            bili_jct=os.getenv("BILI_JCT"),
            buvid3=os.getenv("BUVID3"),
        )
        self.video = video.Video(bvid=bvid, credential=self.credential)
        self.download_stat = 0.0
        self.thumnail_url = ""
        self.selected_quality = VideoQuality._720P

    # 下载进度刷新
    async def update_progress(self):
        while True:
            await asyncio.sleep(0.3)
            # print(f"downloading... {self.download_stat}%", end="\n")
            if self.download_stat == 100.0:
                break

    # 下载器核心方法  
    async def download(self, url: str, out: str, intro: str):
        dwn_id = await get_client().download_create(url, HEADERS)
        bts = 0
        tot = get_client().download_content_length(dwn_id)
        with open(out, "wb") as file:
            while True:
                bts += file.write(await get_client().download_chunk(dwn_id))
                print(f"{intro} - {out} [{bts} / {tot}]", end="\r")
                self.download_stat = bts / tot * 100

                if bts == tot:
                    break

    # 视频下载主流程                  
    async def download_by_bvid(self, bvid: str):
        # 实例化 Credential 类
        load_dotenv()  # take environment variables from .env.
        SESSDATA = os.getenv("SESSDATA")
        BILI_JCT = os.getenv("BILI_JCT")
        BUVID3 = os.getenv("BUVID3")
        FFMPEG_PATH = os.getenv("FFMPEG_PATH")
        credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
        # 实例化 Video 类
        v = video.Video(bvid=bvid, credential=credential)
        # 获取视频下载链接
        download_url_data = await v.get_download_url(0)
        # 解析视频下载信息
        detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
        streams = detecter.detect_best_streams()
        current_timestamp = int(time.time())
        # 有 MP4 流 / FLV 流两种可能
        if detecter.check_flv_mp4_stream() == True:
            # FLV 流下载
            await self.download(streams[0].url, "flv_temp.flv", "下载 FLV 音视频流")
            # 转换文件格式

            os.system(f"{FFMPEG_PATH} -y -i flv_temp.flv video_{current_timestamp}.mp4")
            # 删除临时文件
            os.remove("flv_temp.flv")
        else:
            # MP4 流下载
            await self.download(streams[0].url, "video_temp.m4s", "下载视频流")
            await self.download(streams[1].url, "audio_temp.m4s", "下载音频流")
            # 混流
            os.system(
                f"{FFMPEG_PATH} -y -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy video_{current_timestamp}.mp4"
            )
            # 删除临时文件
            os.remove("video_temp.m4s")
            os.remove("audio_temp.m4s")

        print(f"已下载为：video_{current_timestamp}.mp4")

        # 实例化 Credential 类

    # 获取封面信息
    async def get_vidoe_info(self, bvid) -> None:
        # 实例化 Video 类
        v = video.Video(bvid=bvid)
        # 获取信息
        info = await v.get_info()
        download_url = await v.get_download_url(page_index=0)
        dector = VideoDownloadURLDataDetecter(download_url)
        self.thumnail_url = info["pic"]
        print(self.thumnail_url)
        all_data = dector.detect(video_max_quality=VideoQuality._360P)

        # for data in all_data:
        #     if isinstance(data, VideoStreamDownloadURL):
        #         print(data.url)
        #         print(data.video_quality)
        #         print(data.video_codecs)

        # 打印信息

    # 主异步入口
    async def main(self):
        await asyncio.gather(
            self.download_by_bvid(self.bvid),
            self.update_progress(),
            self.get_vidoe_info(self.bvid),
        )


if __name__ == "__main__":
    # 主入口
    downloader = BilibliDownloader("BV1vp37zDEVZ")
    asyncio.run(downloader.main())


# async def main():
#     await asyncio.gather(get_vidoe_info("BV1xRKSznESn"), get_vidoe_info("BV1X2KkzkEzn"))


# if __name__ == "__main__":
#     select_client("aiohttp")
#     asyncio.run(main())
