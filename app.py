from pathlib import Path
import sqlite3

from flask import Flask, abort, g, redirect, render_template, request, url_for

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = INSTANCE_DIR / "posts.db"


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        INSTANCE_DIR.mkdir(exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error: Exception | None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()


@app.route("/")
def index() -> str:
    return posts_list()


@app.route("/posts")
def posts_list() -> str:
    db = get_db()
    posts = db.execute(
        "SELECT id, title, content, created_at FROM posts ORDER BY id DESC"
    ).fetchall()
    return render_template("posts/list.html", posts=posts)


@app.route("/posts/new")
def posts_new() -> str:
    return render_template("posts/new.html")


@app.route("/posts", methods=["POST"])
def posts_create() -> str:
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        return render_template(
            "posts/new.html",
            error="제목과 내용을 모두 입력해주세요.",
            title=title,
            content=content,
        )

    db = get_db()
    cursor = db.execute(
        "INSERT INTO posts (title, content) VALUES (?, ?)",
        (title, content),
    )
    db.commit()
    return redirect(url_for("posts_detail", post_id=cursor.lastrowid))


@app.route("/posts/<int:post_id>")
def posts_detail(post_id: int) -> str:
    db = get_db()
    post = db.execute(
        "SELECT id, title, content, created_at FROM posts WHERE id = ?",
        (post_id,),
    ).fetchone()

    if post is None:
        abort(404)

    return render_template("posts/detail.html", post=post)


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)
