import React, { useState, useEffect, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ThemeContext } from '../context/ThemeContext';
import API from '../services/api';
import '../styles/Profile.css';

const STATES = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 
  'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 
  'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 
  'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 
  'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 
  'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli', 
  'Daman and Diu', 'Lakshadweep', 'Delhi', 'Puducherry'
];

const genderOptions = [
  { id: 'male', name: 'Male' },
  { id: 'female', name: 'Female' },
  { id: 'transgender', name: 'Transgender' }
];

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [updatedProfile, setUpdatedProfile] = useState({});
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { theme } = useContext(ThemeContext);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await API.get('/users/profile/');
        setProfile(response.data);
      } catch (error) {
        console.error('Failed to fetch profile', error);
      }
    };
    fetchProfile();
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setUpdatedProfile({ ...updatedProfile, [name]: type === "checkbox" ? checked : value });
  };

  const handleUpdate = async () => {
    try {
      const response = await API.post('/users/profile/', updatedProfile);
      setProfile(response.data);
      setMessage("Profile updated successfully!");
      setError("");
    } catch (error) {
      console.error('Failed to update profile', error);
      setError(error.response?.data?.non_field_errors?.[0] || "Failed to update profile");
      setMessage("");
    }
  };

  const handleDelete = async () => {
    try {
      await API.delete('/users/profile/');
      setProfile(null);
      setMessage("Profile deleted successfully!");
      setError("");
      navigate('/login');
    } 
    catch (error) {
      console.error('Failed to delete profile', error);
      setError("Failed to delete profile");
      setMessage("");
    }
  };

  return (
    <div className={`profile-container ${theme}`}>
      <Link to="/" className="back-link">Home</Link>
      {message && <div className="success-message">{message}</div>}
      {error && <div className="error-message">{error}</div>}
          {profile ? (
              <div className="profile-card">
                <h2>Profile</h2>
                <p><strong>Username:</strong> {profile.username}</p>
                <p><strong>Email:</strong> {profile.email}</p>

                <form className="profile-form">
                  <label>
                    Gender:
                    <select name="gender" defaultValue={profile.gender} onChange={handleChange}>
                      {genderOptions.map((option) => (
                        <option key={option.id} value={option.id}>{option.name}</option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Residence State:
                    <select name="recidence_state" defaultValue={profile.recidence_state} onChange={handleChange}>
                      {STATES.map((state, index) => (
                        <option key={index} value={state}>{state}</option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Residence District:
                    <input type="text" name="recidence_district" defaultValue={profile.recidence_district} onChange={handleChange} />
                  </label>
                  <label>
                    Caste:
                    <input type="text" name="caste" defaultValue={profile.caste} onChange={handleChange} />
                  </label>
                  <label>
                    Education:
                    <input type="text" name="education" defaultValue={profile.education} onChange={handleChange} />
                  </label>
                  <label>
                    Occupation:
                    <input type="text" name="occupation" defaultValue={profile.occupation} onChange={handleChange} />
                  </label>
                  <label>
                    Age:
                    <input type="number" name="age" defaultValue={profile.age} onChange={handleChange} />
                  </label>
                  <label>
                    Phone Number:
                    <input type="text" name="phone_number" defaultValue={profile.phone_number} onChange={handleChange} />
                  </label>
                  <label>
                    Marital Status:
                    <input type="text" name="marital_status" defaultValue={profile.marital_status} onChange={handleChange} />
                  </label>
                  <label className="checkbox-label">
                    Below Poverty Line:
                    <input type="checkbox" name="is_bpl" defaultChecked={profile.is_bpl} onChange={handleChange} />
                  </label>
                  <label className="checkbox-label">
                    Student:
                    <input type="checkbox" name="is_student" defaultChecked={profile.is_student} onChange={handleChange} />
                  </label>
                  <label className="checkbox-label">
                    Disabled:
                    <input type="checkbox" name="is_disabled" defaultChecked={profile.is_disabled} onChange={handleChange} />
                  </label>

                  <div className="profile-buttons">
                    <button type="button" onClick={handleUpdate}>Save</button>
                    <button type="button" className="delete-button" onClick={handleDelete}>Delete</button>
                  </div>
                </form>
              </div>
          ) : (
            <p>No profile found</p>
          )}
    </div>

  );
};

export default Profile;
