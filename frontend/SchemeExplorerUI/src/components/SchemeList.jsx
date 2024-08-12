// src/components/SchemeList.js
import React, { useState, useEffect } from 'react';
import API from '../services/api';
import { Link } from 'react-router-dom';
import '../styles/SchemeList.css';

const SchemeList = () => {
  const [schemes, setSchemes] = useState([]);

  useEffect(() => {
    const fetchSchemes = async () => {
      try {
        const response = await API.get('/schemes/');
        const schemesData = response.data;
        setSchemes(schemesData);
      } catch (error) {
        console.error('Error fetching schemes:', error);
      }
    };

    fetchSchemes();
  }, []);

  return (
    <div className="scheme-list-container">
      <div className="scheme-list">
        <h1 className="scheme-list-title">Available Schemes</h1>
        <ul className="scheme-list-ul">
          {Array.isArray(schemes) && schemes.length > 0 ? (
            schemes.map(scheme => (
              <li key={scheme.id} className="scheme-list-item">
                <Link to={`/schemes/${scheme.id}`} className="scheme-list-link">
                  {scheme.scheme_name}
                </Link>
              </li>
            ))
          ) : (
            <li className="no-schemes">No schemes available</li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default SchemeList;
