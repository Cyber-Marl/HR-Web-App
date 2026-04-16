import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, ListFlowable, ListItem
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Configuration
ARTIFACT_DIR = r"C:\Users\marlv\.gemini\antigravity\brain\ded1a0ea-dfd7-4c76-a4ca-7544cdfc9d17"
OUTPUT_FILE = r"C:\Users\marlv\Documents\lims\HR-Web-App\Strategic_Synergy_HR_WebApp_Documentation.pdf"

PAGES = [
    {
        "title": "Home Page",
        "features": [
            "Clear hero section with value proposition",
            "Dynamic navigation bar with login access",
            "Overview of key HR consulting services",
            "Professional, dark-themed responsive design"
        ],
        "image": "home_page_1773070941558.png"
    },
    {
        "title": "About Page",
        "features": [
            "Company history and core values",
            "Mission and vision statements",
            "Leadership team overview",
            "Engaging visual hero section"
        ],
        "image": "about_hero_section_1773046114901.png"
    },
    {
        "title": "Services Page",
        "features": [
            "Comprehensive directory of HR solutions",
            "Categorized service offerings (e.g., Talent Acquisition, Structuring)",
            "Clear descriptions for each service area",
            "Call to action for client inquiries"
        ],
        "image": "services_page_1773048384323.png"
    },
    {
        "title": "Careers Page",
        "features": [
            "List of open job positions",
            "Filtering options by Job Type and Location",
            "Clean tabular/card layout for easy scanning",
            "Direct links to job details and application"
        ],
        "image": "careers_page_1773048424599.png"
    },
    {
        "title": "Job Detail Page",
        "features": [
            "Detailed job description and requirements",
            "Key metadata: Location, Job Type, Salary, Deadline",
            "Direct 'Apply Now' functionality",
            "Clear presentation of organizational context"
        ],
        "image": "job_detail_page_1773070988149.png" # Fixed
    },
    {
        "title": "Events Page",
        "features": [
            "Listing of upcoming corporate events",
            "Event details including dates, locations, and descriptions",
            "Registration links or instructions",
            "Past events gallery or summary"
        ],
        "image": "events_page_1773048449750.png"
    },
    {
        "title": "Insights (Articles) Page",
        "features": [
            "Blog-style thought leadership articles",
            "Industry news and HR trends",
            "Categorized content for easy discovery",
            "Author attribution and publication dates"
        ],
        "image": "insights_page_1773048486640.png"
    },
    {
        "title": "Resources Page",
        "features": [
            "Downloadable templates and guides",
            "Whitepapers and case studies",
            "Searchable resource library",
            "Valuable tools for HR professionals"
        ],
        "image": "resources_page_1773048521057.png"
    },
    {
        "title": "Gallery Page",
        "features": [
            "Visual showcase of company culture",
            "Team building activity photos",
            "Office environment imagery",
            "Event photography"
        ],
        "image": "gallery_page_1773048552742.png"
    },
    {
        "title": "Contact Page",
        "features": [
            "Direct inquiry form",
            "Physical address and location map snippet",
            "Email and telephone contact details",
            "Responsive customer service links"
        ],
        "image": "contact_page_1773141238548.png"
    },
    {
        "title": "Feedback Page",
        "features": [
            "Client testimonial submission forms",
            "User experience feedback collection",
            "Anonymous submission options (if applicable)",
            "Direct pipeline to management"
        ],
        "image": "feedback_page_1773048615358.png"
    },
    {
        "title": "Portal - Login Page",
        "features": [
            "Secure authentication gateway",
            "Role-based access control (HR vs Candidates)",
            "Password recovery functionality",
            "Clean, focused interface"
        ],
        "image": "login_page_png_1773068312302.png"
    },
    {
        "title": "Portal - Registration Page",
        "features": [
            "New candidate account creation",
            "Profile setup for job applications",
            "Data privacy consent integration",
            "Validation and secure password handling"
        ],
        "image": "register_page_png_1773068294167.png"
    },
    {
        "title": "HR Manager Dashboard",
        "features": [
            "Centralized control panel for administrators",
            "Quick actions for common tasks",
            "Overview of system health and activity",
            "Direct links to specific management modules"
        ],
        "image": "hr_dashboard_page_png_1773068402833.png"
    },
    {
        "title": "HR Analytics",
        "features": [
            "Data visualization of key HR metrics",
            "Total applications and open position tracking",
            "Time-to-hire and other performance indicators",
            "Visual charts for intuitive understanding"
        ],
        "image": "hr_analytics_page_png_1773068453586.png"
    },
    {
        "title": "All Applications List",
        "features": [
            "Comprehensive review of candidate submissions",
            "Status tracking and updating capabilities",
            "Filtering and sorting for efficient review",
            "Access to candidate resumes and details"
        ],
        "image": "all_applications_page_png_1773068491804.png"
    },
    {
        "title": "Job Applications (Specific Job)",
        "features": [
            "Filtered view of applications for a single role",
            "Comparison of candidates for the same position",
            "Bulk action capabilities (status updates)",
            "Detailed applicant data"
        ],
        "image": "job_applications_page_1773071100688.png" # Fixed
    },
    {
        "title": "Add/Edit Job Form",
        "features": [
            "Intuitive interface for creating new postings",
            "Rich text editing for job descriptions",
            "Date pickers for application deadlines",
            "Form validation to ensure complete data"
        ],
        "image": "add_job_page_1773071117476.png" # Fixed
    },
    {
        "title": "Onboarding Programs Management",
        "features": [
            "Creation and assignment of onboarding workflows",
            "Task lists for new hires",
            "Progress tracking for HR administrators",
            "Template-based program generation"
        ],
        "image": "onboarding_programs_page_png_1773068523372.png"
    },
    {
        "title": "My Onboarding (Employee View)",
        "features": [
            "Personalized checklist for new employees",
            "Task completion interactive elements",
            "Clear timeline and expectations",
            "Resource links for required reading"
        ],
        "image": "my_onboarding_page_1773071134666.png" # Fixed
    }
]

class DocTemplateWithHeaderFooter(SimpleDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        
    def addPageTemplates(self, pageTemplates):
        super().addPageTemplates(pageTemplates)

def footer(canvas, doc):
    canvas.saveState()
    # Footer
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.HexColor("#64748b")) # slate-500
    canvas.drawString(inch, 0.75 * inch, f"Strategic Synergy HR Web App Documentation - Page {doc.page}")
    canvas.drawRightString(letter[0] - inch, 0.75 * inch, datetime.now().strftime("%B %d, %Y"))
    canvas.restoreState()

# For TOC functionality, we need a custom document template to capture headings
class MyDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))

def generate_pdf():
    doc = MyDocTemplate(OUTPUT_FILE, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=28,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=20
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontName='Helvetica',
        fontSize=16,
        textColor=colors.HexColor("#334155"),
        alignment=1, # Center
        spaceAfter=30
    )

    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        textColor=colors.HexColor("#64748b"),
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor("#1e40af"),
        spaceAfter=15
    )
    
    toc_heading_style = ParagraphStyle(
        'TOCHeading',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=20,
        alignment=1
    )

    bullet_style = ParagraphStyle(
        'BulletPoint',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        spaceAfter=4
    )
    
    Story = []
    
    # Cover Page
    Story.append(Spacer(1, 2.0*inch))
    Story.append(Paragraph("Strategic Synergy HR Web App", title_style))
    Story.append(Paragraph("Client Presentation & Feature Documentation", subtitle_style))
    Story.append(Spacer(1, 0.5*inch))
    
    # Authorized recipient / Author details
    Story.append(Paragraph("Prepared For:", heading_style))
    Story.append(Paragraph("Mr. Bumhira", bullet_style))
    Story.append(Paragraph("Managing Consultant", bullet_style))
    Story.append(Paragraph("Strategic Synergy Consultancy", bullet_style))
    Story.append(Spacer(1, 0.3*inch))
    
    Story.append(Paragraph("Prepared By:", heading_style))
    Story.append(Paragraph("Mr. Mwamuka", bullet_style))
    Story.append(Paragraph("Software Engineer", bullet_style))
    Story.append(Paragraph("Secure Stack Enterprise Solutions", bullet_style))
    Story.append(Spacer(1, 0.5*inch))
    
    Story.append(Paragraph("Note: This document represents a comprehensive redesign proposal. There will be no development costs associated with this redesign.", bullet_style))
    Story.append(Spacer(1, 0.5*inch))

    current_date = datetime.now().strftime("%B %d, %Y")
    Story.append(Paragraph(f"Date: {current_date}", date_style))
    Story.append(PageBreak())
    
    # Table of Contents
    Story.append(Paragraph("Table of Contents", toc_heading_style))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(fontName='Helvetica', fontSize=12, name='TOCLevel0', leftIndent=20, firstLineIndent=-20, spaceBefore=5, leading=16),
    ]
    Story.append(toc)
    Story.append(PageBreak())
    
    # Generate pages
    for page in PAGES:
        # Title (will be caught by MyDocTemplate.afterFlowable for TOC)
        Story.append(Paragraph(page['title'], heading_style))
        Story.append(Spacer(1, 0.1*inch))
        
        # Features (Bullet Points)
        bullet_items = []
        for feature in page['features']:
            bullet_items.append(ListItem(Paragraph(feature, bullet_style), bulletColor=colors.HexColor("#3b82f6"), value='circle'))
        
        Story.append(ListFlowable(bullet_items, bulletType='bullet', start='circle', leftIndent=20))
        Story.append(Spacer(1, 0.3*inch))
        
        # Image
        img_path = os.path.join(ARTIFACT_DIR, page['image'])
        if os.path.exists(img_path):
            try:
                img = Image(img_path)
                # Max width: 6.5 inches (8.5 - 2)
                # Max height: 6.0 inches
                max_width = 6.5 * inch
                max_height = 6.0 * inch
                
                # Aspect ratio scaling
                img_width = img.drawWidth
                img_height = img.drawHeight
                
                scale = min(max_width/img_width, max_height/img_height)
                img.drawWidth = img_width * scale
                img.drawHeight = img_height * scale
                
                Story.append(img)
            except Exception as e:
                Story.append(Paragraph(f"[Error loading image: {str(e)}]", bullet_style))
        else:
            Story.append(Paragraph(f"[Image missing: {img_path}]", bullet_style))
            
        Story.append(PageBreak())

    # Build the document, calling the footer function on each page
    doc.multiBuild(Story, onFirstPage=footer, onLaterPages=footer)
    print(f"PDF generated successfully at: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_pdf()
