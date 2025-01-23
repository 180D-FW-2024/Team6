// src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [doorStatus, setDoorStatus] = useState(null);
  const [voiceMemos, setVoiceMemos] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5002/api/door_status')
    .then(response => {
      console.log('Door status response:', response.data);
      setDoorStatus(response.data);
    })
      .catch(error => console.error('Error fetching door status:', error));
  }, []);
  
  useEffect(() => {
    axios.get('http://localhost:5002/api/voice_memos')
      .then(response => {
        console.log('Voice memos response:', response.data);
        setVoiceMemos(response.data);
      })
      .catch(error => console.error('Error fetching voice memos:', error));
  }, []);

  return (
    <div className="App">
      <h1>Door Access Control</h1>

      {/* Display door status */}
      {doorStatus ? (
        <div>
          <h2>Door Status: {doorStatus.door_unlocked ? 'Unlocked' : 'Locked'}</h2>
          <h3>Door Open: {doorStatus.door_open ? 'Yes' : 'No'}</h3>
        </div>
      ) : (
        <p>Loading door status...</p>
      )}

      {/* Display voice memos */}
      <h2>Voice Memos</h2>
      <ul>
        {voiceMemos.length > 0 ? (
          voiceMemos.map((memo, index) => (
            <li key={index}>{memo.Timestamp}: {memo.Memo}</li>
          ))
        ) : (
          <p>No voice memos available.</p>
        )}
      </ul>
    </div>
  );
}

export default App;
