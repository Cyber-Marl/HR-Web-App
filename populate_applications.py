import os, sys, django, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strategic_synergy.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from careers.models import Job, Application
from django.utils import timezone
from datetime import timedelta

now = timezone.now()

# Realistic Zimbabwean / Southern African names
first_names = [
    'Tendai', 'Tatenda', 'Rutendo', 'Kudzai', 'Farai', 'Rumbidzai', 'Tafadzwa',
    'Nyasha', 'Chiedza', 'Tinotenda', 'Blessing', 'Grace', 'Privilege', 'Takudzwa',
    'Munyaradzi', 'Simbarashe', 'Tinashe', 'Tanaka', 'Nokuthula', 'Sibongile',
    'Thabo', 'Lerato', 'Naledi', 'Zanele', 'Precious', 'Prosper', 'Brian',
    'Michelle', 'Sandra', 'David', 'Joseph', 'Sarah', 'Linda', 'Margaret',
    'Robert', 'James', 'Patricia', 'Elizabeth', 'Danai', 'Rufaro', 'Tsitsi',
    'Rudo', 'Tariro', 'Yeukai', 'Anesu', 'Tadiwanashe', 'Panashe', 'Makanaka',
]

last_names = [
    'Moyo', 'Ndlovu', 'Ncube', 'Dube', 'Sibanda', 'Mpofu', 'Nkomo',
    'Chirwa', 'Mutasa', 'Mhaka', 'Chikwanha', 'Maposa', 'Gumbo', 'Nyoni',
    'Banda', 'Phiri', 'Zimuto', 'Makoni', 'Tavengwa', 'Chigumba',
    'Mashingaidze', 'Chipunza', 'Nyanungo', 'Mukoko', 'Zvidzai', 'Mataruka',
    'Chakanetsa', 'Mutsvairo', 'Katsande', 'Mushonga', 'Chidhakwa',
    'Mangwende', 'Chikore', 'Mapuranga', 'Hungwe', 'Zvobgo', 'Mazarura',
]

statuses = ['PENDING', 'REVIEWED', 'INTERVIEW', 'REJECTED', 'HIRED']
status_weights = [0.35, 0.25, 0.20, 0.12, 0.08]

cover_letters = [
    "I am writing to express my strong interest in this position. With my background in human resources and passion for organisational development, I believe I can make a meaningful contribution to your team. I am particularly drawn to Strategic Synergy's reputation for excellence in HR consulting.",
    "I am excited to apply for this role at Strategic Synergy. My experience in the HR field has equipped me with the skills and knowledge necessary to excel in this position. I am eager to bring my expertise to your dynamic team and contribute to your clients' success.",
    "Having followed Strategic Synergy's work in the HR consulting space, I am thrilled to apply for this opportunity. My professional experience aligns perfectly with the requirements, and I am confident in my ability to add value from day one.",
    "I am a dedicated HR professional seeking to advance my career with an industry leader. Strategic Synergy's commitment to transforming workplaces resonates deeply with my own professional values. I would welcome the chance to contribute to your mission.",
    "Please accept my application for this exciting role. My track record in human resources, combined with my passion for people development, makes me an ideal candidate. I look forward to discussing how I can contribute to Strategic Synergy's continued success.",
    "I was delighted to see this vacancy advertised. With extensive experience in the HR sector, I am confident that my skills and dedication would be a valuable asset to your team. I am particularly interested in the opportunity to work with diverse client organisations.",
    "As a motivated professional with a strong HR background, I am eager to join Strategic Synergy. I bring a combination of strategic thinking and hands-on experience that I believe would benefit your clients and team alike.",
    "I am applying with great enthusiasm for this position. Throughout my career, I have consistently delivered results in human resources, and I am now seeking an opportunity to apply my expertise at a leading consultancy like Strategic Synergy.",
]

used_names = set()

def generate_applicant():
    while True:
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        full = f"{fn} {ln}"
        if full not in used_names:
            used_names.add(full)
            break
    email = f"{fn.lower()}.{ln.lower()}@{'gmail.com' if random.random() > 0.4 else 'outlook.com'}"
    phone = f"+263 7{random.randint(1,9)} {random.randint(100,999)} {random.randint(1000,9999)}"
    linkedin = f"https://linkedin.com/in/{fn.lower()}-{ln.lower()}-{random.randint(100,999)}" if random.random() > 0.3 else ""
    status = random.choices(statuses, weights=status_weights, k=1)[0]
    rating = random.randint(0, 5) if status != 'PENDING' else 0
    cover = random.choice(cover_letters)
    days_ago = random.randint(1, 45)
    return {
        'full_name': full,
        'email': email,
        'phone': phone,
        'linkedin_url': linkedin,
        'cover_letter': cover,
        'status': status,
        'rating': rating,
        'applied_at_offset': days_ago,
    }


def create_applications(job_title, count):
    try:
        job = Job.objects.get(title__icontains=job_title)
    except Job.DoesNotExist:
        print(f"ERROR: Job not found: {job_title}")
        return
    except Job.MultipleObjectsReturned:
        job = Job.objects.filter(title__icontains=job_title).first()

    created = 0
    for _ in range(count):
        data = generate_applicant()
        app = Application(
            job=job,
            full_name=data['full_name'],
            email=data['email'],
            phone=data['phone'],
            linkedin_url=data['linkedin_url'],
            cover_letter=data['cover_letter'],
            status=data['status'],
            rating=data['rating'],
            resume='resumes/placeholder_cv.pdf',
        )
        app.save()
        # Backdate the applied_at
        Application.objects.filter(pk=app.pk).update(
            applied_at=now - timedelta(days=data['applied_at_offset'])
        )
        created += 1

    print(f"Created {created} applications for: {job.title}")


# Create applications per user request
create_applications('Senior HR Consultant', 10)
create_applications('Talent Acquisition Specialist', 6)
create_applications('Organizational Development Intern', 20)
create_applications('HR Business Partner', 5)
create_applications('Learning & Development Manager', 5)

print(f"\nTotal applications now: {Application.objects.count()}")
