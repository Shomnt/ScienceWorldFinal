import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {Article} from './Article';

export default function ArticlePage() {
  const { article_id } = useParams();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/article-service/articles/${article_id}`)
      .then((res) => {
        if (!res.ok) throw new Error("Ошибка при загрузке статьи");
        return res.json();
      })
      .then((data) => {
        setArticle(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError(err);
        setLoading(false);
      });
  }, [article_id]);

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div>Ошибка: {error}</div>;
  if (!article) return <div>Статья не найдена</div>;

  return (
    <Article article={article}/>
  );
}
