import React, { useState, useEffect } from "react";
import axios from "axios";
import { Box, Button, Input, Select, VStack, Text } from "@chakra-ui/react";

function VoiceMemos() {
  const [memos, setMemos] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [sortOrder, setSortOrder] = useState("newest");
  const [filteredMemos, setFilteredMemos] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5002/api/voice_memos", { withCredentials: true })
      .then((response) => {
        const formattedMemos = response.data.map(memo => ({
          content: memo.data,
          date: new Date(memo.timestamp),
        }));
        setMemos(formattedMemos);
        setFilteredMemos(formattedMemos);
      })
      .catch((error) => {
        console.error("Error fetching voice memos:", error);
      });
  }, []);

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchSubmit = () => {
    setFilteredMemos(memos.filter((memo) =>
      memo?.content?.toLowerCase().includes(searchQuery.toLowerCase())
    ));
  };

  const handleSortChange = (event) => {
    setSortOrder(event.target.value);
  };

  const sortedMemos = filteredMemos.sort((a, b) => {
    return sortOrder === "newest"
      ? b.date - a.date
      : a.date - b.date;
  });

  console.log(filteredMemos);

  return (
    <Box p={5}>
      <Text fontSize="2xl" fontWeight="bold" mb={4}>Voice Memos</Text>
      <VStack spacing={3} align="start" width="100%">
        <Input
          placeholder="Search memos..."
          value={searchQuery}
          onChange={handleSearchChange}
        />
        <Button onClick={handleSearchSubmit}>Search</Button>
        <Select value={sortOrder} onChange={handleSortChange}>
          <option value="newest">Newest First</option>
          <option value="oldest">Oldest First</option>
        </Select>
        <VStack spacing={3} width="100%">
          {sortedMemos.length > 0 ? (
            sortedMemos.map((memo, index) => (
              <Box key={index} p={4} borderWidth="1px" borderRadius="md" width="100%">
                <Text fontSize="sm" color="gray.500">{memo.date.toLocaleString()}</Text>
                <Text mt={2}>{memo.content}</Text>
              </Box>
            ))
          ) : (
            <Text>No voice memos found.</Text>
          )}
        </VStack>
      </VStack>
    </Box>
  );
}

export default VoiceMemos;
