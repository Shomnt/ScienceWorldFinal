import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { createThread } from "../api/api";
import "./CreateThread.css";

export default function CreateThread() {
  const { groupId } = useParams();
  const [title, setTitle] = useState("");
  const [startMessage, setStartMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createThread({ title, start_message: startMessage, group_id: groupId });
      alert("Тред создан!");
      setTitle("");
      setStartMessage("");
    } catch (error) {
      alert("Ошибка при создании треда");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="createthread-form">
      <h3 className="createthread-title">Создать тред</h3>
      <input
        type="text"
        placeholder="Заголовок"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
        className="createthread-input"
      />
      <textarea
        placeholder="Первое сообщение"
        value={startMessage}
        onChange={(e) => setStartMessage(e.target.value)}
        required
        className="createthread-textarea"
      />
      <button type="submit" className="createthread-button">Создать</button>
    </form>
  );
}
