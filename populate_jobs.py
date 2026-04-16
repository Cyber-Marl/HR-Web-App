import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strategic_synergy.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from careers.models import Job
from django.utils import timezone
from datetime import timedelta

now = timezone.now()

jobs = [
    {
        'title': 'HR Business Partner',
        'location': 'Harare, Zimbabwe',
        'job_type': 'FT',
        'salary_range': '$45,000 - $65,000',
        'deadline': now + timedelta(days=30),
        'description': 'We are seeking an experienced HR Business Partner to join our growing team. You will serve as a strategic advisor to business leaders, aligning HR initiatives with organisational goals.\n\nKey Responsibilities:\n- Partner with senior leadership to develop and implement HR strategies\n- Drive talent management, succession planning, and workforce planning initiatives\n- Provide coaching and guidance to managers on employee relations matters\n- Analyse HR metrics and provide data-driven recommendations\n- Lead change management efforts across the organisation\n- Ensure compliance with local labour laws and company policies',
        'requirements': "- Bachelor's degree in Human Resources, Business Administration, or related field\n- 5+ years of progressive HR experience, with at least 2 years as an HRBP\n- Strong knowledge of Zimbabwe labour law and employment regulations\n- Excellent communication, negotiation, and conflict resolution skills\n- IPMZ or CIPD certification preferred\n- Proficiency in HRIS systems and Microsoft Office Suite",
    },
    {
        'title': 'Learning & Development Manager',
        'location': 'Bulawayo, Zimbabwe',
        'job_type': 'FT',
        'salary_range': '$50,000 - $70,000',
        'deadline': now + timedelta(days=45),
        'description': 'Strategic Synergy is looking for a dynamic Learning & Development Manager to design and deliver impactful training programmes that build organisational capability.\n\nKey Responsibilities:\n- Design, develop, and implement comprehensive L&D strategies\n- Conduct training needs analysis across all business units\n- Create blended learning solutions including e-learning, workshops, and coaching\n- Manage the annual training budget and track ROI on learning investments\n- Develop leadership development programmes for emerging and senior leaders\n- Build partnerships with external training providers and academic institutions',
        'requirements': "- Master's degree in Education, HR, or Organisational Development\n- 7+ years of experience in learning and development\n- Proven track record of designing and delivering leadership programmes\n- Experience with LMS platforms and e-learning authoring tools\n- Strong facilitation and presentation skills\n- Training of Trainers (ToT) certification is an advantage",
    },
    {
        'title': 'Payroll & Benefits Administrator',
        'location': 'Harare, Zimbabwe',
        'job_type': 'FT',
        'salary_range': '$30,000 - $42,000',
        'deadline': now + timedelta(days=21),
        'description': 'We are hiring a detail-oriented Payroll & Benefits Administrator to manage end-to-end payroll processing and employee benefits administration.\n\nKey Responsibilities:\n- Process monthly payroll for 500+ employees accurately and on time\n- Administer employee benefits including medical aid, pension, and insurance\n- Ensure compliance with ZIMRA tax requirements and NSSA contributions\n- Maintain accurate employee records and payroll documentation\n- Handle payroll queries and resolve discrepancies promptly\n- Prepare payroll reports and analytics for management review',
        'requirements': "- Diploma or degree in Accounting, Finance, or HR\n- 3+ years of payroll administration experience\n- Strong knowledge of PAYE, NSSA, and statutory deductions in Zimbabwe\n- Proficiency in payroll software (Belina, SAP, or similar)\n- Advanced Excel skills\n- High attention to detail and confidentiality",
    },
    {
        'title': 'Recruitment Coordinator',
        'location': 'Remote / Harare',
        'job_type': 'CT',
        'salary_range': '$25,000 - $35,000',
        'deadline': now + timedelta(days=14),
        'description': 'Join our Talent Acquisition team as a Recruitment Coordinator on a 12-month contract. You will support the full recruitment lifecycle for multiple client organisations.\n\nKey Responsibilities:\n- Coordinate interview scheduling and logistics for candidates and hiring managers\n- Screen CVs and conduct initial phone interviews\n- Manage job postings across multiple platforms and social media channels\n- Maintain the applicant tracking system with accurate candidate data\n- Prepare recruitment reports and pipeline analytics\n- Support employer branding initiatives and career fair participation',
        'requirements': "- Bachelor's degree in HR, Psychology, or Business\n- 2+ years of recruitment or HR coordination experience\n- Familiarity with applicant tracking systems\n- Excellent organisational and time management skills\n- Strong written and verbal communication\n- Ability to handle multiple priorities in a fast-paced environment",
    },
    {
        'title': 'Employee Wellness Specialist',
        'location': 'Harare, Zimbabwe',
        'job_type': 'FT',
        'salary_range': '$35,000 - $48,000',
        'deadline': now + timedelta(days=28),
        'description': 'We are looking for a passionate Employee Wellness Specialist to design and manage comprehensive workplace wellness programmes for our clients.\n\nKey Responsibilities:\n- Develop and implement employee wellness strategies and programmes\n- Coordinate mental health awareness campaigns and workshops\n- Manage Employee Assistance Programme (EAP) vendor relationships\n- Conduct wellness assessments and analyse programme effectiveness\n- Organise health screenings, fitness challenges, and wellbeing events\n- Provide one-on-one wellness coaching to employees',
        'requirements': "- Degree in Psychology, Social Work, Public Health, or related field\n- 3+ years of experience in employee wellness or occupational health\n- Knowledge of mental health first aid and crisis intervention\n- Certification in wellness coaching or counselling preferred\n- Strong empathy, communication, and programme management skills\n- Experience with wellness technology platforms",
    },
    {
        'title': 'HR Data Analyst',
        'location': 'Remote',
        'job_type': 'FT',
        'salary_range': '$40,000 - $55,000',
        'deadline': now + timedelta(days=35),
        'description': 'Strategic Synergy is seeking an HR Data Analyst to transform people data into actionable insights that drive strategic decision-making.\n\nKey Responsibilities:\n- Build and maintain HR dashboards and reporting systems\n- Analyse workforce trends including turnover, engagement, and diversity metrics\n- Develop predictive models for attrition risk and talent forecasting\n- Partner with HR leaders to identify data-driven solutions to business challenges\n- Ensure data integrity and governance across all HR systems\n- Present findings and recommendations to senior stakeholders',
        'requirements': "- Bachelor's degree in Data Science, Statistics, HR Analytics, or related field\n- 3+ years of experience in data analysis, preferably in HR context\n- Proficiency in Python, R, SQL, and data visualisation tools (Power BI/Tableau)\n- Experience with HRIS platforms (Workday, SAP SuccessFactors, or similar)\n- Strong analytical thinking and storytelling with data\n- Knowledge of GDPR/POPIA data privacy regulations",
    },
    {
        'title': 'Graduate HR Trainee',
        'location': 'Harare, Zimbabwe',
        'job_type': 'IN',
        'salary_range': '$12,000 - $18,000',
        'deadline': now + timedelta(days=21),
        'description': "Kickstart your HR career with our 18-month Graduate Trainee Programme. You will rotate through all HR functions gaining hands-on experience in a leading consultancy.\n\nKey Responsibilities:\n- Rotate through Recruitment, L&D, Compensation, and Employee Relations\n- Assist with day-to-day HR operations and administrative tasks\n- Support the delivery of client consulting projects\n- Participate in training workshops and professional development sessions\n- Contribute to research projects on emerging HR trends\n- Complete a capstone project presented to senior leadership",
        'requirements': "- Recent graduate (2025/2026) with a degree in HR, Business, or Social Sciences\n- Strong academic record (2.1 or above)\n- Genuine passion for human resources and people development\n- Excellent communication and interpersonal skills\n- Proficiency in Microsoft Office\n- Willingness to learn and adapt in a fast-paced environment",
    },
    {
        'title': 'Change Management Consultant',
        'location': 'Johannesburg, South Africa',
        'job_type': 'FT',
        'salary_range': '$55,000 - $75,000',
        'deadline': now + timedelta(days=40),
        'description': "We are expanding our regional presence and seeking a Change Management Consultant to lead transformation initiatives for our corporate clients across Southern Africa.\n\nKey Responsibilities:\n- Lead change management workstreams for large-scale transformation projects\n- Conduct stakeholder analysis and develop communication strategies\n- Design change readiness assessments and impact analyses\n- Develop training and coaching plans to support adoption\n- Facilitate workshops and town halls to engage employees through change\n- Measure and report on change adoption and business outcomes",
        'requirements': "- Master's degree in Business, Organisational Psychology, or related field\n- 5+ years of change management consulting experience\n- Prosci, ACMP, or similar change management certification\n- Experience with digital transformation and ERP implementations\n- Strong stakeholder management and executive presence\n- Willingness to travel across Southern Africa (up to 40%)",
    },
    {
        'title': 'Diversity, Equity & Inclusion Lead',
        'location': 'Harare, Zimbabwe',
        'job_type': 'PT',
        'salary_range': '$28,000 - $38,000',
        'deadline': now + timedelta(days=25),
        'description': "Strategic Synergy is hiring a part-time DEI Lead to develop and drive our clients' diversity, equity, and inclusion strategies.\n\nKey Responsibilities:\n- Develop DEI strategies, roadmaps, and action plans for client organisations\n- Conduct diversity audits and analyse representation data\n- Design and facilitate unconscious bias and inclusive leadership training\n- Establish Employee Resource Groups (ERGs) and mentoring programmes\n- Advise on inclusive recruitment practices and equitable policies\n- Track DEI metrics and report progress to leadership teams",
        'requirements': "- Degree in Social Sciences, HR, Law, or related field\n- 4+ years of experience in DEI, HR, or organisational development\n- Deep understanding of intersectionality and inclusive workplace practices\n- Experience designing and delivering DEI training programmes\n- Strong facilitation, research, and data analysis skills\n- Passion for social justice and creating equitable workplaces",
    },
    {
        'title': 'Labour Relations Officer',
        'location': 'Mutare, Zimbabwe',
        'job_type': 'FT',
        'salary_range': '$38,000 - $52,000',
        'deadline': now + timedelta(days=30),
        'description': "We are looking for an experienced Labour Relations Officer to manage employee relations and ensure compliance with labour legislation for our clients in the Eastern Highlands region.\n\nKey Responsibilities:\n- Advise clients on labour law compliance and best practices\n- Handle disciplinary hearings, grievances, and dispute resolution proceedings\n- Represent clients at the Labour Court and conciliation/arbitration proceedings\n- Draft employment contracts, policies, and HR procedures\n- Conduct workplace investigations and prepare investigation reports\n- Provide training on labour law updates and employee relations practices",
        'requirements': "- Degree in Law, Labour Relations, or Human Resources\n- 5+ years of experience in labour relations or employment law\n- In-depth knowledge of the Zimbabwe Labour Act and related legislation\n- Experience with NEC proceedings and collective bargaining\n- Strong negotiation, mediation, and conflict resolution skills\n- Valid driver's licence and willingness to travel within the region",
    },
]

for j in jobs:
    Job.objects.create(**j)
    print(f'Created: {j["title"]}')

print(f'\nTotal jobs now: {Job.objects.count()}')
