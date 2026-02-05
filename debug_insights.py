import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\marlv\Documents\lims\Strategic Synergy')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strategic_synergy.settings')
django.setup()

try:
    from insights import views
    print(f"Successfully imported insights.views: {views}")
    if hasattr(views, 'article_list'):
        print("article_list exists in views.")
    else:
        print("ERROR: article_list NOT found in views.")
        print(f"Dir of views: {dir(views)}")
except Exception as e:
    print(f"Import failed: {e}")
