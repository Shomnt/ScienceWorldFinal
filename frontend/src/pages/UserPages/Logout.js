import React, { useEffect } from 'react';
import {useAuth} from "../../contexts/AuthContext";
import { useNavigate } from 'react-router-dom';

export function Logout() {
  const { auth, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (auth.isAuthenticated) {
        logout();
    }
    navigate('/login');
  }, []);

  return <p>Выход из аккаунта...</p>;
}
