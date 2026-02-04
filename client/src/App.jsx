import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CommentNode from './CommentNode';

// --- DELETE THIS LINE TO PREVENT CORS ERRORS ---
// axios.defaults.withCredentials = true; 

function App() {
  const [posts, setPosts] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [expandedPostId, setExpandedPostId] = useState(null);
  const [postComments, setPostComments] = useState([]);

  // Use your Live Render Backend URL
  const API_BASE = 'https://playto-challenge-foy8.onrender.com/api';

  const fetchPosts = async () => {
    try {
      const res = await axios.get(`${API_BASE}/posts/`);
      setPosts(res.data);
    } catch (err) {
      console.error("Error fetching posts:", err);
    }
  };

  const fetchLeaderboard = async () => {
    try {
      const res = await axios.get(`${API_BASE}/leaderboard/`);
      setLeaderboard(res.data);
    } catch (err) {
      console.error("Error fetching leaderboard:", err);
    }
  };

  // --- THE FIX FOR VOTING ---
  const handlePostVote = async (postId) => {
    try {
      // 1. Send the correct payload matching your Backend
      await axios.post(`${API_BASE}/vote/`, {
        type: 'post',  // MUST be 'post' (singular)
        id: postId     // The ID of the post
      });
      
      // 2. Refresh data to show new score immediately
      fetchPosts();
      fetchLeaderboard();
      
      // Optional: Nice feedback
      // alert("Upvoted Post!"); 
    } catch (err) {
      console.error("Voting failed:", err);
      alert("Error voting. Check console.");
    }
  };

  const loadComments = async (postId) => {
    if (expandedPostId === postId) {
      setExpandedPostId(null);
      return;
    }
    try {
      const res = await axios.get(`${API_BASE}/posts/${postId}/`);
      setPostComments(res.data.comments);
      setExpandedPostId(postId);
    } catch (err) {
      console.error("Error loading comments:", err);
    }
  };

  useEffect(() => {
    fetchPosts();
    fetchLeaderboard();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8 flex gap-8 flex-col md:flex-row">
      {/* Feed Section */}
      <div className="flex-1 max-w-2xl">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">Community Feed</h1>
        {posts.map(post => (
          <div key={post.id} className="bg-white p-6 rounded-lg shadow mb-4">
            <h2 className="font-bold text-lg text-blue-900">{post.author_name || 'Anonymous'}</h2>
            <p className="text-gray-700 mt-2">{post.content}</p>
            
            <div className="mt-4 flex items-center gap-4 text-sm text-gray-500">
              {/* Like Button */}
              <button 
                onClick={() => handlePostVote(post.id)}
                className="text-blue-600 font-bold hover:bg-blue-50 px-3 py-1 rounded transition"
              >
                👍 Like ({post.likes_count})
              </button>

              {/* Toggle Comments */}
              <button 
                onClick={() => loadComments(post.id)}
                className="text-gray-600 hover:text-gray-900"
              >
                {expandedPostId === post.id ? "Hide Comments" : "Show Comments"}
              </button>
            </div>

            {/* Nested Comments Section */}
            {expandedPostId === post.id && (
              <div className="mt-4 border-t pt-4 bg-gray-50 p-4 rounded-b-lg">
                {postComments.map(c => (
                  <CommentNode 
                    key={c.id} 
                    comment={c} 
                    postId={post.id} 
                    onReplyAdded={() => loadComments(post.id)} 
                  />
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Leaderboard Section */}
      <div className="w-full md:w-80">
        <div className="bg-white p-6 rounded-lg shadow sticky top-8 border-t-4 border-blue-500">
          <h2 className="text-xl font-bold mb-4 border-b pb-2">🏆 Leaderboard (24h)</h2>
          {leaderboard.length === 0 ? (
            <p className="text-gray-500 text-sm">No active users today.</p>
          ) : (
            <ul>
              {leaderboard.map((user, idx) => (
                <li key={idx} className="flex justify-between py-2 border-b last:border-0">
                  <span className="font-medium text-gray-700">
                    {idx + 1}. {user.username}
                  </span>
                  <span className="font-bold text-blue-600">
                    {user.score} pts
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;