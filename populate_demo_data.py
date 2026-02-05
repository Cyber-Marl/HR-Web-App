import os
import django
from django.utils.text import slugify
from django.utils import timezone
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strategic_synergy.settings')
django.setup()

from careers.models import Job
from insights.models import Article

def populate_jobs():
    print("Populating Jobs...")
    jobs_data = [
        {
            "title": "Senior HR Consultant",
            "location": "New York, NY",
            "job_type": "FT",
            "description": "We are seeking an experienced HR Consultant to lead strategic initiatives for our Fortune 500 clients. You will be responsible for organizational design, change management, and leadership development programs.",
            "requirements": "- 7+ years of HR consulting experience\n- Master's degree in HR or MBA preferred\n- Strong project management skills\n- Willingness to travel up to 30%",
            "salary_range": "$120k - $150k"
        },
        {
            "title": "Talent Acquisition Specialist",
            "location": "Remote / Chicago",
            "job_type": "FT",
            "description": "Join our dynamic recruiting team to find the best talent in the industry. You will manage the full recruitment lifecycle for technical and executive roles.",
            "requirements": "- 3+ years of recruiting experience\n- Proficiency with modern ATS systems\n- Excellent communication skills\n- Experience with LinkedIn Recruiter",
            "salary_range": "$80k - $100k"
        },
        {
            "title": "Organizational Development Intern",
            "location": "London, UK",
            "job_type": "IN",
            "description": "A unique opportunity for a graduate student to gain hands-on experience in organizational psychology and workforce planning. You will support senior consultants on data analysis and workshop facilitation.",
            "requirements": "- Currently enrolled in a relevant Master's program\n- Strong analytical skills\n- Proficiency in Excel and PowerPoint",
            "salary_range": "Paid Internship"
        },
        {
            "title": "Compensation Analyst",
            "location": "San Francisco, CA",
            "job_type": "CT",
            "description": "We need a contract analyst to help review and restructure our client's compensation packages. This is a 6-month project focusing on tech sector benchmarking.",
            "requirements": "- 5+ years of compensation analysis\n- Knowledge of Radford or similar surveys\n- Detail-oriented mindset",
            "salary_range": "$90/hr"
        }
    ]

    for job in jobs_data:
        Job.objects.get_or_create(
            title=job["title"],
            defaults=job
        )
    print(f"Created/Verified {len(jobs_data)} jobs.")

def populate_insights():
    print("Populating Insights...")
    articles_data = [
        {
            "title": "The Evolution of Hybrid Leadership",
            "category": "LEADERSHIP",
            "author": "Sarah Jenkins, Partner",
            "content": "As remote work becomes the norm rather than the exception, leadership styles must evolve. The old 'command and control' model is dead. Today's successful leaders are facilitators, empathy-driven coaches who focus on output rather than hours logged.\n\nKey takeaways:\n1. Trust is the new currency of leadership.\n2. Asynchronous communication skills are vital.\n3. Mental health awareness is a business imperative.\n\nWe explored these themes in our recent survey of 500 CEOs..."
        },
        {
            "title": "AI in Recruitment: Bias or Benefit?",
            "category": "TECH",
            "author": "Marcus Thorne, Tech Lead",
            "content": "Artificial Intelligence is revolutionizing how we hire, from resume screening to predictive analytics for candidate success. But with great power comes great responsibility. Algorithmic bias is a real threat if models are trained on historical data that reflects past prejudices.\n\nIn this article, we discuss how to audit your AI tools for fairness and ensuring that the 'human' remains in Human Resources."
        },
        {
            "title": "Building a Culture of Belonging",
            "category": "CULTURE",
            "author": "Elena Rodriguez, DEI Director",
            "content": "Diversity is being invited to the party; inclusion is being asked to dance; belonging is knowing all the songs. Creating a culture where every employee feels they truly belong is the next frontier for DEI initiatives.\n\nIt requires moving beyond metrics and quotas to addressing the day-to-day micro-interactions that define an employee's experience. Psychological safety is paramount."
        },
        {
            "title": "Strategic Workforce Planning for 2030",
            "category": "STRATEGY",
            "author": "Dr. Alan Grant",
            "content": "What will your workforce look like in 5 years? If you don't have an answer, you're already behind. Demographic shifts, the gig economy, and automation are reshaping the talent landscape.\n\nStrategic workforce planning moves beyond simple headcount forecasting to skill-gap analysis and scenario planning. Organizations must become agile learning organisms to survive."
        }
    ]

    for article in articles_data:
        slug = slugify(article["title"])
        Article.objects.get_or_create(
            title=article["title"],
            defaults={
                "slug": slug,
                "category": article["category"],
                "author": article["author"],
                "content": article["content"],
                "is_published": True
            }
        )
    print(f"Created/Verified {len(articles_data)} articles.")

if __name__ == "__main__":
    populate_jobs()
    populate_insights()
    print("Done!")
