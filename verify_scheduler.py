import scheduler_service
import time
import os
import scraper
import logging

# Configure logging to see scheduler output
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def test_scheduler_api():
    print("Testing Scheduler API...")

    # 1. Start scheduler
    scheduler_service.start_scheduler()
    assert scheduler_service.scheduler.running
    print("Scheduler started.")

    # 2. Add job
    job_id = 123
    interval = 10 # minutes
    scheduler_service.add_job_to_scheduler(job_id, interval)

    jobs = scheduler_service.get_scheduled_jobs()
    assert len(jobs) == 1
    assert jobs[0].id == str(job_id)
    print(f"Job {job_id} added successfully.")

    # 3. Remove job
    scheduler_service.remove_job_from_scheduler(job_id)
    jobs = scheduler_service.get_scheduled_jobs()
    assert len(jobs) == 0
    print(f"Job {job_id} removed successfully.")

    # Shutdown
    scheduler_service.scheduler.shutdown()
    print("Scheduler shutdown successfully.")

if __name__ == "__main__":
    test_scheduler_api()
