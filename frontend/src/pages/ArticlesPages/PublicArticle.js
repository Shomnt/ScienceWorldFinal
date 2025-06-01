import React, { useState } from 'react';
import axios from 'axios';
import AsyncSelect from "react-select/async";
import AsyncCreatableSelect from 'react-select/async-creatable';
import './PublicArticle.css';

const fetchOptions = async (url, inputValue) => {
  const res = await axios.get(`${url}?query=${inputValue}`);
  return res.data.map(item => ({
    value: item.id || item.name,
    label: item.name || item.title
  }));
};

export function PublicArticle(){
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [authors, setAuthors] = useState([]);
  const [tags, setTags] = useState([]);
  const [areas, setAreas] = useState([]);
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage('Пожалуйста, выберите файл');
      return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('authors', JSON.stringify(authors.map(a => a.value)));
    formData.append('tags', JSON.stringify(tags.map(t => t.label)));
    formData.append('areas', JSON.stringify(areas.map(a => a.label)));
    formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:8000/article-service/article/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setMessage('Статья успешно загружена');
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Загрузка не удалась');
    }
  };

  return (
    <div className="public-article-container">
      <h2 className="public-article-title">Опубликовать статью</h2>
      <form onSubmit={handleSubmit} className="public-article-form">
        <input
          type="text"
          placeholder="Название"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
          className="public-article-input"
        />
        <textarea
          placeholder="Описание"
          value={description}
          onChange={e => setDescription(e.target.value)}
          required
          className="public-article-textarea"
        />
        <AsyncSelect
          isMulti
          cacheOptions
          defaultOptions
          loadOptions={(input) => fetchOptions('http://localhost:8000/article-service/authors/clue', input)}
          onChange={setAuthors}
          placeholder="Выберите авторов"
          className="public-article-select"
          classNamePrefix="select"
        />
        <AsyncCreatableSelect
          isMulti
          cacheOptions
          defaultOptions
          loadOptions={(input) => fetchOptions('http://localhost:8000/article-service/tags/clue', input)}
          onChange={setTags}
          placeholder="Выберите ключевые слова"
          className="public-article-select"
          classNamePrefix="select"
        />
        <AsyncSelect
          isMulti
          cacheOptions
          defaultOptions
          loadOptions={(input) => fetchOptions('http://localhost:8000/article-service/areas/clue', input)}
          onChange={setAreas}
          placeholder="Выберите научные области"
          className="public-article-select"
          classNamePrefix="select"
        />
        <input
          type="file"
          onChange={e => setFile(e.target.files[0])}
          required
          className="public-article-file"
        />
        <button type="submit" className="public-article-button">Загрузить</button>
      </form>
      <p className="public-article-message">{message}</p>
    </div>
  );
};
