from django.db import models
from django.db.models import *
from django.db import *
from . constants import *
# Create your models here.

class User(models.Model):
    name = models.CharField(
        max_length=100
    )
    
    profile_pic = models.URLField(
        default=''
    )
    
    def __str__(self):
        return self.name
        
class Group(models.Model):
    name = models.CharField(
        max_length = 100
    )
    
    members = models.ManyToManyField(
        User, 
        through = 'Membership'
    )
    
    def __str__(self):
        return self.name
    
class Membership(models.Model):
    
    group = models.ForeignKey(
        Group, 
        on_delete = models.CASCADE
    )
    
    member = models.ForeignKey(
        User, 
        on_delete = models.CASCADE
    )
    
    is_admin = models.BooleanField(
        default = False
    )

    
class Post(models.Model):
    
    content = models.CharField(
        max_length = 1000
    )
    
    posted_at = models.DateTimeField(
        auto_now = True
    )
    
    posted_by = models.ForeignKey(
        User, 
        on_delete = models.CASCADE, 
        related_name = 'posts'
    )
    
    group = models.ForeignKey(
        Group, 
        on_delete = models.CASCADE, 
        null = True
    )
    
   
class Comment(models.Model):
    content = models.CharField(
        max_length = 1000
    )
    
    commented_at = models.DateTimeField(
        auto_now = True
    )
    
    commented_by = models.ForeignKey(
        User, 
        on_delete = models.CASCADE, 
        related_name = 'comments'
    )
    
    post = models.ForeignKey(
        Post, 
        on_delete = models.CASCADE, 
        related_name = 'comments'
    )
    
    parent_comment = models.ForeignKey(
        'self', 
        on_delete = models.CASCADE, 
        null = True
    )
    
    
class Reaction(models.Model):
    
    post = models.ForeignKey(
        Post, 
        on_delete = models.CASCADE, 
        null = True, 
        blank = True, 
        related_name = 'reactions'
    )
    
    comment = models.ForeignKey(
        Comment, 
        on_delete = models.CASCADE, 
        null = True, 
        blank = True, 
        related_name = 'reactions'
    )
    
    reaction = models.CharField(
        choices = [(react.value, react.name) for react in ReactionEnum], 
        max_length = 100
    )
    
    reacted_at = models.DateTimeField(
        auto_now = True
    )
    
    reacted_by = models.ForeignKey(
        User, 
        on_delete = models.CASCADE
    )
    
    def __str__(self):
        return self.reaction
        
