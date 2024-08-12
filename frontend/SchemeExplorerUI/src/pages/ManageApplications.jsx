import React, { useState, useEffect } from 'react';
import API from '../services/api';
import { useNavigate, useParams } from 'react-router-dom';
import '../styles/ManageApplications.css';

const ManageApplications = () => {
    const { schemeId } = useParams();
    const [applications, setApplications] = useState([]);
    const [expandedApplication, setExpandedApplication] = useState(null);
    const [eligibilityCriteria, setEligibilityCriteria] = useState('');
    const [statusUpdates, setStatusUpdates] = useState({}); // Track status changes

    const navigate = useNavigate();

    useEffect(() => {
        const fetchApplications = async () => {
            try {
                const response = await API.get(`/applications/schemes/${schemeId}/`);
                setApplications(response.data);
            } catch (error) {
                console.error('Failed to fetch applications', error);
            }
        };

        const fetchEligibilityCriteria = async () => {
            try {
                const response = await API.get(`/schemes/${schemeId}/`);
                setEligibilityCriteria(response.data.eligibility_criteria);
            } catch (error) {
                console.error('Failed to fetch eligibility criteria', error);
            }
        };

        fetchApplications();
        fetchEligibilityCriteria();
    }, [schemeId]);

    const handleStatusChange = (id, newStatus) => {
        setStatusUpdates(prev => ({
            ...prev,
            [id]: newStatus
        }));
    };

    const saveStatusChange = async (id) => {
        const newStatus = statusUpdates[id] || applications.find(app => app.id === id).status;
        
        try {
            await API.put(`/applications/${id}/`, { status: newStatus });
            setApplications(applications.map(app =>
                app.id === id ? { ...app, status: newStatus } : app
            ));
        } catch (error) {
            console.error('Failed to update status', error);
        }
    };

    return (
        <>
            <button className="back-button" onClick={() => navigate(-1)}>◀ Back</button>
            <div className="eligibility-criteria">
                <h1>Eligibility Requirements</h1>
                <div className="criteria-content">
                    {eligibilityCriteria.split('\n').map((line, index) => (
                        <p key={index}>{line}</p>
                    ))}
                </div>
            </div>
            <div className="applications-container">
                {applications.length === 0 && <h1>No applications found</h1>}
                {applications.length > 0 &&
                    <div className="applications-list">
                        <h1>Manage Applications</h1>
                        {applications.map(app => (
                            <div key={app.id} className="application-card">
                                <div className="application-summary">
                                    <h2>{app.username}</h2>
                                    <p><strong>Scheme:</strong> {app.scheme_name}</p>
                                    <p><strong>Status:</strong> {app.status}</p>
                                    <button
                                        className="expand-button"
                                        onClick={() => setExpandedApplication(expandedApplication === app.id ? null : app.id)}
                                    >
                                        {expandedApplication === app.id ? '▲' : '▼'} Details
                                    </button>
                                </div>
                                {expandedApplication === app.id && (
                                    <div className="application-details">
                                        <h3>User Details</h3>
                                        <p><strong>Age:</strong> {app.user_details.age}</p>
                                        <p><strong>Caste:</strong> {app.user_details.caste}</p>
                                        <p><strong>Education:</strong> {app.user_details.education}</p>
                                        <p><strong>Email:</strong> {app.user_details.email}</p>
                                        <p><strong>Gender:</strong> {app.user_details.gender}</p>
                                        <p><strong>Phone:</strong> {app.user_details.phone_number}</p>
                                        <p><strong>Address:</strong> {app.user_details.recidence_district}, {app.user_details.recidence_state}</p>
                                        <p><strong>Marital Status:</strong> {app.user_details.marital_status}</p>
                                        <p><strong>Occupation:</strong> {app.user_details.occupation}</p>
                                        <p><strong>BPL Status:</strong> {app.user_details.is_bpl ? 'Yes' : 'No'}</p>
                                        <p><strong>Disabled:</strong> {app.user_details.is_disabled ? 'Yes' : 'No'}</p>
                                        <p><strong>Student:</strong> {app.user_details.is_student ? 'Yes' : 'No'}</p>
                                        <div className="status-update">
                                            <label htmlFor={`status-${app.id}`}>Update Status:</label>
                                            <select
                                                id={`status-${app.id}`}
                                                value={statusUpdates[app.id] || app.status}
                                                onChange={(e) => handleStatusChange(app.id, e.target.value)}
                                            >
                                                <option value="pending">Pending</option>
                                                <option value="approved">Approved</option>
                                                <option value="rejected">Rejected</option>
                                            </select>
                                            <button className="save-button" onClick={() => saveStatusChange(app.id)}> Save </button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                }
            </div>
        </>
    );
};

export default ManageApplications;
