// src/pages/HomePage.jsx
import React from 'react';
import SchemeList from '../components/SchemeList';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import ThemeToggle from '../components/ThemeToggle';
import '../styles/Home.css';
const HomePage = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await API.post('/users/logout/', {}, { withCredentials: true });
      navigate('/login');
    } catch (error) {
      console.error('Logout failed', error);
    }
  };

  return (
    <>
       <button className="profile-button" onClick={()=>{navigate('/profile')}}>Profile</button>
       <div className="toggle-mode" >
        <ThemeToggle></ThemeToggle>
        <button className="logout-button" onClick={handleLogout}>Logout</button>
       </div>
       <div className="home-container">
          <h1>Welcome to the Scheme Portal</h1>
          <SchemeList />    
          
      </div>
    </>
    
  );
};

export default HomePage;
