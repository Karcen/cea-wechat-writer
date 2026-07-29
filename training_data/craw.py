import os
import re
import json
import time
import requests
from urllib.parse import urlparse, parse_qs

BASE_DIR = "./train"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/16.0 Safari/605.1.15",
    "Referer": "https://mp.weixin.qq.com/",
}

# 合集列表：目录名 -> 链接
ALBUMS = {
    "广纳英才": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIwMTM3NTc1MA==&action=getalbum&album_id=4359871620916183041#wechat_redirect",
    "会议通知": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIwMTM3NTc1MA==&action=getalbum&album_id=3796870271735398405#wechat_redirect",
    "新近动态": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIwMTM3NTc1MA==&action=getalbum&album_id=3741917144150360078#wechat_redirect",
    "学术前沿": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIwMTM3NTc1MA==&action=getalbum&album_id=3849250294718103552#wechat_redirect",
    "特刊推荐": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIwMTM3NTc1MA==&action=getalbum&album_id=3737597163552030730#wechat_redirect",
    "文章解读": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIwMTM3NTc1MA==&action=getalbum&album_id=3740907519493980161#wechat_redirect",
    "学会历史": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIwMTM3NTc1MA==&action=getalbum&album_id=4084137650704089088#wechat_redirect",
}


def sanitize(name):
    name = re.sub(r'[\\/:*?"<>|\n\r\t]', "_", name).strip()
    return name[:100] or "untitled"


def parse_album_params(url):
    q = parse_qs(urlparse(url).query)
    return q.get("__biz", [""])[0], q.get("album_id", [""])[0]


def get_article_list(session, biz, album_id):
    """分页拉取合集内所有文章，返回 [(title, url), ...]"""
    articles = []
    last_msgid = 0
    last_itemidx = 0
    api = "https://mp.weixin.qq.com/mp/appmsgalbum"
    while True:
        params = {
            "action": "getalbum",
            "__biz": biz,
            "album_id": album_id,
            "count": "20",
            "begin_msgid": last_msgid,
            "begin_itemidx": last_itemidx,
            "f": "json",
        }
        r = session.get(api, params=params, headers=HEADERS, timeout=20)
        try:
            data = r.json()
        except Exception:
            # 首次可能返回 HTML，从中抽取 JSON
            data = extract_from_html(r.text)
            if data is None:
                break

        getalbum = data.get("getalbum_resp") or data
        arts = getalbum.get("article_list") or []
        if not arts:
            break

        for a in arts:
            title = a.get("title", "")
            link = a.get("url", "")
            if link:
                articles.append((title, link))

        continue_flag = str(getalbum.get("continue_flag", "0"))
        if continue_flag != "1" or not arts:
            break

        last = arts[-1]
        last_msgid = last.get("msgid", 0)
        last_itemidx = last.get("itemidx", 0)
        time.sleep(1)

    # 去重
    seen = set()
    uniq = []
    for t, u in articles:
        if u not in seen:
            seen.add(u)
            uniq.append((t, u))
    return uniq


def extract_from_html(html):
    """从合集页面 HTML 中提取内嵌的文章列表 JSON"""
    m = re.search(r'cgiData\s*=\s*(\{.*?\});', html, re.S)
    if not m:
        m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def download_html(session, url, path):
    r = session.get(url, headers=HEADERS, timeout=30)
    r.encoding = r.apparent_encoding or "utf-8"
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)


def main():
    session = requests.Session()
    for folder, url in ALBUMS.items():
        biz, album_id = parse_album_params(url)
        out_dir = os.path.join(BASE_DIR, sanitize(folder))
        os.makedirs(out_dir, exist_ok=True)
        print(f"\n=== 处理合集: {folder} (album_id={album_id}) ===")

        articles = get_article_list(session, biz, album_id)
        print(f"共发现 {len(articles)} 篇文章")

        for i, (title, link) in enumerate(articles, 1):
            fname = f"{i:02d}_{sanitize(title)}.html"
            fpath = os.path.join(out_dir, fname)
            if os.path.exists(fpath):
                print(f"  [{i}] 已存在，跳过: {fname}")
                continue
            try:
                download_html(session, link, fpath)
                print(f"  [{i}] 已下载: {fname}")
            except Exception as e:
                print(f"  [{i}] 下载失败: {title} -> {e}")
            time.sleep(1.5)


if __name__ == "__main__":
    main()