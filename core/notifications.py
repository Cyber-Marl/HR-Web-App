"""
Email notification utilities for Strategic Synergy HR Web App.
Uses Django's send_mail — console backend in dev, SMTP in production.
"""
from django.core.mail import send_mail
from django.conf import settings


def send_application_confirmation(application):
    """Send confirmation email to applicant after submitting."""
    try:
        subject = f"Application Received — {application.job.title}"
        message = (
            f"Dear {application.full_name},\n\n"
            f"Thank you for applying for the position of {application.job.title} "
            f"at Strategic Synergy Consultancy.\n\n"
            f"We have received your application and our HR team will review it shortly. "
            f"You will be notified of any updates to your application status.\n\n"
            f"Position: {application.job.title}\n"
            f"Location: {application.job.location}\n"
            f"Application Date: {application.applied_at.strftime('%B %d, %Y')}\n\n"
            f"Best regards,\n"
            f"Strategic Synergy HR Team"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [application.email],
            fail_silently=True,
        )
    except Exception:
        pass  # Don't break the flow if email fails


def send_status_change_notification(application, old_status):
    """Notify applicant when their application status changes."""
    try:
        status_display = dict(application.STATUS_CHOICES).get(application.status, application.status)
        subject = f"Application Update — {application.job.title}"
        message = (
            f"Dear {application.full_name},\n\n"
            f"Your application for {application.job.title} has been updated.\n\n"
            f"New Status: {status_display}\n\n"
        )

        if application.status == 'INTERVIEW':
            message += "Congratulations! We'd like to invite you for an interview. Our team will reach out with scheduling details soon.\n\n"
        elif application.status == 'HIRED':
            message += "Congratulations! We're thrilled to welcome you to the Strategic Synergy team! You will receive onboarding information shortly.\n\n"
        elif application.status == 'REJECTED':
            message += "After careful consideration, we've decided to move forward with other candidates. We appreciate your interest and encourage you to apply for future openings.\n\n"

        message += "Best regards,\nStrategic Synergy HR Team"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [application.email],
            fail_silently=True,
        )
    except Exception:
        pass


def send_event_registration_confirmation(registration):
    """Send confirmation email after event registration."""
    try:
        event = registration.event
        subject = f"Registration Confirmed — {event.title}"
        message = (
            f"Dear {registration.name},\n\n"
            f"You have successfully registered for:\n\n"
            f"Event: {event.title}\n"
            f"Date: {event.start_time.strftime('%B %d, %Y at %I:%M %p')}\n"
            f"Location: {event.location}\n"
        )

        if event.meeting_link:
            message += f"Meeting Link: {event.meeting_link}\n"

        message += (
            f"\nWe look forward to seeing you there!\n\n"
            f"Best regards,\n"
            f"Strategic Synergy Events Team"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [registration.email],
            fail_silently=True,
        )
    except Exception:
        pass


def send_new_job_notification(job):
    """Notify active newsletter subscribers about a new job posting."""
    try:
        from core.models import NewsletterSubscriber

        subscribers = NewsletterSubscriber.objects.filter(is_active=True).values_list('email', flat=True)
        if not subscribers:
            return

        subject = f"New Opportunity — {job.title}"
        message = (
            f"A new position has been posted at Strategic Synergy Consultancy!\n\n"
            f"Position: {job.title}\n"
            f"Location: {job.location}\n"
            f"Type: {job.get_job_type_display()}\n"
        )

        if job.salary_range:
            message += f"Salary Range: {job.salary_range}\n"

        if job.deadline:
            message += f"Application Deadline: {job.deadline.strftime('%B %d, %Y')}\n"

        message += (
            f"\nVisit our careers page to learn more and apply.\n\n"
            f"Best regards,\n"
            f"Strategic Synergy HR Team\n\n"
            f"—\n"
            f"You're receiving this because you subscribed to our newsletter."
        )

        for email in subscribers:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
    except Exception:
        pass
