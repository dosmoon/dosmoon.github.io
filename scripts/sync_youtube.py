"""Fetch latest videos from VideoCraftNews channel RSS and write videos.json."""
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

CHANNEL_ID = "UCgEhSmLDY7APGy0xG3fSPuA"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
MAX_ITEMS = 12
OUTPUT = Path(__file__).resolve().parent.parent / "videos.json"

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def fetch_feed() -> bytes:
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "dosmoon-sync/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def parse(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    items = []
    for entry in root.findall("atom:entry", NS)[:MAX_ITEMS]:
        vid = entry.findtext("yt:videoId", namespaces=NS)
        title = entry.findtext("atom:title", namespaces=NS)
        published = entry.findtext("atom:published", namespaces=NS)
        group = entry.find("media:group", NS)
        thumb = ""
        if group is not None:
            t = group.find("media:thumbnail", NS)
            if t is not None:
                thumb = t.get("url", "")
        items.append({
            "id": vid,
            "title": title,
            "published": published,
            "thumbnail": thumb or f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
            "url": f"https://www.youtube.com/watch?v={vid}",
        })
    return items


def main() -> None:
    feed = fetch_feed()
    videos = parse(feed)
    payload = {
        "channel": "VideoCraftNews",
        "channelUrl": f"https://www.youtube.com/channel/{CHANNEL_ID}",
        "videos": videos,
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(videos)} videos to {OUTPUT}")


if __name__ == "__main__":
    main()
