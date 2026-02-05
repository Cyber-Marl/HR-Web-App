import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strategic_synergy.settings')
django.setup()

from careers.models import Job

jobs = Job.objects.all()
print(f"Total Jobs: {jobs.count()}")

for job in jobs:
    print(f"\nJob: {job.title}")
    print(f"  Posted: {job.posted_at}")
    print(f"  Deadline: {job.deadline}")
    print(f"  Has deadline: {job.deadline is not None}")
