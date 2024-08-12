import React, { useState } from 'react';
import API from '../services/api';
import '../styles/FeedbackForm.css'; 

const FeedbackForm = ({ schemeId, existingFeedback }) => {
  const [comment, setComment] = useState('');
  const [rating, setRating] = useState(1); // default rating

  const handleSubmit = (e) => {
    e.preventDefault();
    API.post(`/schemes/${schemeId}/feedbacks/`, { comment, rating })
      .then(response => {
        console.log('Feedback added:', response.data);
        setComment('');
        setRating(1);
        window.location.reload();  
      })
      .catch(error => {
        console.log(comment, rating);
        console.error('Error adding feedback:', error.response.data);
      });
  };

  if (existingFeedback) {
    return null;
  }

  return (
    <form className="feedback-form" onSubmit={handleSubmit}>
      <textarea
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        placeholder="Add your feedback"
        required
      ></textarea>
      <div className="rating-input">
        <label htmlFor="rating">Rating:</label>
        <select
          id="rating"
          value={rating}
          onChange={(e) => setRating(Number(e.target.value))}
          required
        >
          {[1, 2, 3, 4, 5].map((value) => (
            <option key={value} value={value}>
              {value}
            </option>
          ))}
        </select>
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default FeedbackForm;
