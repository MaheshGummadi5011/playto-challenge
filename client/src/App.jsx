import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CommentNode from './CommentNode';

// Ensure cookies are sent with requests
axios.defaults.withCredentials = true;

function App() {
  const [posts, setPosts] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [expandedPostId, setExpandedPostId] = useState(null);
  const [postComments, setPostComments] = useState([]);

  const fetchPosts = async () => {
    const res = await axios.get('https://playto-challenge-foy8.onrender.com/api/posts/');
    setPosts(res.data);
  };

  const fetchLeaderboard = async () => {
    const res = await axios.get('https://playto-challenge-foy8.onrender.com/api/leaderboard/');
    setLeaderboard(res.data);
  };

  // NEW: Function to handle liking a POST
  const handlePostVote = async (postId) => {
    try {
      await axios.post('https://playto-challenge-foy8.onrender.com/api/vote/', {
        type: 'post',
        id: postId
      });
      // Refresh data to show new score
      fetchPosts();
      fetchLeaderboard();
      alert("Upvoted Post!");
    } catch (err) {
      alert(err.response?.data?.error || "Error voting");
    }
  };

  const loadComments = async (postId) => {
    if (expandedPostId === postId) {
      setExpandedPostId(null);
      return;
    }
    const res = await axios.get(`https://playto-challenge-foy8.onrender.com/api/posts/${postId}/`);
    setPostComments(res.data.comments);
    setExpandedPostId(postId);
  };

  useEffect(() => {
    fetchPosts();
    fetchLeaderboard();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8 flex gap-8">
      {/* Feed */}
      <div className="flex-1 max-w-2xl">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">Community Feed</h1>
        {posts.map(post => (
          <div key={post.id} className="bg-white p-6 rounded-lg shadow mb-4">
            <h2 className="font-bold text-lg">{post.author_name}</h2>
            <p className="text-gray-700 mt-2">{post.content}</p>
            
            <div className="mt-4 flex items-center gap-4 text-sm text-gray-500">
              {/* NEW: The Like Button */}
              <button 
                onClick={() => handlePostVote(post.id)}
                className="text-blue-600 font-bold hover:underline"
              >
                Like ({post.likes_count})
              </button>

              <button 
                onClick={() => loadComments(post.id)}
                className="text-gray-600 hover:underline"
              >
                {expandedPostId === post.id ? "Hide Comments" : "Show Comments"}
              </button>
            </div>

            {expandedPostId === post.id && (
              <div className="mt-4 border-t pt-4">
                {postComments.map(c => (
                  <CommentNode 
                    key={c.id} 
                    comment={c} 
                    postId={post.id} 
                    onReplyAdded={() => loadComments(post.id)} // Refresh comments on reply
                  />
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Leaderboard */}
      <div className="w-80">
        <div className="bg-white p-6 rounded-lg shadow sticky top-8">
          <h2 className="text-xl font-bold mb-4 border-b pb-2">🏆 Leaderboard (24h)</h2>
          <ul>
            {leaderboard.map((user, idx) => (
              <li key={idx} className="flex justify-between py-2 border-b last:border-0">
                <span className="font-medium text-gray-700">{idx + 1}. {user.username}</span>
                <span className="font-bold text-blue-600">{user.score} pts</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;