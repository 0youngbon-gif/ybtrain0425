"""Google News RSS → SQLite posts 테이블 시드 스크립트"""

import os
import sqlite3
from pathlib import Path

from crawler import fetch_news

DB_PATH = Path(os.getenv("DATABASE_PATH", str(Path(__file__).resolve().parent / "instance" / "posts.db")))


def seed_news(limit=10):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    conn.commit()

    articles = fetch_news(limit=limit)
    added = 0
    skipped = 0

    for a in articles:
        exists = conn.execute("SELECT 1 FROM posts WHERE title = ?", (a["title"],)).fetchone()
        if exists:
            print(f"  건너뛰기(중복): {a['title']}")
            skipped += 1
            continue

        content = a["summary"] or a["title"]
        conn.execute(
            "INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)",
            (a["title"], content, a["pub_date"]),
        )
        print(f"  추가됨: {a['title']}")
        added += 1

    conn.commit()
    conn.close()
    print(f"\n총 {len(articles)}건 중 {added}건 추가, {skipped}건 건너뛰기 완료")


if __name__ == "__main__":
    print("뉴스 시드 시작\n")
    seed_news()
