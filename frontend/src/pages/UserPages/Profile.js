import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

export function Profile() {
    const { userId } = useParams();
    const { auth } = useAuth();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchUser() {
            try {
                const response = await fetch(`http://localhost:8000/auth-service/user/profile/${userId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        ...(auth.token && { 'Authorization': `Bearer ${auth.token}` }),
                    },
                });

                if (!response.ok) {
                    throw new Error('Ошибка при загрузке профиля');
                }

                const data = await response.json();
                setUser(data);
            } catch (error) {
                console.error('Ошибка:', error);
                setUser(null);
            } finally {
                setLoading(false);
            }
        }

        void fetchUser();
    }, [userId, auth.token]);

    if (loading) return <p>Загрузка...</p>;
    if (!user) return <p>Пользователь не найден</p>;

    return (
        <div>
            <h1>Профиль пользователя</h1>
            <p><strong>Имя:</strong> {user.first_name} {user.last_name}</p>
            <p><strong>Email:</strong> {user.email}</p>
        </div>
    );
}
