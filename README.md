CRM Application Setup Guide
This guide provides instructions to set up and run the CRM application with Celery and Celery Beat for scheduled tasks.
Prerequisites

Python 3.8 or higher
Redis server

Setup Instructions

Install Redis

On Ubuntu/Debian:sudo apt update
sudo apt install redis-server


On macOS:brew install redis


Ensure Redis is running:redis-server




Install Dependencies

Install the required Python packages:pip install -r requirements.txt




Run Database Migrations

Apply migrations to set up the database:python manage.py migrate




Start Celery Worker

Run the Celery worker to process tasks:celery -A crm worker -l info




Start Celery Beat

Run Celery Beat to schedule periodic tasks:celery -A crm beat -l info





Verifying Logs

Check the weekly CRM report logs in /tmp/crm_report_log.txt for details on total customers, orders, and revenue.
Logs are generated every Monday at 6:00 AM UTC.

Additional Notes

Ensure the GraphQL endpoint (http://localhost:8000/graphql) is accessible.
The Celery task uses Redis as the broker (redis://localhost:6379/0). Verify Redis is running on the default port or update the configuration in crm/settings.py if needed.
