from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class User(AbstractUser):
    # We inherit from AbstractUser to keep standard fields (username, password)
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Adjacency List: A comment points to its parent (if it's a reply)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes_cast')
    
    # Optimization: Store who RECEIVED the vote here. 
    # This allows us to calculate the leaderboard without complex joins.
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes_received')
    
    # Generic Relation: Links to EITHER a Post OR a Comment
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # 5 for Post, 1 for Comment
    points = models.IntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # CONCURRENCY FIX: 
        # A user can only vote on a specific object once. 
        # The database enforces this, preventing race conditions.
        unique_together = ('voter', 'content_type', 'object_id')
        
        indexes = [
            # Index for the leaderboard time-window query
            models.Index(fields=['created_at', 'receiver']),
        ]