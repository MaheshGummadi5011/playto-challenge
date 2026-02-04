import React, { useState } from 'react';
import axios from 'axios';

// 1. The Recursive Component
const CommentNode = ({ comment, postId, onReplyAdded }) => {
  const [showReplyBox, setShowReplyBox] = useState(false);
  const [replyText, setReplyText] = useState("");

  const handleVote = async () => {
    try {
      // Calls our Concurrency-Proof API
      await axios.post('https://playto-challenge-foy8.onrender.com/api/vote/', {
        type: 'comment',
        id: comment.id
      });
      alert("Upvoted! (Refresh to see karma change)");
    } catch (err) {
      alert(err.response?.data?.error || "Error voting");
    }
  };

  const submitReply = async () => {
    try {
      await axios.post(`https://playto-challenge-foy8.onrender.com/api/posts/${postId}/comment/`, {
        content: replyText,
        parent: comment.id // Link to this comment as parent
      });
      setShowReplyBox(false);
      setReplyText("");
      onReplyAdded(); // Trigger refresh
    } catch (err) {
      alert("Failed to reply");
    }
  };

  return (
    <div className="ml-4 mt-2 border-l-2 border-gray-200 pl-4">
      {/* The Comment Content */}
      <div className="bg-gray-50 p-3 rounded shadow-sm">
        <div className="text-xs text-gray-500 font-bold mb-1">
          {comment.author_name}
        </div>
        <p className="text-gray-800">{comment.content}</p>
        
        {/* Actions */}
        <div className="mt-2 flex gap-3 text-xs">
          <button onClick={handleVote} className="text-blue-600 hover:underline">
            Like
          </button>
          <button onClick={() => setShowReplyBox(!showReplyBox)} className="text-gray-600 hover:underline">
            Reply
          </button>
        </div>

        {/* Reply Box */}
        {showReplyBox && (
          <div className="mt-2">
            <input 
              className="border p-1 text-sm w-full rounded" 
              value={replyText} 
              onChange={e => setReplyText(e.target.value)}
              placeholder="Write a reply..."
            />
            <button onClick={submitReply} className="mt-1 bg-blue-500 text-white px-2 py-1 rounded text-xs">
              Send
            </button>
          </div>
        )}
      </div>

      {/* 2. RECURSION: Render children if they exist */}
      {comment.replies && comment.replies.map(reply => (
        <CommentNode 
          key={reply.id} 
          comment={reply} 
          postId={postId} 
          onReplyAdded={onReplyAdded} 
        />
      ))}
    </div>
  );
};

export default CommentNode;