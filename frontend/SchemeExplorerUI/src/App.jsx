// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import HomePage from './pages/HomePage';
import SchemePage from './pages/SchemePage';
import Register from './pages/Register';
import Profile from './pages/Profile';
import ManageGroups from './pages/ManageGroups';
import LoginPage from './pages/LoginPage';
import PrivateRoute from './components/PrivateRoute';
import ApplicationForm from './pages/ApplicationForm';
import ManageApplications from './pages/ManageApplications';
const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage/>} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/profile" element={<PrivateRoute element={Profile} />} />
          <Route path="/schemes/:id" element={<PrivateRoute element={SchemePage} />} />
          <Route path="/apply/:id" element={<PrivateRoute element={ApplicationForm} />}/>
          <Route path="/manage-groups" element={<PrivateRoute element={ManageGroups} />} />
          <Route path="/applications/schemes/:schemeId" element={<PrivateRoute element={ManageApplications}/>} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
