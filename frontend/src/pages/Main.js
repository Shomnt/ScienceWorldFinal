import React, { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import './Main.css';

export function Main() {
  const [searchParams] = useSearchParams();
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedArea, setSelectedArea] = useState('');
  const [sortBy, setSortBy] = useState('rating');

  const areasList = ['Physics', 'Mathematics', 'Biology', 'Chemistry'];

  // Получаем query из URL при монтировании
  useEffect(() => {
    const queryFromUrl = searchParams.get('query') || '';
    setSearchQuery(queryFromUrl);
  }, [searchParams]);

  useEffect(() => {
    const getArticles = async () => {
      setLoading(true);

      const params = new URLSearchParams();

      if (searchQuery) params.append('query', searchQuery);
      if (selectedArea) params.append('areas', selectedArea);
      if (sortBy) params.append('sort_by', sortBy);

      const url = `http://localhost:8000/article-service/articles?${params.toString()}`;

      try {
        const res = await fetch(url);
        if (!res.ok) {
          setArticles([]);
        } else {
          const data = await res.json();
          setArticles(data);
        }
      } catch (error) {
        console.error('Ошибка загрузки статей:', error);
        setArticles([]);
      }

      setLoading(false);
    };

    void getArticles();
  }, [searchQuery, selectedArea, sortBy]);

  return (
    <div className="main-container">
      <h1 className="main-title">Лента статей</h1>

      {/* Фильтры */}
      <div className="filters">
        <select
          value={selectedArea}
          onChange={(e) => setSelectedArea(e.target.value)}
          className="area-select"
        >
          <option value="">Все области</option>
          {areasList.map(area => (
            <option key={area} value={area}>{area}</option>
          ))}
        </select>

        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="sort-select"
        >
          <option value="rating">По рейтингу</option>
          <option value="title">По названию</option>
        </select>
      </div>

      {/* Результаты */}
      {loading ? (
        <p className="loading-message">Загрузка...</p>
      ) : articles.length === 0 ? (
        <p className="empty-message">Статей не найдено.</p>
      ) : (
        <ul className="article-list">
          {articles.map(article => (
            <li key={article.id} className="article-item">
              <h2 className="article-title">
                <Link to={`/article/${article.id}`} className="article-link">{article.title}</Link>
              </h2>
              <p className="article-description">{article.description}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
