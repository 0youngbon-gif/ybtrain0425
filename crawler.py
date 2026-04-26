import sys
import io
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Windows 콘솔 UTF-8 출력 설정
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


RSS_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"


def fetch_news(limit=10):
    resp = requests.get(RSS_URL, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "xml")
    items = soup.find_all("item")[:limit]

    articles = []
    for item in items:
        title = item.find("title").text.strip() if item.find("title") else "제목 없음"
        link = item.find("link").text.strip() if item.find("link") else ""
        summary = item.find("description").text.strip() if item.find("description") else ""
        pub_date = item.find("pubDate").text.strip() if item.find("pubDate") else ""

        # HTML 태그 제거 (요약에 포함된 경우)
        if summary:
            summary_soup = BeautifulSoup(summary, "html.parser")
            summary = summary_soup.get_text(strip=True)

        # 발행시간 포맷 통일
        if pub_date:
            try:
                dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S GMT")
                pub_date = dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                pass

        articles.append({
            "title": title,
            "link": link,
            "summary": summary,
            "pub_date": pub_date,
        })

    return articles


def print_articles(articles):
    for i, a in enumerate(articles, 1):
        print(f"[{i:>2}] {a['title']}")
        print(f"     시간: {a['pub_date']}")
        if a["summary"]:
            short = a["summary"][:120] + ("..." if len(a["summary"]) > 120 else "")
            print(f"     요약: {short}")
        print(f"     링크: {a['link']}")
        print()


if __name__ == "__main__":
    print("구글 뉴스 한국어 RSS 크롤러\n")
    articles = fetch_news(limit=10)
    print_articles(articles)
    print(f"총 {len(articles)}건 수집 완료")
