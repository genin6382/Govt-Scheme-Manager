import React, { useState, useEffect } from 'react';
import API from '../services/api';
import { useParams, useNavigate } from 'react-router-dom';
import FeedbackList from './FeedbackList';
import FeedbackForm from './FeedbackForm';
import '../styles/SchemeDetail.css';
import '../styles/FeedbackSection.css';

const SchemeDetail = () => {
  const { id } = useParams();
  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [existingFeedback, setExistingFeedback] = useState(null);
  const [canFeedback, setCanFeedback] = useState(false);
  const [showApplyButton, setShowApplyButton] = useState(true);
  const [applicationStatus, setApplicationStatus] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    API.get(`/schemes/${id}/`)
      .then(response => {
        setScheme(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching scheme details:', error);
        setLoading(false);
      });

    API.get(`/schemes/${id}/feedbacks/`)
      .then(response => {
        const userFeedback = response.data.find(feedback => feedback.owned);
        setExistingFeedback(userFeedback);
      })
      .catch(error => {
        console.error('Error fetching feedbacks:', error);
      });

    API.get(`/schemes/${id}/can-feedback/`)
      .then(response => {
        setCanFeedback(response.data.can_feedback);
      })
      .catch(error => {
        console.error('Error fetching can feedback status:', error);
      });
    
    API.get(`/applications/check/${id}/`)
      .then(response => {
            if(response.data.status === 'approved') {
                setApplicationStatus({ message: 'Congratulations! Your application has been approved', backgroundColor: '#c3e6cb', color: '#155724' });
            }
            else if(response.data.status === 'rejected') {
                setApplicationStatus({ message: 'Sorry! Your application has been rejected', backgroundColor: '#f8d7da', color: '#721c24' });
            }
            else if(response.data.status === 'pending') {
                setApplicationStatus({ message: 'Your application is pending', backgroundColor: '#fff3cd', color: '#856404' });
            }
            else {
                setApplicationStatus(null);
            }
        setShowApplyButton(response.data.can_apply);
      })
      .catch(error => {
        console.error('Error checking application status:', error);
      });
  }, [id]);

  if (loading) return <div className="loading">Loading...</div>;

  if (!scheme) return <div className="error">Unable to load scheme details. Please try again later.</div>;

  const renderList = (text) => (
    text.split(/(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\n)\s/).filter(item => item.trim()).map((item, index) => (
      <li key={index}>{item}</li>
    ))
  );

  return (
    
    <div className="scheme-detail-container">
      {scheme.is_scheme_manager && (
        <button className="scheme-manager-actions" onClick={() => navigate(`/applications/schemes/${id}/`)}>View Applications</button>
      )
      }
      {applicationStatus && (
          <div className="application-status" style={{ padding: '10px',backgroundColor:applicationStatus.backgroundColor,color:applicationStatus.color,border: '1px solid #f5c6cb',borderRadius: '5px',fontSize: '16px',fontWeight: 'bold',textAlign: 'center',marginBottom: '20px'}}>
              <b>{applicationStatus.message}</b>
          </div>
      )}
      <h1 className="scheme-title">{scheme.scheme_name}</h1>
      <p className="scheme-summary">{scheme.summary}</p>
      <div className="scheme-details">
        {[
          { title: 'Benefits', content: scheme.benefits },
          { title: 'Eligibility Criteria', content: scheme.eligibility_criteria },
          { title: 'Application Process', content: scheme.application_process },
          { title: 'Documents Required', content: scheme.documents_required }
        ].map((section, index) => (
          <div key={index} className="scheme-section">
            <h2>{section.title}</h2>
            <ul className="scheme-list">
              {renderList(section.content)}
            </ul>
          </div>
        ))}
      </div>
      {showApplyButton && (
        <button className="apply-button" onClick={() => navigate(`/apply/${id}`)}>Apply</button>
      )}
      <div className="feedback-section">
        <h2 className="feedback-title">Client Feedback</h2>
        <div className="feedback-carousel">
          <FeedbackList schemeId={id} />
        </div>
        {canFeedback && (
          <button className="add-feedback-button" onClick={() => setShowFeedbackForm(!showFeedbackForm)}>Add Feedback</button>
        )}
        {showFeedbackForm && <FeedbackForm schemeId={id} existingFeedback={existingFeedback} />}
      </div>
    </div>
  );
};

export default SchemeDetail;
