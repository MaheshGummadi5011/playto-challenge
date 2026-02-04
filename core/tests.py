from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from .models import User, Post, Vote

class LeaderboardTestCase(TestCase):
    def setUp(self):
        # Create Users
        self.user1 = User.objects.create_user(username='alice')
        self.user2 = User.objects.create_user(username='bob')
        
        # Create TWO Posts for Bob
        self.post_bob_1 = Post.objects.create(author=self.user2, content="Bob's 1st Post")
        self.post_bob_2 = Post.objects.create(author=self.user2, content="Bob's 2nd Post")
        self.post_content_type = ContentType.objects.get_for_model(Post)

    def test_leaderboard_ignores_old_votes(self):
        """
        Test that votes older than 24 hours are NOT counted in the leaderboard.
        """
        # 1. Create a "Fresh" vote on Post 1 (Should count -> 5 pts)
        Vote.objects.create(
            voter=self.user1,
            receiver=self.user2,
            content_type=self.post_content_type,
            object_id=self.post_bob_1.id,
            points=5,
            created_at=timezone.now()
        )

        # 2. Create an "Old" vote on Post 2 (Should NOT count)
        old_vote = Vote.objects.create(
            voter=self.user1,
            receiver=self.user2,
            content_type=self.post_content_type,
            object_id=self.post_bob_2.id,
            points=5
        )
        # Manually hack the timestamp to be 25 hours ago
        old_vote.created_at = timezone.now() - timedelta(hours=25)
        old_vote.save()

        # 3. Check Leaderboard
        response = self.client.get('/api/leaderboard/')
        data = response.json()

        # Bob should have 5 points (from fresh vote only), not 10
        bob_entry = next(item for item in data if item["username"] == "bob")
        self.assertEqual(bob_entry['score'], 5)