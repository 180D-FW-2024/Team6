import { Box, Button, Input, Heading, Text, Alert, AlertIcon, VStack, Image, Grid, Stack } from "@chakra-ui/react";
import axios from 'axios';
import './App.css';
import { useState, useEffect } from 'react';

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
    <Box maxW="400px" mx="auto" mt="50px" p="6" borderWidth="1px" borderRadius="lg" boxShadow="lg">
      <Heading mb={4} textAlign="center">Login</Heading>
      {error && (
        <Alert status="error" mb={4}>
          <AlertIcon />
          {error}
        </Alert>
      )}
      <VStack spacing={3} as="form" onSubmit={handleLogin}>
        <Input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
        <Input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <Button type="submit" colorScheme="blue" width="full">Login</Button>
      </VStack>
    </Box>
  );
}

function Signup({ onSignupSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [userId, setUserId] = useState('');
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
      onSignupSuccess();
    })
    .catch(error => {
      setError(error.response?.data.error || "Signup failed. Try again.");
      setSuccess('');
    });
  };

  return (
    <Box maxW="400px" mx="auto" mt="50px" p="6" borderWidth="1px" borderRadius="lg" boxShadow="lg">
      <Heading mb={4} textAlign="center">Signup</Heading>
      {error && (
        <Alert status="error" mb={4}>
          <AlertIcon />
          {error}
        </Alert>
      )}
      {success && (
        <Alert status="success" mb={4}>
          <AlertIcon />
          {success}
        </Alert>
      )}
      <VStack spacing={3} as="form" onSubmit={handleSignup}>
        <Input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
        <Input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <Input placeholder="Choose a unique ID" type="number" value={userId} onChange={(e) => setUserId(e.target.value)} required />
        <Button type="submit" colorScheme="green" width="full">Sign Up</Button>
      </VStack>
    </Box>
  );
}



function Dashboard() {
  const [doorStatus, setDoorStatus] = useState(null);
  const [voiceMemos, setVoiceMemos] = useState([]);
  const [visitors, setVisitors] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5002/api/door_status', { withCredentials: true })
      .then(response => setDoorStatus(response.data))
      .catch(error => console.error(error));

    axios.get('http://localhost:5002/api/voice_memos', { withCredentials: true })
      .then(response => setVoiceMemos(response.data))
      .catch(error => console.error(error));

    axios.get('http://localhost:5002/api/visitors', { withCredentials: true })
      .then(response => setVisitors(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <VStack spacing={6} p={6}>
      <Heading>Dashboard</Heading>
      {doorStatus && (
        <Box p={4} borderWidth="1px" borderRadius="md" boxShadow="md">
          <Text fontSize="lg"><strong>Door Unlocked:</strong> {doorStatus.door_unlocked ? 'Yes' : 'No'}</Text>
          <Text fontSize="lg"><strong>Door Open:</strong> {doorStatus.door_open ? 'Yes' : 'No'}</Text>
        </Box>
      )}

      <Heading size="md">Voice Memos</Heading>
      <Stack spacing={2}>
        {voiceMemos.map((memo, index) => (
          <Text key={index}>{memo.timestamp}: {memo.data}</Text>
        ))}
      </Stack>

      <Heading size="md">Visitors</Heading>
      <Grid templateColumns="repeat(auto-fill, minmax(100px, 1fr))" gap={4}>
        {visitors.map((photo, index) => (
          <Box key={index} border="2px solid" borderColor="gray.200" borderRadius="md" p={2} textAlign="center">
            <Image src={`data:image/png;base64,${photo.data}`} alt={photo.timestamp} borderRadius="md" />
            <Text>{photo.timestamp}</Text>
          </Box>
        ))}
      </Grid>
    </VStack>
  );
}


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  return (
    <Box p={6}>
      {isLoggedIn ? (
        <>
          <Button colorScheme="red" onClick={() => setIsLoggedIn(false)}>Logout</Button>
          <Dashboard />
        </>
      ) : showSignup ? (
        <>
          <Signup onSignupSuccess={() => setShowSignup(false)} />
          <Text textAlign="center">Already have an account? <Button variant="link" onClick={() => setShowSignup(false)}>Login</Button></Text>
        </>
      ) : (
        <>
          <Login onLoginSuccess={() => setIsLoggedIn(true)} />
          <Text textAlign="center">Don't have an account? <Button variant="link" onClick={() => setShowSignup(true)}>Sign Up</Button></Text>
        </>
      )}
    </Box>
  );
}

export default App;