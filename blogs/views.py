"""Views of blogs package."""
import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms_fields import EditorForm
from .models import Article


# Create your views here.


def home(request):
    """Show title for each article with link."""
    articles_query = Article.objects.filter(visibility="public").order_by('-update_time')
    today_year = datetime.date.today().year
    context = {'articles': articles_query,
               'this_year': today_year}
    return render(request, 'blogs/pages/home.html', context)


@login_required
def write_article(request):
    """Article writing functionality"""
    if request.method != "POST":
        # Blank form for all request except 'POST'
        form = EditorForm()
    else:
        # Process submitted form
        form = EditorForm(data=request.POST)
        if form.is_valid():
            post_article = form.save(commit=False)
            post_article.author = request.user
            post_article.save()
            articles_query = Article.objects.filter(author=request.user)
            article_id = 0
            for last_article in articles_query:
                article_id = last_article.id
            return redirect('blogs:article_page', article_id=article_id)
    # Display the blank form
    context = {'writing_form': form}
    return render(request, 'blogs/article/write.html', context)


def read_article(request, article_id):
    """Article reading page"""
    try:
        article_query = Article.objects.get(id=article_id)
        more_articles_query = Article.objects.filter(author=article_query.author.id,
                                                     visibility="public").order_by('-update_time')[:5]
        today_year = datetime.date.today().year
        share_text = article_share_text(request, article_query)
        context = {
            'the_article': article_query,
            'articles': more_articles_query,
            'this_year': today_year,
            'article_share_text': share_text
        }
        if article_query.visibility == 'private':
            """Only author can access to his/her private article"""
            if article_query.author != request.user:
                data = {}
                return render(request, 'blogs/article/410_error.html', data)
            else:
                return render(request, 'blogs/article/read.html', context)
        else:
            """If the article is public..."""
            return render(request, 'blogs/article/read.html', context)
    except Article.DoesNotExist:
        data = {}
        return render(request, 'blogs/article/410_error.html', data)


def edit_article(request, article_id):
    """Article editing functionality"""
    article_query = Article.objects.get(id=article_id)
    check_auth(request, article_query)
    if request.method != 'POST':
        # Pre-fill form for all request except 'POST'
        form = EditorForm(instance=article_query)
    else:
        # Process submitted form
        form = EditorForm(instance=article_query, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:article_page', article_id=article_id)
    # Show pre-fill form
    context = {'article': article_query, 'editor_form': form}
    return render(request, 'blogs/article/edit.html', context)


def delete_article(request, article_id):
    """Article deleting functionality"""
    try:
        article_query = Article.objects.get(id=article_id)
        check_auth(request, article_query)
        if request.method == 'GET':
            article_query.delete()
            return redirect('blogs:your_articles')
    except Article.DoesNotExist:
        raise Http404


def check_auth(request, the_article):
    if request.user != the_article.author:
        raise Http404


@login_required
def authors_own_articles(request):
    """Private article's page for each author.
    Where their private articles will be listed."""
    private_articles_query = Article.objects.filter(author=request.user, visibility="private") \
        .order_by("-update_time")
    public_articles_query = Article.objects.filter(author=request.user, visibility="public") \
        .order_by("-update_time")
    today_year = datetime.date.today().year
    context = {'private_articles': private_articles_query,
               'public_articles': public_articles_query,
               'this_year': today_year}
    return render(request, 'blogs/pages/your_articles.html', context)


def article_share_text(request, article_query):
    """Article sharing caption/text will be different for Author & Reader"""
    if article_query.author == request.user:
        share_text = 'I just published ' + article_query.title + ' ' + str(request.build_absolute_uri())
    else:
        share_text = article_query.title + ' by @' + str(article_query.author) + ' ' \
                     + str(request.build_absolute_uri())
    return share_text


def search_articles(request):
    """People's Article searching functionality"""
    today_year = datetime.date.today().year
    latest_articles = Article.objects.filter(visibility='public').order_by('-id')
    if request.method == 'POST':
        query_text = request.POST.get('query', None).strip()
        if query_text is not None:
            by_title = Article.objects.filter(visibility='public',
                                              title__icontains=query_text).order_by('-update_time')
            found_articles = by_title
            if len(by_title) < 10:
                by_text = Article.objects.filter(visibility='public',
                                                 text__icontains=query_text).order_by('-update_time')
                found_articles = by_text

            results = found_articles
            context = {'search_results': results,
                       'query_text': query_text,
                       'this_year': today_year,
                       }
            return render(request, 'blogs/pages/search_articles.html', context)
    else:
        context = {'latest_articles': latest_articles}
        return render(request, 'blogs/pages/search_articles.html', context)
