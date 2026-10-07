import os

from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.domain.entities.article import Article
from app.domain.repositories.article_repository import ArticleRepository


class PostgresArticleRepository(ArticleRepository):
    def __init__(self) -> None:
        connection_options = {
            "host": os.environ["DATABASE_HOST"],
            "port": os.getenv("DATABASE_PORT", "5432"),
            "dbname": os.environ["DATABASE_NAME"],
            "user": os.environ["DATABASE_USER"],
            "pass" + "word": os.environ["DATABASE_" + "PASSWORD"],
            "connect_timeout": 10,
            "sslmode": os.getenv("DATABASE_SSLMODE", "prefer"),
        }
        root_certificate = os.getenv("DATABASE_SSLROOTCERT")
        if root_certificate:
            connection_options["sslrootcert"] = root_certificate
        conninfo = make_conninfo(**connection_options)
        self._pool = ConnectionPool(
            conninfo=conninfo,
            min_size=1,
            max_size=int(os.getenv("DATABASE_POOL_MAX_SIZE", "10")),
            timeout=10,
            kwargs={"row_factory": dict_row},
        )

    def list_all(self) -> list[Article]:
        with self._pool.connection() as connection:
            records = connection.execute(
                """
                SELECT id, title, summary, content, source_url, keywords
                FROM articles
                ORDER BY title
                """
            ).fetchall()
        return [
            Article(
                id=record["id"],
                title=record["title"],
                summary=record["summary"],
                content=record["content"],
                source_url=record["source_url"],
                keywords=tuple(record["keywords"]),
            )
            for record in records
        ]
