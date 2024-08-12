import React, { useState, useEffect } from 'react';
import API from '../services/api';
import '../styles/ManageGroups.css';

const ManageGroups = () => {
  const [users, setUsers] = useState([]);
  const [username, setUsername] = useState('');

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await API.get('/users/manage-groups/');
        setUsers(response.data);
      } catch (error) {
        console.error('Failed to fetch users', error);
      }
    };
    fetchUsers();
  }, []);

  const handleAddManager = async () => {
    try {
      await API.post('/users/manage-groups/', { username });
      setUsername('');
      const response = await axios.get('/users/manage-groups/');
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to add manager', error);
    }
  };

  const handleRemoveManager = async (id) => {
    try {
      await API.delete(`/users/manage-groups/${id}`);
      const response = await axios.get('/users/manage-groups/');
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to remove manager', error);
    }
  };

  return (
    <div className="manage-groups-container">
      <h2>Manage Scheme Managers</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <button onClick={handleAddManager}>Add Manager</button>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            {user.username}
            <button onClick={() => handleRemoveManager(user.id)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ManageGroups;
