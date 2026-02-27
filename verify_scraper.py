import database
import scraper
import os
import time

def test_scraper_logic():
    # Reset DB
    if os.path.exists(database.DB_NAME):
        os.remove(database.DB_NAME)
    database.init_db()

    # Create a job for a reliable site (e.g., example.com)
    job_id = database.add_job("https://example.com", "h1", 1)
    print(f"Created job {job_id}")

    # First run - should save result
    scraper.process_job(job_id)
    result = database.get_latest_result(job_id)
    assert result is not None
    assert "Example Domain" in result['content']
    print("First scrape successful.")

    # Second run - no change
    # We can't easily mock the response without extra libs, so we rely on the site not changing in 2 seconds
    time.sleep(2)
    scraper.process_job(job_id)
    results = database.get_job_results(job_id)
    # Should still be 1 result because content didn't change
    assert len(results) == 1
    print("No duplicate result saved for unchanged content.")

    # Verify last_run updated
    job = database.get_job(job_id)
    print(f"Last run: {job['last_run']}")

    print("Scraper verification successful!")

if __name__ == "__main__":
    test_scraper_logic()
