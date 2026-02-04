from django.urls import path
from .views import PostListView, PostDetailView, CommentCreateView, CastVoteView, LeaderboardView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comment/', CommentCreateView.as_view(), name='create-comment'),
    path('vote/', CastVoteView.as_view(), name='cast-vote'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]