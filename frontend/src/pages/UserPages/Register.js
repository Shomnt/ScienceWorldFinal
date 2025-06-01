import { useNavigate } from 'react-router-dom';
import {useEffect, useState} from "react";
import { useAuth } from "../../contexts/AuthContext";

export function Register(){
    const navigate = useNavigate();
    const { auth, login,  logout } = useAuth();

    useEffect(() => {
        if (auth.isAuthenticated) {
            navigate("/");
            window.location.reload();
        }
    }, [auth.isAuthenticated, navigate]);

    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        email: "",
        password: ""
    });

    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        setFormData(prev => ({
            ...prev,
            [e.target.name]: e.target.value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/auth-service/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            if (response.ok) {
                setMessage('Регистрация прошла успешно!');
                await login({"email":formData.email, "password":formData.password})
                setFormData({ first_name: "", last_name: "", email: "", password: "" });
                navigate("/")
                } else {
                const errorData = await response.json();
                setMessage(`Ошибка: ${errorData.detail || 'Что-то пошло не так'}`);
            }
        } catch (error) {
            setMessage('Ошибка сети. Попробуйте позже.');
            console.error(error);
        }
    };



    return(
        <div>
            <h2>Регистрация</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Имя:</label>
                    <input
                        type="text"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Фамилия:</label>
                    <input
                        type="text"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Пароль:</label>
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <button type="submit">Зарегистрироваться</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    )
}