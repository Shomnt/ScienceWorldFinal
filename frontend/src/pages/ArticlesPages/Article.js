import React from 'react';
import './Article.css';

export function Article({ article }) {
  if (!article) {
    return <p className="article-loading">Загрузка...</p>;
  }

  return (
    <div className="article-container">
      <h1 className="article-title">{article.title}</h1>
      <p className="article-description">{article.description}</p>

      <div className="article-authors">
        <strong>Авторы:</strong>{' '}
        {article.authors_articles?.length > 0
          ? article.authors_articles
                .filter(aa => aa.author && aa.author.first_name)
                .map(aa => `${aa.author.first_name} ${aa.author.last_name}`)
                .join(', ')
          : 'Нет авторов'}
      </div>

      <div className="article-tags">
        <strong>Теги:</strong>{' '}
        {article.article_tags?.length > 0
          ? article.article_tags
                .filter(at => at.tag && at.tag.name)
                .map(at => at.tag.name)
                .join(', ')
          : 'Нет тегов'}
      </div>

      <div className="article-areas">
        <strong>Области:</strong>{' '}
        {article.article_areas?.length > 0
          ? article.article_areas
                .filter(aa => aa.area && aa.area.name)
                .map(aa => aa.area.name)
                .join(', ')
          : 'Нет областей'}
      </div>
    </div>
  );
}
