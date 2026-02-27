import requests
from bs4 import BeautifulSoup
import database
import notifier
from datetime import datetime

def fetch_and_parse(url, selector):
    try:
        # verify=False is a workaround for the SSL error in the environment
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        elements = soup.select(selector)
        if elements:
            # Join text of all matching elements
            return "\n".join([el.get_text(strip=True) for el in elements])
        else:
            return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def process_job(job_id):
    job = database.get_job(job_id)
    if not job:
        print(f"Job {job_id} not found.")
        return

    content = fetch_and_parse(job['url'], job['selector'])

    if content is None:
        print(f"No content found for job {job_id}")
        return

    latest_result = database.get_latest_result(job_id)

    if not latest_result or latest_result['content'] != content:
        database.add_result(job_id, content)
        if latest_result:
             notifier.send_notification(job, content)
        else:
            print(f"Initial scrape for job {job_id} completed.")
    else:
        print(f"No change detected for job {job_id}.")

        conn = database.get_db_connection()
        conn.execute('UPDATE jobs SET last_run = CURRENT_TIMESTAMP WHERE id = ?', (job_id,))
        conn.commit()
        conn.close()
