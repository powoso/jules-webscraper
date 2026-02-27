from flask import Flask, render_template, request, redirect, url_for
import database
import scheduler_service
import scraper

app = Flask(__name__)

# Initialize DB on start
database.init_db()

# Start scheduler
scheduler_service.start_scheduler()

# Load existing jobs into scheduler on restart
# In a production app, we would query DB and add them.
def load_jobs_from_db():
    jobs = database.get_jobs()
    for job in jobs:
        if job['is_active']:
            scheduler_service.add_job_to_scheduler(job['id'], job['interval_minutes'])

load_jobs_from_db()

@app.route('/')
def index():
    jobs = database.get_jobs()
    return render_template('index.html', jobs=jobs)

@app.route('/add', methods=['POST'])
def add_job():
    url = request.form['url']
    selector = request.form['selector']
    interval = int(request.form['interval'])

    job_id = database.add_job(url, selector, interval)
    scheduler_service.add_job_to_scheduler(job_id, interval)

    # Trigger an immediate run for user feedback? Optional.
    # scraper.process_job(job_id)

    return redirect(url_for('index'))

@app.route('/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    database.delete_job(job_id)
    scheduler_service.remove_job_from_scheduler(job_id)
    return redirect(url_for('index'))

@app.route('/results/<int:job_id>')
def job_results(job_id):
    job = database.get_job(job_id)
    results = database.get_job_results(job_id)
    return render_template('results.html', job=job, results=results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
