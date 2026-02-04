# Engineering Challenge - Explainer

## 1. The Tree (Handling Nested Comments)
**Constraint:** Avoid the "N+1 Problem" when loading nested threads.
**Solution:** I implemented a **Flat-Fetch + In-Memory Reconstruction** strategy.
* Instead of recursive queries, I fetch `Comment.objects.filter(post=obj)` in one go.
* I rebuild the tree structure in Python using a hash map (O(N) complexity).
* **Result:** A thread with 100 comments loads in 1 SQL query, not 101.

## 2. The Math (Leaderboard Aggregation)
**Constraint:** Calculate leaderboard based strictly on Karma earned in the last 24 hours.
**Solution:** I used Django's conditional aggregation on the fly.
* **Code:** `Sum('votes_received__points', filter=Q(created_at__gte=last_24h))`
* **Why:** This ensures data is always fresh and avoids race conditions found in caching.

## 3. The Concurrency (The Like Button)
**Constraint:** Prevent users from double-voting.
**Solution:** I used `transaction.atomic()` and a Database Unique Constraint (`unique_together`).
* If two requests hit at the exact same millisecond, the database itself rejects the second one, ensuring data integrity.