from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.db.models import Sum, Q
from django.db import transaction, IntegrityError
from django.utils import timezone
from datetime import timedelta

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
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# 2. Post Detail
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# 3. Create Comment
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    # Apply the fix here too, just in case
    authentication_classes = [CsrfExemptSessionAuthentication]

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)

# 4. The Vote Button (Concurrency Fix)
class CastVoteView(views.APIView):
    permission_classes = [IsAuthenticated]
    # We explicitly tell this view to use our "Unsafe" authentication
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        user = request.user
        obj_type = request.data.get('type')
        obj_id = request.data.get('id')
        
        if obj_type not in ['post', 'comment']:
            return Response({"error": "Invalid type"}, status=400)
        
        model = Post if obj_type == 'post' else Comment
        points = 5 if obj_type == 'post' else 1

        try:
            target_obj = model.objects.get(id=obj_id)
        except model.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        try:
            with transaction.atomic():
                Vote.objects.create(
                    voter=user,
                    receiver=target_obj.author,
                    content_object=target_obj,
                    points=points
                )
            return Response({"message": "Vote cast!", "points": points}, status=201)
            
        except IntegrityError:
            return Response({"error": "You already liked this."}, status=400)

# 5. The Leaderboard
class LeaderboardView(views.APIView):
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