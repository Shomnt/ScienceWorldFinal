import React, { useState } from "react";
import { createGroup } from "../api/api";
import "./CreateGroup.css";

export default function CreateGroup() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createGroup({ title, description });
      alert("Группа создана!");
      setTitle("");
      setDescription("");
    } catch (error) {
      alert("Ошибка при создании группы");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="creategroup-form">
      <h3 className="creategroup-title">Создать обсуждение</h3>
      <input
        type="text"
        placeholder="Название"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
        className="creategroup-input"
      />
      <input
        type="text"
        placeholder="Описание"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
        className="creategroup-input"
      />
      <button type="submit" className="creategroup-button">Создать</button>
    </form>
  );
}
