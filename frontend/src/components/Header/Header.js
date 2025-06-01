import React, {useState} from 'react';
import styles from './Header.module.css';
import {Link, useNavigate} from 'react-router-dom';
import {useAuth} from "../../contexts/AuthContext";

function Header() {
    const {auth} = useAuth()
    const [searchQuery, setSearchQuery] = useState('');
    const navigate = useNavigate();

    const handleSearch = (e) => {
        e.preventDefault();
        if (searchQuery.trim()) {
            navigate(`/?query=${encodeURIComponent(searchQuery.trim())}`);
            setSearchQuery('');
        }
    };

    return (
        <header className={styles.header}>
            <nav className={styles.nav}>
                <Link to="/" className={styles.button}>Главная</Link>
                <Link to="/discussions/" className={styles.button}>Обсуждения</Link>
                <Link to="/public" className={styles.button}>Опубликовать статью</Link>
            </nav>

            <form onSubmit={handleSearch} className={styles.searchForm}>
                <input
                    type="text"
                    placeholder="Поиск статей..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className={styles.searchInput}
                />
                <button type="submit" className={styles.button}>🔍</button>
            </form>

            <div className={styles.nav}>
                {auth.isAuthenticated ? (
                    <>
                        <button className={styles.button}>Уведомления</button>
                        <Link to={`/profile/${auth.user.sub}`} className={styles.button}>Профиль</Link>
                        <Link to="/logout" className={styles.button}>Выйти</Link>
                    </>
                ) : (
                    <>
                        <Link to="/login" className={styles.button}>Войти</Link>
                        <Link to="/register" className={styles.button}>Зарегистрироваться</Link>
                    </>
                )}
            </div>
        </header>
    );
}

export default Header;
