import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strategic_synergy.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

def create_hr_manager():
    username = 'hr_manager'
    email = 'hr@strategicsynergy.co.zw'
    password = 'password123'
    
    if User.objects.filter(username=username).exists():
        print(f"User {username} already exists. Updating permissions...")
        user = User.objects.get(username=username)
    else:
        print(f"Creating user {username}...")
        user = User.objects.create_user(username=username, email=email, password=password)
    
    user.is_staff = True
    user.save()
    
    # Define permissions to grant
    permissions_to_grant = [
        # Careers
        'add_job', 'change_job', 'delete_job', 'view_job',
        'add_application', 'change_application', 'delete_application', 'view_application',
        # Insights
        'add_article', 'change_article', 'delete_article', 'view_article',
        'add_resource', 'change_resource', 'delete_resource', 'view_resource',
        # Events
        'add_event', 'change_event', 'delete_event', 'view_event',
        'add_registration', 'change_registration', 'delete_registration', 'view_registration',
        # Portal (Optional: allow them to manage client docs)
        'add_clientdocument', 'change_clientdocument', 'delete_clientdocument', 'view_clientdocument',
    ]
    
    perms = []
    for codename in permissions_to_grant:
        try:
            perm = Permission.objects.get(codename=codename)
            perms.append(perm)
        except Permission.DoesNotExist:
            print(f"Warning: Permission {codename} not found.")
            
    user.user_permissions.set(perms)
    user.save()
    
    print(f"Done! User '{username}' created/updated with HR permissions.")
    print(f"Login at: /admin/")
    print(f"Password: {password}")

if __name__ == "__main__":
    create_hr_manager()
