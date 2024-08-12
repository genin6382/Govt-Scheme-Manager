// src/pages/LoginPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import '../styles/Login.css';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
  
    try {
      const response = await API.post('/users/login/', { username, password }, {
        headers: {
          'Content-Type': 'application/json',
          withCredentials: true,
        },
      });

      console.log(response, response.status);
      if (response.status === 200) {
        navigate('/');
      } else {
        alert('Login failed');
      }
    } catch (error) {
      console.error('Login failed', error);
      alert('Login failed');
    }
  };
  
  

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
      <p>Dont have an account? <a href="/register">Register</a></p>
    </div>
  );
};

export default LoginPage;
