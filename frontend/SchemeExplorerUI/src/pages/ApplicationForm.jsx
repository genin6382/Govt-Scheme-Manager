import React, { useState, useContext } from 'react';
import API from '../services/api';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import '../styles/AppForm.css';

const ApplicationForm = () => {
    const { id } = useParams();
    const [documents, setDocuments] = useState([]);
    const [errors, setErrors] = useState([]);
    const navigate = useNavigate();
    const { authStatus } = useContext(AuthContext);

    const handleFileChange = (e) => {
        setDocuments(e.target.files);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrors([]);

        if (documents.length === 0) {
            setErrors(['Please upload at least one document.']);
            return;
        }

        const formData = new FormData();
        formData.append('scheme', id);
        for (let i = 0; i < documents.length; i++) {
            formData.append('documents', documents[i]);
        }

        try {
            console.log('Submitting application:', formData.get('scheme'), formData.get('documents'));
            console.log('Auth status:', authStatus);
            const response = await API.post('/applications/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                withCredentials: true,
            });

            if (response.data.status === 'rejected') {
                setErrors(response.data.validity);
            } else {

                navigate('/');
            }
        } catch (error) {
            console.error('Error submitting application:', error.response.data);
            setErrors([error.response.data.detail || 'An error occurred while submitting your application. Please try again later.']);
        }
    };

    return (
        <center>
            <div className="application-form-container">
                <h1>Apply for the Scheme</h1>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="documents">Upload Documents</label>
                        <input 
                            type="file" 
                            id="documents" 
                            onChange={handleFileChange} 
                            multiple 
                            required
                        />
                    </div>
                    <button type="submit" className="submit-button">Submit</button>
                </form>
                {errors.length > 0 && (
                    <div className="error-messages">
                        <h2>Application Rejected</h2>
                        <ul>
                            {errors.map((error, index) => (
                                <li key={index}>{error}</li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </center>
    );
};

export default ApplicationForm;
