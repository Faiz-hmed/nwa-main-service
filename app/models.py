from django.utils import timezone
from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.TextField()
    time_written = models.DateTimeField(default=timezone.now)
    category = models.ManyToManyField('Category')
    author = models.ManyToManyField('Author')

    article_file = models.FileField(upload_to="articles/%Y/%m/%d/")
    article_link = models.URLField(max_length=400)
    reading_time = models.IntegerField(null=True)

    def __str___(self):
        return self.title

class Category(models.Model):
    cat_name = models.CharField(max_length=128)

class User(models.Model):
    user = models.OneToOneField('auth.User',primary_key=True,on_delete=models.CASCADE)

    interaction = models.ManyToManyField(Article, through='Interactions')
 
    def __str__(self):
        return self.user.username


class Interactions(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    time_seen = models.IntegerField(null=True)
    def __str__(self) -> str:
        return "{}, {}, for: {} mins".format(self.article.title,self.user.fname+" "+self.user.lname, self.time_seen)


class Article_Images(models.Model):
    article = models.ForeignKey(Article,related_name= 'images', on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to="article_images/%Y/%m/%d/")
    

class Author(models.Model):
    name = models.CharField(max_length=32)
    pub_choices = [
        ('cnn','CNN'),
        ('fox','Fox News'),
        ('HT','Hindustan Times'),
        ('TOI','Times Of India')
    ]
    publication = models.CharField(choices=pub_choices,max_length=32)

    def __str__(self) -> str:
        return self.name