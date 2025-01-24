// src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import "./App.css";

function App() {
  const [doorStatus, setDoorStatus] = useState(null);
  const [voiceMemos, setVoiceMemos] = useState([]);

  const [userName, setUserName] = useState("");
  const [visitors, setVisitors] = useState([]);

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

  // Retrieve images for current user
  useEffect(() => {
    axios.get('http://localhost:5002/api/visitors', {params: {userName: userName}} )
      .then(response => {
        console.log(`Visitors recieved (${response.data.length} images)`);
        setVisitors(response.data);
      })
      .catch(error => console.error('Error fetching visitor images:', error));
  }, [userName]);


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

      {/*Display visitor images of a particular user*/}
      <p>For testing db w/out proper login:</p>
      <input
          type="text"
          className="input-box"
          placeholder="ex: person a"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
        />
        <p>Username : {userName}</p>
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

export default App;
