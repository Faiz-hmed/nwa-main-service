from dataclasses import field, fields
from unicodedata import category
from rest_framework import serializers
from .models import Article, Author, Category

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['name','publication']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['cat_name']

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    author = AuthorSerializer(many=True)

    class Meta:
        model = Article
        fields = ['id','title','time_written','category','author','article_file','article_link','images']
        depth = 1
