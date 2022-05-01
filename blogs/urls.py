"""blogs package URL Configuration"""
from django.urls import path

from blogs import views

app_name = 'blogs'
urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:article_id>/', views.read_article, name='article_page'),
    path('article/write/', views.write_article, name="write_article"),
    path('article/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('article/<int:article_id>/delete', views.delete_article, name='delete_article'),
    path('me/articles/', views.authors_own_articles, name='your_articles'),
    path('search/', views.search_articles, name='search_articles'),

]
