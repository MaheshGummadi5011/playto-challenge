from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import SessionAuthentication
from django.db.models import Sum, Q
from django.db import transaction, IntegrityError
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404  # Essential for fetching objects safely

from .models import Post, Comment, Vote, User
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer

# --- THE FIX: Custom Authentication that ignores CSRF ---
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Do nothing! (Bypasses the check)

# 1. The Feed
class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def perform_create(self, serializer):
        # Fallback to guest if anonymous
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user, _ = User.objects.get_or_create(username='guest')
        serializer.save(author=user)

# 2. Post Detail
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [CsrfExemptSessionAuthentication]

# 3. Create Comment
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    # Allow ANYONE to comment (even guests) to make the demo smooth
    permission_classes = [] 
    authentication_classes = [CsrfExemptSessionAuthentication]

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        
        # Handle Guest User for Comments
        if self.request.user.is_authenticated:
            author = self.request.user
        else:
            author, _ = User.objects.get_or_create(username='guest')
            
        serializer.save(author=author, post=post)

# 4. The Vote Button (Concurrency Fix + Guest Support + Receiver Fix)
@api_view(['POST'])
def vote(request):
    try:
        # 1. HANDLE THE USER
        if request.user.is_authenticated:
            voter = request.user
        else:
            voter, created = User.objects.get_or_create(username='guest')
            
        # 2. GET DATA
        # Support both naming conventions for safety
        content_type_str = request.data.get('content_type') or request.data.get('type')
        object_id = request.data.get('object_id') or request.data.get('id')
        
        # 3. IDENTIFY OBJECT & OWNER (The Fix for NULL constraint)
        if content_type_str == 'post':
            target_obj = get_object_or_404(Post, pk=object_id)
            content_type = ContentType.objects.get_for_model(Post)
            points = 5
        elif content_type_str == 'comment':
            target_obj = get_object_or_404(Comment, pk=object_id)
            content_type = ContentType.objects.get_for_model(Comment)
            points = 1
        else:
            return Response({'error': 'Invalid type'}, status=400)

        # 4. SAVE VOTE
        # We MUST include 'receiver' in defaults so the DB knows who gets the points
        vote_obj, created = Vote.objects.get_or_create(
            voter=voter,
            content_type=content_type,
            object_id=object_id,
            defaults={
                'points': points,
                'receiver': target_obj.author  # <--- Essential Line
            }
        )
        
        if not created:
            return Response({'message': 'Already voted'}, status=200)

        return Response({'message': 'Vote counted'}, status=201)

    except Exception as e:
        return Response({'error': str(e)}, status=400)

# 5. The Leaderboard
class LeaderboardView(views.APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def get(self, request):
        last_24h = timezone.now() - timedelta(hours=24)
        
        leaders = User.objects.annotate(
            recent_karma=Sum(
                'votes_received__points', 
                filter=Q(votes_received__created_at__gte=last_24h)
            )
        ).exclude(recent_karma__isnull=True).order_by('-recent_karma')[:5]
        
        data = [
            {"username": u.username, "score": u.recent_karma} 
            for u in leaders
        ]
        return Response(data)