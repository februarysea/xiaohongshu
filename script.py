# Mimproxy script
# Get notes urls from mobile phone redbooknotes
# mitmdump -s notesScript.py

from mitmproxy import ctx
import json
import time

def response(flow):
    note_url = "https://edith.xiaohongshu.com/api/sns/v2/note/feed?"
    user_url = "https://edith.xiaohongshu.com/api/sns/v3/user/info?"

    item = {}

    # notes
    if flow.request.url.startswith(note_url):
        text = json.loads(flow.response.text)
        note = text["data"][0]["note_list"][0]
        item["title"] = note["title"]
        item["url"] = f"https://www.xiaohongshu.com/discovery/item/{note['id']}"
        item["content"] = note["desc"]
        item["comment_nr"] = note["comments_count"]
        images = []
        for image in note["images_list"]:
            images.append(image["url"])
        item["images"] = images
        item["like_nr"] = note["liked_count"]
        item["star_nr"] = note["collected_count"]
        item["user_url"] = f"https://www.xiaohongshu.com/user/profile/{note['id']}"
        item["datePublished"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(note["time"])))
        with open("notes.txt", "a") as f:
            f.write(f"{str(item)}\n")
        ctx.log.warn(str(item))
        
    # user info
    if flow.request.url.startswith(user_url):
        text = json.loads(flow.response.text)
        user = text["data"]
        item["author_collect_nr"] = user["note_num_stat"]["collected"]
        item["author_fans_nr"] = user["fans"]
        item["author_name"] = user["nickname"]
        item["author_note_nr"] = user["note_num_stat"]["posted"]
        with open("noteUsers.txt", "a") as f:
            f.write(f"{str(item)}\n")
        ctx.log.warn(str(item))