import React, { useState, useEffect } from "react";
import { Box, Text, Heading, VStack, Image, Grid, Stack, Button } from "@chakra-ui/react";
import axios from "axios";

function Dashboard() {
  const [doorStatus, setDoorStatus] = useState(null);
  const [voiceMemos, setVoiceMemos] = useState([]);
  const [visitors, setVisitors] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5002/api/door_status", {
      withCredentials: true
    }).then((response) => setDoorStatus(response.data));
    axios.get("http://localhost:5002/api/voice_memos", {
      withCredentials: true
    }).then((response) => setVoiceMemos(response.data));
    axios.get("http://localhost:5002/api/visitors", {
      withCredentials: true
    }).then((response) => setVisitors(response.data));
  }, []);

  const handleLockToggle = () => {
    axios.post("http://localhost:5002/toggle", {'door_unlocked' : !doorStatus.door_unlocked }, {
      withCredentials: true
    });
    setDoorStatus({"door_open" : doorStatus.door_open, "door_unlocked" : !doorStatus.door_unlocked});
  }

  return (
    <VStack spacing={6} p={6} align="stretch">
      <Heading color="brand.darkBlue" textAlign="center">
        Dashboard
      </Heading>
      {doorStatus && (
        <Box p={4} borderWidth="1px" borderRadius="md" boxShadow="md" bg="white">
          <Button colorScheme="red" onClick={handleLockToggle}>
            {doorStatus.door_unlocked ? "Lock" : "Unlock"}
          </Button>
          <Text fontSize="lg">
            <strong>{doorStatus.door_unlocked ? "Door unlocked" : "Door locked"}</strong>
          </Text>
          <Text fontSize="lg">
            <strong>{doorStatus.door_open ? "Door open" : "Door closed"}</strong> 
          </Text>
        </Box>
      )}
      <Box bg="white" p={4} borderRadius="md" boxShadow="md">
        <Heading size="md" mb={4} color="brand.darkBlue">
          Voice Memos
        </Heading>
        <Stack spacing={2}>
          {voiceMemos.map((memo, index) => (
            <Text key={index}>
              {memo.timestamp}: {memo.data}
            </Text>
          ))}
        </Stack>
      </Box>
      <Box bg="white" p={4} borderRadius="md" boxShadow="md">
        <Heading size="md" mb={4} color="brand.darkBlue">
          Visitors
        </Heading>
        <Grid templateColumns="repeat(auto-fill, minmax(100px, 1fr))" gap={4}>
          {visitors.map((photo, index) => (
            <Box key={index} textAlign="center" bg="brand.beige" p={2} borderRadius="md">
              <Image src={`data:image/png;base64,${photo.data}`} alt={photo.timestamp} borderRadius="md" />
              <Text>{photo.timestamp}</Text>
            </Box>
          ))}
        </Grid>
      </Box>
    </VStack>
  );
}

export default Dashboard;
