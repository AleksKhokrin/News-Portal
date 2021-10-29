import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField("рейтинг автора", default=0)

    def __str__(self):
        
        return f'{self.authorUser.username}'

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.authorRating = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    categoryName = models.CharField('Topic', max_length=64, unique=True)

    def __str__(self):
        
        return f'{self.categoryName.title()}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORIES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]
    categoryType = models.CharField(max_length=2,
                                     choices=CATEGORIES,
                                     default=ARTICLE)
    pubDate = models.DateTimeField('Publication date ', auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='postCategory')
    postTitle = models.CharField('Title ', max_length=128)
    postText = models.TextField('Text')
    rating = models.SmallIntegerField("рейтинг статьи/новости", default=0)

    
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

   
    def preview(self):
        return f'{self.postText[:124]} ...'

    def __str__(self):
        
        return f'{self.postTitle}. {self.postText[:124]} ...'

    def get_absolute_url(self):
        
        return f'/news/{self.id}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
       
        return f'{self.postThrough}. {self.categoryThrough}'



class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.CharField('текст комментария', max_length=200)
    pubDate = models.DateTimeField('дата и время публикации комментария', auto_now_add=True)
    rating = models.SmallIntegerField("рейтинг комментария", default=0)

    
    def __str__(self):
        
        return f'{self.commentUser.username}'

   
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
