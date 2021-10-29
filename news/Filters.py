from django_filters import FilterSet, CharFilter, ModelChoiceFilter, \
    DateFromToRangeFilter  
from .models import Author, Category, Post, PostCategory, Comment

from django.contrib.auth.models import User


class PostFilter(FilterSet):
    pubDate = DateFromToRangeFilter(label='Dates From To Range')

    
    class Meta:
        model = Post
        
        fields = {
           
            'postTitle': ['icontains'],  
            'author': ['exact'],  
        }
