import os
import shutil
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from insights.models import Article


class Command(BaseCommand):
    help = 'Populate insights articles with images and create new articles'

    def handle(self, *args, **options):
        static_img = os.path.join(settings.BASE_DIR, 'static', 'img')
        media_dest = os.path.join(settings.MEDIA_ROOT, 'insights', 'images')
        os.makedirs(media_dest, exist_ok=True)

        # Map existing articles to images from static/img
        existing_updates = {
            'building-a-culture-of-belonging': {
                'source_img': '20180324_121720.jpg',
                'dest_name': 'culture_belonging.jpg',
            },
            'ai-in-recruitment-bias-or-benefit': {
                'source_img': '20221117_112421.jpg',
                'dest_name': 'ai_recruitment.jpg',
            },
            'the-evolution-of-hybrid-leadership': {
                'source_img': '20190223_093854.jpg',
                'dest_name': 'hybrid_leadership.jpg',
            },
        }

        # Update existing articles with images
        for slug, img_info in existing_updates.items():
            try:
                article = Article.objects.get(slug=slug)
                src = os.path.join(static_img, img_info['source_img'])
                if os.path.exists(src):
                    dest = os.path.join(media_dest, img_info['dest_name'])
                    shutil.copy2(src, dest)
                    article.image = f"insights/images/{img_info['dest_name']}"
                    article.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated image for: {article.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Image not found: {src}'))
            except Article.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Article not found: {slug}'))

        # New articles with content and images
        new_articles = [
            {
                'title': 'The Future of Remote Work in 2026',
                'slug': 'future-of-remote-work-2026',
                'author': 'Dr. Sarah Moyo',
                'category': 'STRATEGY',
                'source_img': '20220716_115522.jpg',
                'dest_name': 'remote_work_future.jpg',
                'content': (
                    "The landscape of work has undergone a seismic shift. As we navigate "
                    "through 2026, remote and hybrid work models have evolved from emergency "
                    "measures into sophisticated, technology-driven ecosystems that are "
                    "redefining how organisations operate.\n\n"
                    
                    "The Rise of Digital-First Workplaces\n\n"
                    "Forward-thinking companies are no longer asking whether remote work is "
                    "viable — they are asking how to optimise it. Digital-first workplaces "
                    "leverage cloud collaboration tools, AI-powered project management, and "
                    "virtual reality meeting spaces to create seamless experiences that rival "
                    "in-person interactions.\n\n"
                    
                    "Key Trends Shaping Remote Work\n\n"
                    "1. Asynchronous Communication: Teams spread across time zones are "
                    "embracing async-first communication, reducing meeting fatigue while "
                    "improving documentation and decision-making quality.\n\n"
                    
                    "2. Results-Based Performance: The shift from hours-based to outcomes-based "
                    "performance measurement is empowering employees while giving managers "
                    "clearer visibility into productivity.\n\n"
                    
                    "3. Digital Nomad Policies: Progressive employers are developing formal "
                    "policies that allow employees to work from anywhere, attracting top "
                    "talent from a global pool.\n\n"
                    
                    "4. Hybrid Hub Models: Companies are replacing traditional offices with "
                    "smaller, purpose-built collaboration hubs designed for team gatherings "
                    "and creative workshops.\n\n"
                    
                    "Challenges and Solutions\n\n"
                    "While the benefits are clear, remote work presents challenges around "
                    "culture building, onboarding new employees, and maintaining team cohesion. "
                    "Successful organisations are addressing these through regular in-person "
                    "retreats, virtual team-building activities, and dedicated culture "
                    "ambassadors.\n\n"
                    
                    "The evidence is compelling: companies that master remote work will have "
                    "a decisive competitive advantage in talent acquisition, employee "
                    "satisfaction, and operational resilience. The future of work isn't "
                    "coming — it's already here."
                ),
            },
            {
                'title': 'Mental Health in the Modern Workplace',
                'slug': 'mental-health-modern-workplace',
                'author': 'Tatenda Chirwa',
                'category': 'CULTURE',
                'source_img': '20190930_152447.jpg',
                'dest_name': 'mental_health_workplace.jpg',
                'content': (
                    "Employee mental health has risen to the top of every progressive HR "
                    "leader's agenda. In today's fast-paced work environment, the line "
                    "between professional and personal life has blurred, making mental "
                    "wellbeing not just a moral imperative but a business-critical priority.\n\n"
                    
                    "The Business Case for Mental Health\n\n"
                    "Research consistently shows that organisations investing in employee "
                    "mental health see significant returns. Reduced absenteeism, increased "
                    "productivity, and lower turnover rates all contribute to a compelling "
                    "ROI. Companies with robust mental health programmes report up to 25% "
                    "higher employee engagement scores.\n\n"
                    
                    "Building a Supportive Framework\n\n"
                    "Creating a mentally healthy workplace requires a multi-layered approach:\n\n"
                    
                    "Leadership Training: Managers are the frontline of mental health support. "
                    "Training them to recognise signs of burnout, have empathetic "
                    "conversations, and direct employees to resources is fundamental.\n\n"
                    
                    "Flexible Work Arrangements: Autonomy over when and where work happens "
                    "is one of the most powerful tools for supporting mental health. "
                    "Organisations that offer genuine flexibility see measurable improvements "
                    "in employee wellbeing.\n\n"
                    
                    "Employee Assistance Programmes (EAPs): Modern EAPs go beyond crisis "
                    "intervention to include preventive coaching, financial wellness tools, "
                    "and family support services.\n\n"
                    
                    "Psychologically Safe Cultures: Teams where people feel safe to speak up, "
                    "make mistakes, and be vulnerable consistently outperform those dominated "
                    "by fear and hierarchy.\n\n"
                    
                    "Measuring What Matters\n\n"
                    "Progressive organisations are moving beyond traditional engagement "
                    "surveys to implement real-time wellbeing pulse checks, anonymised "
                    "sentiment analysis, and predictive analytics that identify burnout "
                    "risks before they escalate.\n\n"
                    
                    "The message is clear: mental health is not a perk — it is the "
                    "foundation of sustainable high performance."
                ),
            },
            {
                'title': 'Diversity, Equity & Inclusion: Beyond the Buzzwords',
                'slug': 'dei-beyond-buzzwords',
                'author': 'Rumbidzai Ncube',
                'category': 'LEADERSHIP',
                'source_img': '20181005_124606.jpg',
                'dest_name': 'dei_inclusion.jpg',
                'content': (
                    "Diversity, Equity, and Inclusion (DEI) has moved beyond corporate "
                    "rhetoric into a measurable business discipline. The organisations "
                    "seeing real results are those that have embedded DEI into their "
                    "operational DNA rather than treating it as a standalone initiative.\n\n"
                    
                    "From Compliance to Competitive Advantage\n\n"
                    "The data is unequivocal: diverse teams make better decisions, drive "
                    "more innovation, and deliver stronger financial performance. Companies "
                    "in the top quartile for ethnic and cultural diversity are 36% more "
                    "likely to outperform their peers in profitability.\n\n"
                    
                    "Practical Steps for Meaningful Change\n\n"
                    "1. Inclusive Hiring Practices: Blind resume screening, diverse interview "
                    "panels, and structured interviews reduce bias and broaden talent pools.\n\n"
                    
                    "2. Equitable Career Development: Sponsorship programmes, mentoring "
                    "circles, and transparent promotion criteria ensure talent from all "
                    "backgrounds has equal opportunity to advance.\n\n"
                    
                    "3. Belonging Metrics: Measuring inclusion through belonging scores, "
                    "psychological safety indices, and retention analytics provides "
                    "actionable data for continuous improvement.\n\n"
                    
                    "4. Inclusive Leadership Training: Leaders set the tone. Training "
                    "programmes that build awareness of unconscious bias, micro-aggressions, "
                    "and inclusive decision-making are essential.\n\n"
                    
                    "The Path Forward\n\n"
                    "True inclusion requires sustained commitment, accountability, and "
                    "courage. It means examining systems, challenging norms, and creating "
                    "spaces where every individual can contribute their best work. The "
                    "organisations that get this right will define the future of business."
                ),
            },
            {
                'title': 'Upskilling Your Workforce for the AI Era',
                'slug': 'upskilling-workforce-ai-era',
                'author': 'Kudzai Mutasa',
                'category': 'TECH',
                'source_img': '20191001_092327.jpg',
                'dest_name': 'upskilling_ai.jpg',
                'content': (
                    "Artificial intelligence is not replacing workers — it is redefining "
                    "what work looks like. The organisations that will thrive are those "
                    "investing proactively in upskilling their workforce to collaborate "
                    "effectively with AI systems.\n\n"
                    
                    "The Skills Revolution\n\n"
                    "According to the World Economic Forum, 44% of workers' skills will "
                    "be disrupted in the next five years. This isn't cause for alarm — "
                    "it's an opportunity. The skills most in demand are uniquely human: "
                    "critical thinking, creativity, emotional intelligence, and complex "
                    "problem-solving.\n\n"
                    
                    "Building an AI-Ready Organisation\n\n"
                    "Data Literacy for All: Every employee should understand basic data "
                    "concepts, how AI makes decisions, and how to interpret AI-generated "
                    "insights. This doesn't require everyone to become a data scientist, "
                    "but it does require basic fluency.\n\n"
                    
                    "AI Augmentation Training: Teaching employees to use AI as a force "
                    "multiplier — for research, analysis, content creation, and "
                    "decision-support — dramatically increases individual productivity.\n\n"
                    
                    "Continuous Learning Culture: Moving from annual training events to "
                    "always-on learning ecosystems with micro-learning, peer coaching, "
                    "and experimentation time is essential.\n\n"
                    
                    "Strategic Workforce Planning\n\n"
                    "HR leaders must map their current workforce capabilities against "
                    "future requirements, identifying gaps, transition pathways, and "
                    "investment priorities. This is no longer a nice-to-have — it is "
                    "a strategic imperative.\n\n"
                    
                    "The organisations that invest in their people today will lead "
                    "their industries tomorrow."
                ),
            },
            {
                'title': 'Employee Retention Strategies That Actually Work',
                'slug': 'employee-retention-strategies',
                'author': 'Farai Mhaka',
                'category': 'TALENT',
                'source_img': '20181002_122658.jpg',
                'dest_name': 'employee_retention.jpg',
                'content': (
                    "The cost of losing a skilled employee can be 50% to 200% of their "
                    "annual salary. Yet many organisations continue to invest heavily in "
                    "recruitment while neglecting the factors that keep their best people "
                    "engaged and committed.\n\n"
                    
                    "Why People Really Leave\n\n"
                    "Exit interviews reveal consistent themes: lack of growth opportunities, "
                    "poor management, feeling undervalued, and misalignment with company "
                    "values. Compensation, while important, is rarely the primary driver.\n\n"
                    
                    "Proven Retention Strategies\n\n"
                    "1. Career Architecture: Creating clear, transparent career pathways "
                    "— including lateral moves and specialist tracks — gives employees "
                    "a compelling reason to stay and grow within the organisation.\n\n"
                    
                    "2. Manager Quality: Investing in manager development is the single "
                    "highest-impact retention strategy. Employees don't leave companies — "
                    "they leave managers.\n\n"
                    
                    "3. Recognition and Appreciation: Frequent, genuine recognition — "
                    "not just annual awards — creates emotional connection and reinforces "
                    "desired behaviours.\n\n"
                    
                    "4. Purpose and Impact: Employees who understand how their work "
                    "contributes to the broader mission are significantly more engaged "
                    "and less likely to leave.\n\n"
                    
                    "5. Stay Interviews: Rather than waiting for exit interviews, "
                    "proactive stay conversations identify satisfaction drivers and "
                    "potential flight risks before it's too late.\n\n"
                    
                    "The Retention Mindset\n\n"
                    "Great retention isn't about perks or gimmicks — it's about creating "
                    "an environment where talented people can do meaningful work, grow "
                    "professionally, and feel genuinely valued. The organisations that "
                    "master this will win the war for talent."
                ),
            },
        ]

        for article_data in new_articles:
            slug = article_data['slug']
            if Article.objects.filter(slug=slug).exists():
                self.stdout.write(self.style.WARNING(f'Article already exists: {slug}'))
                continue

            src = os.path.join(static_img, article_data['source_img'])
            dest_name = article_data['dest_name']
            if os.path.exists(src):
                dest = os.path.join(media_dest, dest_name)
                shutil.copy2(src, dest)
                image_path = f"insights/images/{dest_name}"
            else:
                image_path = ''
                self.stdout.write(self.style.WARNING(f'Image not found: {src}'))

            article = Article.objects.create(
                title=article_data['title'],
                slug=article_data['slug'],
                author=article_data['author'],
                content=article_data['content'],
                image=image_path,
                category=article_data['category'],
                is_published=True,
            )
            self.stdout.write(self.style.SUCCESS(f'Created article: {article.title}'))

        self.stdout.write(self.style.SUCCESS('\nDone! All insights have been updated.'))
