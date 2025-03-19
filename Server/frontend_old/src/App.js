import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import { Box, Button, Heading, Text } from "@chakra-ui/react";



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
  
  const [selectedPhotos, setSelectedPhotos] = useState([]); //hold array of photo object ids to manipulate
  const [photoStates, setPhotoStates] = useState({}); //hold selected state of each photo (dict)

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

  //print currently selected photos (just for debugging purposes)
  useEffect(()=> {
    console.log(selectedPhotos)
  }, [selectedPhotos])

  //clear/init selected state when visitor images are updated
  useEffect(()=>{
    var photoStateDict = {}
    for(let i =0; i<visitors.length; i++){
      photoStateDict[visitors[i]['id']] = false
    }
    setPhotoStates(photoStateDict)
    setSelectedPhotos([])
  }, [visitors])

  const handlePhotoSelect = (photo_id) => {
    //toggle select state
    if (!photoStates[photo_id]){
      //add id to selected photos
      setSelectedPhotos([...selectedPhotos, photo_id]);
    }else{
      //remove id from selected photos
      setSelectedPhotos(selectedPhotos.filter(a => a!== photo_id));
    }
    //update photo states
    let prevState = photoStates[photo_id]
    setPhotoStates({...photoStates, [photo_id] : !prevState})
    // console.log("new state: " +  JSON.stringify(photoStates))
  };

  //Delete selected photos and rerender remaining visitor photos
  const deleteSelectedPhotos = () => {
    axios.delete('http://localhost:5002/api/delete_photos', 
      {data: selectedPhotos}, 
      {withCredentials: true }
    )
    .then(response => setVisitors(response.data)) //returns updated photos
    .catch(error => {
      console.error('Deleting photos error:', error);
    });
   
  }

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
      <p>{selectedPhotos.length} photos selected</p>
      <button onClick={deleteSelectedPhotos}>Delete selected photos from DB</button>
      <div class="faces-gallery">
            {visitors.length > 0 ? (
              visitors.map((photo, index) => (
                <Photo photo={photo} onClick={handlePhotoSelect} selectState={photoStates[photo[['id']]]} key={index}/>
              ))
            ) : (
              <p>No visitors (or unknown user).</p>
            )}
        </div>
    </div>
  );
}

//Visitor photo component
function Photo({ photo, onClick, selectState}){
  // const [selected, setSelected] = useState(false);
  // const handleClick = () => {
  //   setSelected(!selected);
  // };
  // useEffect(() => {
  //   // callback to add photo id to selectedPhotos
  //   onClick(photo['id'], selected);
  // }, [selected]);
  return (
    <div class="face-item" onClick={() => {onClick(photo['id']);}} style={{border: `3px solid ${selectState? "#6CDF80" : "white"}`}}>
        <img src={"data:image/png;base64,"+photo['data']} alt={photo['timestamp']}/>
        <p>{photo["timestamp"]}</p>
    </div>);
}

function Signup({ onSignupSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [userId, setUserId] = useState('');  // NEW: Add user ID input
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSignup = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5002/signup', { username, password, id: userId }, {
      headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
      setSuccess("Signup successful! You can now log in.");
      setError('');
      onSignupSuccess();  // Switch to login page
    })
    .catch(error => {
      if (error.response && error.response.data.error) {
        setError(error.response.data.error);
      } else {
        setError("Signup failed. Try again.");
      }
      setSuccess('');
    });
  };

  return (
    <div>
      <h1>Signup</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
      <form onSubmit={handleSignup}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Choose a unique ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          required
        />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [showSignup, setShowSignup] = useState(false);  // New: Toggle between login/signup

  useEffect(() => {
    axios.get('http://localhost:5002/check_login', { withCredentials: true })
      .then(response => {
        if (response.data.logged_in) {
          setIsLoggedIn(true);
        }
      })
      .catch(error => {
        console.error('Error checking login status:', error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    axios.post('http://localhost:5002/logout', {}, { withCredentials: true })
      .then(() => {
        setIsLoggedIn(false);
      })
      .catch(error => console.error('Logout failed:', error));
  };

  if (isLoading) {
    return <p>Loading...</p>;
  }

  return (
    <div className="App">
      {isLoggedIn ? (
        <>
          <button onClick={handleLogout}>Logout</button>
          <Dashboard />
        </>
      ) : (
        <>
          {showSignup ? (
            <>
              <Signup onSignupSuccess={() => setShowSignup(false)} />
              <p>Already have an account? <button onClick={() => setShowSignup(false)}>Login</button></p>
            </>
          ) : (
            <>
              <Login onLoginSuccess={handleLoginSuccess} />
              <p>Don't have an account? <button onClick={() => setShowSignup(true)}>Sign Up</button></p>
            </>
          )}
        </>
      )}
    </div>
  );
}

export default App;
