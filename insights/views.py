from django.shortcuts import render, get_object_or_404
from .models import Article

def article_list(request):
    # Retrieve all published articles
    articles = Article.objects.filter(is_published=True)
    featured_article = articles.first() # Simplification for now
    recent_articles = articles[1:] if articles.count() > 1 else []
    
    context = {
        'featured_article': featured_article,
        'recent_articles': recent_articles,
        'articles': articles # Fallback if we want just a list
    }
    return render(request, 'insights/article_list.html', context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    related_articles = Article.objects.filter(category=article.category).exclude(id=article.id)[:3]
    return render(request, 'insights/article_detail.html', {'article': article, 'related_articles': related_articles})

from .models import Resource

def resource_list(request):
    resources = Resource.objects.filter(is_public=True)
    return render(request, 'insights/resource_list.html', {'resources': resources})
