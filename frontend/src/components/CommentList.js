import React, { useEffect, useState } from "react";
import { fetchComments } from "../api/api";
import { useParams } from "react-router-dom";
import "./CommentList.css";

export default function CommentList() {
  const { threadId } = useParams();
  const [comments, setComments] = useState([]);

  useEffect(() => {
    fetchComments(threadId).then(res => setComments(res.data));
  }, [threadId]);

  return (
    <div className="commentlist-container">
      <h2 className="commentlist-title">Комментарии</h2>
      <ul className="commentlist-list">
        {comments.map(comment => (
          <li key={comment.id} className="commentlist-item">{comment.content}</li>
        ))}
      </ul>
    </div>
  );
}
