import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strategic_synergy.settings')
django.setup()

from careers.models import Job

count = Job.objects.count()
print(f"Total Jobs in database: {count}")

if count > 0:
    print("Listing first 5 jobs:")
    for job in Job.objects.all()[:5]:
        print(f"- {job.title} (ID: {job.id}, Active: {job.is_active})")
else:
    print("No jobs found in the database.")
