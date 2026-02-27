import database
import os

def test_db_setup():
    if os.path.exists(database.DB_NAME):
        os.remove(database.DB_NAME)

    database.init_db()

    assert os.path.exists(database.DB_NAME)

    job_id = database.add_job("http://example.com", "h1", 10)
    assert job_id is not None

    jobs = database.get_jobs()
    assert len(jobs) == 1
    assert jobs[0]['url'] == "http://example.com"

    database.add_result(job_id, "Example Domain")

    result = database.get_latest_result(job_id)
    assert result['content'] == "Example Domain"

    updated_job = database.get_job(job_id)
    assert updated_job['last_run'] is not None

    database.delete_job(job_id)
    jobs_after_delete = database.get_jobs()
    assert len(jobs_after_delete) == 0

    print("Database verification successful!")

if __name__ == "__main__":
    test_db_setup()
