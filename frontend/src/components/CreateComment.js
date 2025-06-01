import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { createComment } from "../api/api";
import { useAuth } from "../contexts/AuthContext";
import "./CreateComment.css";

export default function CreateComment() {
  const { auth } = useAuth();
  const { threadId } = useParams();
  const [content, setContent] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createComment({
        content,
        thread_id: threadId,
        user_id: auth.user.sub,
      });
      alert("Комментарий отправлен!");
      setContent("");
    } catch (error) {
      alert("Ошибка при отправке комментария");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="createcomment-form">
      <h3 className="createcomment-title">Оставить комментарий</h3>
      <textarea
        placeholder="Комментарий"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        required
        className="createcomment-textarea"
      />
      <button type="submit" className="createcomment-button">Отправить</button>
    </form>
  );
}
