from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import User, Post, Comment, Vote

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'content', 'parent', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author_name', 'content', 'created_at', 'likes_count']

    def get_likes_count(self, obj):
        # FIX: We query the Vote table directly
        # Find votes where the "content_type" is Post and "object_id" is this post's ID
        return Vote.objects.filter(
            content_type__model='post', 
            object_id=obj.id
        ).count()

class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author_name', 'content', 'created_at', 'likes_count', 'comments']

    def get_likes_count(self, obj):
        # FIX: Same fix here for the detail view
        return Vote.objects.filter(
            content_type__model='post', 
            object_id=obj.id
        ).count()

    def get_comments(self, obj):
        # The N+1 Fix (Flat fetch)
        comments = Comment.objects.filter(post=obj).select_related('author').order_by('created_at')
        data = CommentSerializer(comments, many=True).data

        # Build tree in memory
        comment_map = {item['id']: {**item, 'replies': []} for item in data}
        roots = []

        for item in data:
            comment_id = item['id']
            parent_id = item['parent']
            node = comment_map[comment_id]

            if parent_id:
                if parent_id in comment_map:
                    comment_map[parent_id]['replies'].append(node)
            else:
                roots.append(node)
                
        return roots