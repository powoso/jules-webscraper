from flask import Flask, render_template, request, redirect, url_for, flash
import database
import scheduler_service
import scraper
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Initialize DB on start
database.init_db()

# Start scheduler
scheduler_service.start_scheduler()

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

    try:
        job_id = database.add_job(url, selector, interval)
        scheduler_service.add_job_to_scheduler(job_id, interval)
        flash('Job added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding job: {str(e)}', 'danger')

    return redirect(url_for('index'))

@app.route('/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    try:
        database.delete_job(job_id)
        scheduler_service.remove_job_from_scheduler(job_id)
        flash('Job deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting job: {str(e)}', 'danger')
    return redirect(url_for('index'))

@app.route('/run/<int:job_id>', methods=['POST'])
def run_job(job_id):
    try:
        scraper.process_job(job_id)
        flash('Job executed manually!', 'info')
    except Exception as e:
        flash(f'Error running job: {str(e)}', 'danger')
    return redirect(url_for('index'))

@app.route('/results/<int:job_id>')
def job_results(job_id):
    job = database.get_job(job_id)
    if not job:
        flash('Job not found!', 'danger')
        return redirect(url_for('index'))
    results = database.get_job_results(job_id)
    return render_template('results.html', job=job, results=results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
