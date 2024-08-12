import React, { useState, useEffect } from 'react';
import API from '../services/api';
import '../styles/FeedbackList.css';

const FeedbackList = ({ schemeId }) => {
  const [feedbacks, setFeedbacks] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [editingFeedback, setEditingFeedback] = useState(null);
  const [editComment, setEditComment] = useState('');

  const maleAvatar = 'https://img.freepik.com/free-psd/3d-illustration-human-avatar-profile_23-2150671142.jpg?size=338&ext=jpg&ga=GA1.1.2008272138.1722643200&semt=ais_hybrid_1_2008272138&mt=HYBR-TL-ais_hybrid_1_2008272138&tl=1&rf=2008272138';
  const femaleAvatar = 'https://img.freepik.com/free-psd/3d-illustration-with-online-avatar_23-2151303063.jpg?size=338&ext=jpg&ga=GA1.1.2008272138.1722643200&semt=ais_hybrid_1_2008272138&mt=HYBR-TL-ais_hybrid_1_2008272138&tl=1&rf=2008272138';
  const transAvatar = 'https://www.shutterstock.com/image-illustration/business-woman-icon-isolated-on-260nw-1905216310.jpg';

  useEffect(() => {
    API.get(`/schemes/${schemeId}/feedbacks/`)
      .then(response => {
        console.log('Feedbacks fetched:', response.data);
        setFeedbacks(response.data);
      })
      .catch(error => {
        console.error('Error fetching feedbacks:', error);
      });
  }, [schemeId]);

  const handleEdit = (feedback) => {
    setEditingFeedback(feedback);
    setEditComment(feedback.comment);
  };

  const handleEditSubmit = (feedbackId) => {
    API.put(`/feedbacks/${feedbackId}/`, { comment: editComment })
      .then(response => {
        setFeedbacks(feedbacks.map(f => (f.id === feedbackId ? response.data : f)));
        setEditingFeedback(null);
        setEditComment('');
      })
      .catch(error => {
        console.error('Error editing feedback:', error);
      });
  };

  const handleDelete = (feedbackId) => {
    API.delete(`/feedbacks/${feedbackId}/`)
      .then(response => {
        setFeedbacks(feedbacks.filter(feedback => feedback.id !== feedbackId));
      })
      .catch(error => {
        console.error('Error deleting feedback:', error);
      });
  };

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % feedbacks.length);
  };

  const handlePrev = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + feedbacks.length) % feedbacks.length);
  };

  if (!feedbacks.length) {
    return <p>No feedbacks available for this scheme.</p>;
  }

  const getAvatar = (gender) => {
    if (gender === 'male') return maleAvatar;
    else if (gender === 'female') return femaleAvatar;
    else if (gender === 'transgender') return transAvatar;
    else return maleAvatar;
  };

  const getStar = (rating) => {
    let stars = [];
    for (let i = 0; i < rating; i++) {
      stars.push("⭐");
    }
    return stars;
  };

  const feedback = feedbacks[currentIndex];

  return (
    <div className="feedback-carousel">
      <div className="feedback-card">
        <div className="flex-container">
          <img src={getAvatar(feedback.gender)} alt="User Avatar" />
          <p>{getStar(feedback.rating)}</p>
        </div>
        <div className="feedback-content">
          {editingFeedback && editingFeedback.id === feedback.id ? (
            <>
              <textarea
                value={editComment}
                onChange={(e) => setEditComment(e.target.value)}
              />
              <button onClick={() => handleEditSubmit(feedback.id)}>Submit</button>
              <button onClick={() => setEditingFeedback(null)}>Cancel</button>
            </>
          ) : (
            <>
              <p className="feedback-author">{feedback.username}</p>
              <blockquote>{feedback.feedback}</blockquote>
            </>
          )}
        </div>
        {feedback.owned && (
          <div className="feedback-actions">
            <button onClick={() => handleEdit(feedback)}>Edit</button>
            <button onClick={() => handleDelete(feedback.id)}>Delete</button>
          </div>
        )}
      </div>
      <div className="carousel-buttons">
        <button onClick={handlePrev}>&lt;</button>
        <button onClick={handleNext}>&gt;</button>
      </div>
    </div>
  );
};

export default FeedbackList;
