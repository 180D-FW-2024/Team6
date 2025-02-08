import React, { useState, useEffect } from "react";
import { Box, Text, Heading, VStack, Image, Grid, Stack } from "@chakra-ui/react";
import axios from "axios";

function Dashboard() {
  const [doorStatus, setDoorStatus] = useState(null);
  const [voiceMemos, setVoiceMemos] = useState([]);
  const [visitors, setVisitors] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5002/api/door_status").then((response) => setDoorStatus(response.data));
    axios.get("http://localhost:5002/api/voice_memos").then((response) => setVoiceMemos(response.data));
    axios.get("http://localhost:5002/api/visitors").then((response) => setVisitors(response.data));
  }, []);

  return (
    <VStack spacing={6} p={6} align="stretch">
      <Heading color="brand.darkBlue" textAlign="center">
        Dashboard
      </Heading>
      {doorStatus && (
        <Box p={4} borderWidth="1px" borderRadius="md" boxShadow="md" bg="white">
          <Text fontSize="lg">
            <strong>Door Unlocked:</strong> {doorStatus.door_unlocked ? "Yes" : "No"}
          </Text>
          <Text fontSize="lg">
            <strong>Door Open:</strong> {doorStatus.door_open ? "Yes" : "No"}
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
