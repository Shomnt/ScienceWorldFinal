import React, { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext({
    auth: { isAuthenticated: false, user: null },
    setAuth: () => {},
    login: async () => {},
    logout: () => {},
});

export function AuthProvider({ children }) {
    const [auth, setAuth] = useState({ isAuthenticated: false, user: null });
    const checkAuth = async () => {
        const token = localStorage.getItem('token');
        try {
            const res = await fetch('http://localhost:8000/auth-service/user/check', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (!res.ok) {
                return { isAuthenticated: false, user: null };
            }
            const data = await res.json();
            return { isAuthenticated: true, user: data.user };
        } catch {
            return { isAuthenticated: false, user: null };
        }
    };

    useEffect(() => {
        const fetchAuth = async () => {
            const result = await checkAuth();
            setAuth(result);
        };
        void fetchAuth();
        }, []);

    const login = async (credentials) => {
        const res = await fetch('http://localhost:8000/auth-service/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(credentials),
        });
        if (!res.ok) {
            throw new Error('Неверные данные для входа');
        }
        const data = await res.json();

        localStorage.setItem('token', data.token);

        const authData = await checkAuth();
        setAuth(authData);
    };
    const logout = () => {
        localStorage.removeItem('token');
        setAuth({ isAuthenticated: false, user: null });
    };

    return (
        <AuthContext.Provider value={{ auth, setAuth, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}
