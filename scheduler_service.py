from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import scraper
import atexit

scheduler = BackgroundScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        # Shut down the scheduler when exiting the app, if it is running
        atexit.register(lambda: scheduler.shutdown() if scheduler.running else None)

def add_job_to_scheduler(job_id, interval_minutes):
    if not scheduler.running:
        start_scheduler()

    # Remove if exists to update
    if scheduler.get_job(str(job_id)):
        scheduler.remove_job(str(job_id))

    scheduler.add_job(
        func=scraper.process_job,
        trigger=IntervalTrigger(minutes=interval_minutes),
        args=[job_id],
        id=str(job_id),
        replace_existing=True
    )

def remove_job_from_scheduler(job_id):
    if scheduler.get_job(str(job_id)):
        scheduler.remove_job(str(job_id))

def get_scheduled_jobs():
    return scheduler.get_jobs()
