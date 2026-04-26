import os
import random
from datetime import datetime, timedelta
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

    # 테이블이 비어 있으면 샘플 데이터 자동 생성
    count = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    if count == 0:
        _seed_data(db)


TITLES = [
    "Flask로 웹 앱 만들기", "Python 기초 다지기", "SQLite 활용법",
    "HTML과 CSS 시작하기", "JavaScript 입문 가이드", "Git 사용법 정리",
    "REST API 설계 원칙", "데이터베이스 정규화", "클라우드 서비스 비교",
    "도커 컨테이너 기초", "리눅스 명령어 모음", "알고리즘 공부법",
    "반응형 웹 디자인", "프론트엔드 트렌드 2026", "백엔드 아키텍처",
    "TDD 실천하기", "코드 리뷰 문화", "CI/CD 파이프라인",
    "마이크로서비스 개론", "보안 기본 지식", "성능 최적화 팁",
    "디자인 패턴 정리", "객체지향 프로그래밍", "함수형 프로그래밍",
    "타입스크립트 시작", "Next.js 프로젝트", "React Hooks 정리",
    "Node.js 백엔드", "Spring Boot 입문", "Django 튜토리얼",
    "API 문서화 방법", "유닛 테스트 작성", "통합 테스트 전략",
    "버전 관리 워크플로우", "코드 품질 관리", "기술 블로그 작성법",
    "오픈소스 기여 가이드", "개발자 포트폴리오", "면접 준비 팁",
    "원격 근무 생산성", "애자일 방법론", "스크럼 실천법",
    "프로젝트 관리 도구", "개발 환경 세팅", "VS Code 확장 추천",
    "터미널 커스터마이징", "Python 가상환경", "패키지 매니저 비교",
    "웹 접근성 가이드", "SEO 최적화 방법", "웹 성능 측정",
    "브라우저 렌더링 원리", "HTTP 프로토콜", "WebSocket 실시간 통신",
    "인증과 인가 개념", "JWT 토큰 이해", "OAuth 2.0 흐름",
    "캐싱 전략 비교", "CDN 활용법", "로드 밸런싱 기초",
    "모니터링과 로깅", "에러 추적 시스템", "장애 대응 매뉴얼",
    "데이터베이스 인덱스", "쿼리 최적화", "N+1 문제 해결",
    "트랜잭션 관리", "동시성 제어", "분산 시스템 개론",
    "메시지 큐 활용", "이벤트 드리븐 아키텍처", "CQRS 패턴",
    "도메인 주도 설계", "클린 아키텍처", "헥사고날 아키텍처",
    "서버리스 컴퓨팅", "IaC 인프라 관리", "컨테이너 오케스트레이션",
    "서비스 메시 개념", "API 게이트웨이", "서비스 디스커버리",
    "설정 관리 전략", "피처 플래그 활용", "A/B 테스트",
    "블루그린 배포", "카나리 배포", "롤링 업데이트",
    "데이터 파이프라인", "배치 처리 시스템", "스트림 처리",
    "머신러닝 기초", "딥러닝 프레임워크", "자연어 처리",
    "컴퓨터 비전", "추천 시스템", "데이터 시각화",
    "통계학 기초", "확률과 분포", "회귀 분석",
    "분류 알고리즘", "클러스터링", "차원 축소",
    "모델 평가 방법", "하이퍼파라미터 튜닝", "전이 학습",
    "모델 서빙과 배포", "MLOps 실천", "데이터 품질 관리",
    "실험 추적 시스템", "피처 엔지니어링", "데이터 증강 기법",
    "GAN 생성 모델", "강화학습 개론", "자율주행 기술",
    "IoT 플랫폼", "블록체인 기초", "스마트 컨트랙트",
    "양자 컴퓨팅", "엣지 컴퓨팅", "디지털 트윈",
]

CONTENTS = [
    "오늘은 {topic}에 대해 알아보겠습니다. 이 주제는 최근 개발 트렌드에서 매우 중요한 위치를 차지하고 있으며, 많은 개발자들이 관심을 가지고 학습하고 있는 분야입니다.\n\n먼저 기본 개념부터 시작해봅시다. {topic}의 핵심은 간단하지만, 이를 실제 프로젝트에 적용하려면 여러 가지 고려해야 할 사항들이 있습니다. 특히 성능, 보안, 유지보수성 측면에서 신중한 접근이 필요합니다.\n\n실무에서는 이러한 개념들을 조합하여 복잡한 시스템을 구축하게 됩니다. 따라서 기초가 탄탄해야 응용도 가능합니다. 꾸준한 학습과 실습이 중요합니다.",
    "{topic}을 배우면서 느낀 점을 정리해봤습니다. 처음에는 개념이 어렵게 느껴졌지만, 실제로 프로젝트에 적용해보니 이해가 빠르게 되었습니다.\n\n가장 중요한 것은 직접 해보는 것입니다. 이론만으로는 한계가 있고, 실제 코드를 작성하고 디버깅하면서 배우는 것이 가장 효과적입니다.\n\n앞으로도 꾸준히 실습하면서 실력을 키워나가겠습니다. 함께 공부하는 분들도 화이팅!",
    "이 글에서는 {topic}의 실무 적용 사례를 소개합니다. 실제 프로젝트에서 겪은 문제와 해결 과정을 공유하겠습니다.\n\n문제 상황: 기존 시스템에서 성능 병목이 발생했습니다.\n\n해결 과정: 원인을 분석하고 단계적으로 개선했습니다.\n\n결과: 응답 시간이 50% 개선되었고, 사용자 만족도도 크게 향상되었습니다.\n\n이 경험을 통해 {topic}의 중요성을 다시 한번 깨달았습니다.",
    "{topic}에 대한 최신 트렌드를 정리합니다. 2026년 현재 이 분야는 빠르게 발전하고 있으며, 새로운 도구와 프레임워크가 계속 등장하고 있습니다.\n\n주요 변화:\n- AI 통합이 기본이 됨\n- 클라우드 네이티브 접근이 표준\n- 개발자 경험(DX) 중시\n- 보안이 설계 단계부터 포함\n\n이러한 트렌드를 이해하고 대비하는 것이 중요합니다. 새로운 기술을 무작정 따르기보다는, 프로젝트 요구사항에 맞는 적절한 선택이 필요합니다.",
    "오늘 {topic} 스터디 노트를 공유합니다. 핵심 포인트만 간추려 정리했으니 빠르게 복습할 수 있습니다.\n\n핵심 개념:\n1. 기본 원리 이해하기\n2. 실습으로 확인하기\n3. 실제 프로젝트에 적용하기\n4. 피드백 받고 개선하기\n\n이 4단계로 학습하면 효율적입니다. 중요한 것은 매일 조금씩이라도 꾸준히 하는 것입니다. 완벽하지 않아도 좋으니 일단 시작하세요!",
]


def _seed_data(db: sqlite3.Connection) -> None:
    base_date = datetime(2026, 1, 1)
    for i in range(120):
        title = TITLES[i % len(TITLES)]
        if i >= len(TITLES):
            title = f"[{i + 1}] {title}"
        content = CONTENTS[i % len(CONTENTS)].replace("{topic}", title)
        created_at = base_date + timedelta(
            days=random.randint(0, 115),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )
        db.execute(
            "INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)",
            (title, content, created_at.strftime("%Y-%m-%d %H:%M:%S")),
        )
    db.commit()


PER_PAGE = 10


@app.route("/")
def index() -> str:
    return redirect(url_for("posts_list"))


@app.route("/posts")
def posts_list() -> str:
    db = get_db()

    page = request.args.get("page", 1, type=int)
    search = request.args.get("q", "").strip()
    sort = request.args.get("sort", "newest")

    where_clause = ""
    params: list[str | int] = []

    if search:
        where_clause = "WHERE title LIKE ? OR content LIKE ?"
        params.extend([f"%{search}%", f"%{search}%"])

    order_map = {
        "newest": "ORDER BY created_at DESC",
        "oldest": "ORDER BY created_at ASC",
        "title_asc": "ORDER BY title ASC",
        "title_desc": "ORDER BY title DESC",
    }
    order_clause = order_map.get(sort, order_map["newest"])

    total = db.execute(
        f"SELECT COUNT(*) FROM posts {where_clause}", params
    ).fetchone()[0]
    total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    page = min(page, total_pages)
    offset = (page - 1) * PER_PAGE

    posts = db.execute(
        f"SELECT id, title, content, created_at FROM posts {where_clause} {order_clause} LIMIT ? OFFSET ?",
        params + [PER_PAGE, offset],
    ).fetchall()

    return render_template(
        "posts/list.html",
        posts=posts,
        page=page,
        total_pages=total_pages,
        total=total,
        search=search,
        sort=sort,
    )


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
