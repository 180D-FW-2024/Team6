import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Login component
function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5002/login', 
      { username, password }, 
      { headers: { 'Content-Type': 'application/json' }, withCredentials: true }
    )
    .then(response => {
      onLoginSuccess();

    })
    .catch(error => {
      console.error('Login error:', error);
      setError('Invalid username or password');
    });
  };
  

  return (
    <div className="App">
      <h1>Login</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

// Dashboard component
function Dashboard() {
  const [doorStatus, setDoorStatus] = useState(null);
  const [voiceMemos, setVoiceMemos] = useState([]);
  const [visitors, setVisitors] = useState([]);

  useEffect(() => {
    // Fetch door status, voice memos, and visitors after login
    axios.get('http://localhost:5002/api/door_status', {
      withCredentials: true
    })
      .then(response => setDoorStatus(response.data))
      .catch(error => console.error(error));

    axios.get('http://localhost:5002/api/voice_memos', {
      withCredentials: true
    })
      .then(response => setVoiceMemos(response.data))
      .catch(error => console.error(error));

    axios.get('http://localhost:5002/api/visitors', {
      withCredentials: true
    })
      .then(response => setVisitors(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="dashboard">
      <h1>Welcome to the Dashboard</h1>
      {doorStatus && (
        <div>
          <h2>Door Status</h2>
          <p>Unlocked: {doorStatus.door_unlocked ? 'Yes' : 'No'}</p>
          <p>Open: {doorStatus.door_open ? 'Yes' : 'No'}</p>
        </div>
      )}
      
      <h2>Voice Memos</h2>
      <ul>
        {voiceMemos.map((memo, index) => (
          <li key={index}>
            {memo.timestamp}: {memo.data}
          </li>
        ))}
      </ul>

      <h2>Visitors</h2>
      <div class="faces-gallery">
            {visitors.length > 0 ? (
              visitors.map((photo) => (
                <div class="face-item">
                <img src={"data:image/png;base64,"+photo['data']} alt={photo['timestamp']}/>
                <div class="caption">
                    <p>{photo["timestamp"]}</p>
                </div>
            </div>

              ))
            ) : (
              <p>No visitors (or unknown user).</p>
            )}

        </div>
    </div>
  );
}

// Main App component
function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true); // Set logged-in state to true
  };

  return (
    <div className="App">
      {isLoggedIn ? (
        <Dashboard />
      ) : (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}

export default App;
