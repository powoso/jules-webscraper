import pytest
import os
import tempfile
import time
import database
import scheduler_service
import scraper
from app.app import app
import threading

# Helper to mock scraper to avoid external requests
def mock_fetch_and_parse(url, selector):
    if "change" in url:
        return f"Changed Content for {selector}"
    return f"Content for {selector}"

@pytest.fixture
def client_with_scheduler():
    db_fd, database.DB_NAME = tempfile.mkstemp()
    app.config['TESTING'] = True
    database.init_db()

    # Patch scraper
    original_fetch = scraper.fetch_and_parse
    scraper.fetch_and_parse = mock_fetch_and_parse

    # Start scheduler
    scheduler_service.start_scheduler()

    # Clean scheduler for this test run
    scheduler_service.scheduler.remove_all_jobs()

    with app.test_client() as client:
        yield client

    # Cleanup
    scheduler_service.scheduler.shutdown()
    scraper.fetch_and_parse = original_fetch
    os.close(db_fd)
    os.unlink(database.DB_NAME)

def test_full_flow(client_with_scheduler):
    # 1. Add a job via UI
    rv = client_with_scheduler.post('/add', data=dict(
        url='http://example.com',
        selector='h1',
        interval=1 # 1 minute
    ), follow_redirects=True)
    assert rv.status_code == 200
    assert b"http://example.com" in rv.data

    # 2. Verify job is in DB and Scheduler
    jobs = database.get_jobs()
    assert len(jobs) == 1
    job_id = jobs[0]['id']

    scheduled_jobs = scheduler_service.get_scheduled_jobs()
    assert len(scheduled_jobs) == 1
    assert scheduled_jobs[0].id == str(job_id)

    # 3. Trigger manual execution (simulating scheduler run)
    scraper.process_job(job_id)

    # 4. Check results via UI
    rv = client_with_scheduler.get(f'/results/{job_id}')
    assert rv.status_code == 200
    assert b"Content for h1" in rv.data

    # 5. Simulate Change
    # Update job URL to trigger "change" in mock
    # We don't have an edit UI, so direct DB update
    conn = database.get_db_connection()
    conn.execute('UPDATE jobs SET url = ? WHERE id = ?', ('http://change.com', job_id))
    conn.commit()
    conn.close()

    scraper.process_job(job_id)

    # 6. Check results again
    rv = client_with_scheduler.get(f'/results/{job_id}')
    assert b"Changed Content for h1" in rv.data

    # 7. Delete Job
    rv = client_with_scheduler.post(f'/delete/{job_id}', follow_redirects=True)
    assert rv.status_code == 200

    jobs = database.get_jobs()
    assert len(jobs) == 0

    scheduled_jobs = scheduler_service.get_scheduled_jobs()
    assert len(scheduled_jobs) == 0

if __name__ == "__main__":
    pytest.main()
