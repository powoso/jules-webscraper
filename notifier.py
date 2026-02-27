def send_notification(job, new_content):
    print(f"==================================================")
    print(f"NOTIFICATION: Change detected for job {job['id']}!")
    print(f"URL: {job['url']}")
    print(f"Selector: {job['selector']}")
    print(f"New Content: {new_content.strip()[:100]}...")
    print(f"==================================================")
