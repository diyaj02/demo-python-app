
import os
import uuid

import pytest
import psycopg
import redis

from db import init_db, create_note, get_notes, update_note, delete_note


@pytest.fixture
def services():
    if not os.environ.get("DATABASE_URL") or not os.environ.get("REDIS_URL"):
        pytest.skip("Database and Redis URLs are not configured")

    init_db()

    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        conn.execute("SELECT 1")

    client = redis.Redis.from_url(os.environ["REDIS_URL"])
    assert client.ping()

    return client


def test_notes_crud(services):
    title = f"Integration Test {uuid.uuid4().hex}"

    note_id = create_note(title, "Original content")

    try:
        notes = get_notes()
        assert any(
            note["id"] == note_id and note["title"] == title
            for note in notes
        )

        assert update_note(note_id, title, "Updated content")

        notes = get_notes()
        assert any(
            note["id"] == note_id
            and note["content"] == "Updated content"
            for note in notes
        )
    finally:
        delete_note(note_id)

    assert not any(
        note["id"] == note_id for note in get_notes()
    )


def test_redis_cache(services):
    key = f"integration-test:{uuid.uuid4().hex}"

    try:
        services.set(key, "working", ex=60)
        assert services.get(key) == b"working"
    finally:
        services.delete(key)
