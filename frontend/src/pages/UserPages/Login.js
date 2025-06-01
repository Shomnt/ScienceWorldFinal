import React, {useEffect, useState} from 'react';
import {useAuth} from "../../contexts/AuthContext";
import { useNavigate } from 'react-router-dom';

export function Login() {
    const navigate = useNavigate();

    const { auth, login } = useAuth();
    const [credentials, setCredentials] = useState({ email: '', password: '' });
    const [error, setError] = useState(null);

    useEffect(() => {
        if (auth.isAuthenticated){
            navigate("/")
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(credentials);
            navigate("/")
        } catch (err) {
            setError(err.message);
        }
    };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Почта"
        value={credentials.username}
        onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
      />
      <input
        type="password"
        placeholder="Пароль"
        value={credentials.password}
        onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
      />
      <button type="submit">Войти</button>
      {error && <p>{error}</p>}
    </form>
  );
}