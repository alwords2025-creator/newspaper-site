"""WEB-001 v1.0 - fetch RSS feeds listed in feeds.json and write news.json.
Standard library only. Stores headline, short summary, link and source;
every story links back to the publisher."""
import json, re, html, sys, urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

PER_FEED = 12

def clean(text, limit=220):
    text = html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip()
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "..."

def parse_date(s):
    try:
        return parsedate_to_datetime(s).astimezone(timezone.utc).isoformat()
    except Exception:
        return datetime.now(timezone.utc).isoformat()

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "WEB-001-news-reader/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return ET.fromstring(r.read())

def main():
    feeds = json.load(open("feeds.json", encoding="utf-8"))
    out, seen = [], set()
    for category, items in feeds.items():
        for f in items:
            try:
                root = fetch(f["url"])
            except Exception as e:
                print(f"skip {f['source']}: {e}", file=sys.stderr)
                continue
            for it in root.iter("item"):
                link = (it.findtext("link") or "").strip()
                title = clean(it.findtext("title"), 160)
                if not link or not title or link in seen:
                    continue
                seen.add(link)
                out.append({"title": title, "summary": clean(it.findtext("description")),
                            "link": link, "source": f["source"], "category": category,
                            "published": parse_date(it.findtext("pubDate"))})
                if sum(1 for x in out if x["source"] == f["source"]) >= PER_FEED:
                    break
    out.sort(key=lambda x: x["published"], reverse=True)
    json.dump({"updated": datetime.now(timezone.utc).isoformat(), "stories": out},
              open("news.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {len(out)} stories")

if __name__ == "__main__":
    main()
