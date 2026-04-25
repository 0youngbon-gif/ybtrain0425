import os
from pathlib import Path
import sqlite3

from flask import Flask, abort, g, redirect, render_template, request, url_for

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = Path(os.getenv("DATABASE_PATH", str(INSTANCE_DIR / "posts.db")))


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
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


def _validate_post_form(title: str, content: str, action: str, post_id: int | None = None) -> str:
    if action == "create":
        return render_template(
            "posts/new.html",
            mode="create",
            form_action=url_for("posts_create"),
            submit_label="Publish",
            error="제목과 내용을 모두 입력해주세요.",
            title=title,
            content=content,
        )

    return render_template(
        "posts/new.html",
        mode="edit",
        form_action=url_for("posts_update", post_id=post_id),
        submit_label="Update",
        error="제목과 내용을 모두 입력해주세요.",
        title=title,
        content=content,
    )


@app.route("/posts", methods=["POST"])
def posts_create() -> str:
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        return _validate_post_form(title, content, "create")

    db = get_db()
    cursor = db.execute(
        "INSERT INTO posts (title, content) VALUES (?, ?)",
        (title, content),
    )
    db.commit()
    return redirect(url_for("posts_detail", post_id=cursor.lastrowid))


@app.route("/posts/<int:post_id>/edit")
def posts_edit(post_id: int) -> str:
    db = get_db()
    post = db.execute(
        "SELECT id, title, content, created_at FROM posts WHERE id = ?",
        (post_id,),
    ).fetchone()

    if post is None:
        abort(404)

    return render_template(
        "posts/new.html",
        mode="edit",
        form_action=url_for("posts_update", post_id=post_id),
        submit_label="Update",
        title=post["title"],
        content=post["content"],
    )


@app.route("/posts/<int:post_id>", methods=["POST"])
def posts_update(post_id: int) -> str:
    db = get_db()
    post = db.execute(
        "SELECT id FROM posts WHERE id = ?",
        (post_id,),
    ).fetchone()

    if post is None:
        abort(404)

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        return _validate_post_form(title, content, "edit", post_id)

    db.execute(
        "UPDATE posts SET title = ?, content = ? WHERE id = ?",
        (title, content, post_id),
    )
    db.commit()
    return redirect(url_for("posts_detail", post_id=post_id))


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def posts_delete(post_id: int) -> str:
    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    return redirect(url_for("posts_list"))


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
