from django.urls import path
# We import 'vote' (the function) instead of 'CastVoteView' (the old class)
from .views import PostListView, PostDetailView, CommentCreateView, vote, LeaderboardView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', CommentCreateView.as_view(), name='create-comment'),
    
    # This is the line that fixed the error:
    path('vote/', vote, name='vote'),  
    
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]