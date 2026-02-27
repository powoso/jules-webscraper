import pytest
import os
import tempfile
import database
from app.app import app

@pytest.fixture
def client():
    db_fd, database.DB_NAME = tempfile.mkstemp()
    app.config['TESTING'] = True
    database.init_db()

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(database.DB_NAME)

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_add_job(client):
    rv = client.post('/add', data=dict(
        url='http://example.com',
        selector='h1',
        interval=10
    ), follow_redirects=True)
    assert rv.status_code == 200

    # Check if job is in DB
    jobs = database.get_jobs()
    assert len(jobs) == 1
    assert jobs[0]['url'] == 'http://example.com'

def test_delete_job(client):
    # Add a job first
    client.post('/add', data=dict(
        url='http://example.com',
        selector='h1',
        interval=10
    ), follow_redirects=True)

    jobs = database.get_jobs()
    job_id = jobs[0]['id']

    rv = client.post(f'/delete/{job_id}', follow_redirects=True)
    assert rv.status_code == 200

    jobs = database.get_jobs()
    assert len(jobs) == 0

def test_results_page(client):
    client.post('/add', data=dict(
        url='http://example.com',
        selector='h1',
        interval=10
    ), follow_redirects=True)

    jobs = database.get_jobs()
    job_id = jobs[0]['id']

    rv = client.get(f'/results/{job_id}')
    assert rv.status_code == 200
