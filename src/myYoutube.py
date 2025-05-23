import feedparser
from googleapiclient.discovery import build
import os
import myJson
import src.data_class as data_class

DEVELOPER_KEY = os.environ["youtube_api_key"]
youtube = build("youtube","v3",developerKey=DEVELOPER_KEY)

base_url = "https://www.youtube.com/feeds/videos.xml?channel_id="

def get_rss(id: str):
    url = base_url + id
    rss = feedparser.parse(url)

    return rss

def get_videos_list(rss) -> data_class.LiveData:
    videos_response = youtube.videos().list(id=','.join(entry["yt_videoid"]for entry in rss["entries"]), 
                                           part='liveStreamingDetails').execute()
    on_lives = []

    for item in videos_response["items"]:
        if "liveStreamingDetails" in item:
            if "actualStartTime" in item["liveStreamingDetails"] and "actualEndTime" not in item["liveStreamingDetails"]:
                rssdata = next(x for x in rss["entries"] if item["id"] == x["yt_videoid"])
                data = data_class.LiveData(rssdata["author_detail"]["name"], rssdata["title"], rssdata["link"])
                data_class.printData(data)
                on_lives.append(data)

    return on_lives

def is_err_https(status:int):
    ret = True
    if status == 200:
        pass
    elif status >= 400:
        print("Client err:" + status)
        #ToDO "display_name"もエラーに表示したい
        ret = False
    elif status >= 500:
        print("Server err:" + status)
        ret = False
    
    return ret

def get_onlives():
    print("youtube get_onlives start --- ")
    livers = myJson.load_livers()
    on_lives = []

    for liver in livers:
        if not liver["youtube"]["channel_id"]:
            continue

        # check channel rss
        rss = get_rss(liver["youtube"]["channel_id"])

        if is_err_https(rss["status"]):
            # check on lives
            videos_list = get_videos_list(rss)

            # mod list data
            for live in videos_list:
                data_class.mod_liver_name(live, liver["name"])
                data_class.mod_liver_tags(live, liver["tags"])
            
            on_lives += videos_list
    
    return on_lives


if __name__ == "__main__":
    get_onlives()
