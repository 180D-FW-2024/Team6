import React, { useState, useEffect } from "react";
import axios from "axios";
import { Box, Button, Input, Select, VStack, Text, Image, SimpleGrid, CloseButton, Spacer, HStack } from "@chakra-ui/react";

function Visitors() {
  const [visitors, setVisitors] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [sortOrder, setSortOrder] = useState("newest");
  const [filteredVisitors, setFilteredVisitors] = useState([]);
  const [rerender, setRerender] = useState(false);

  // Fetch visitors from API
  useEffect(() => {
    axios.get("http://localhost:5002/api/visitors", { withCredentials: true })
      .then((response) => {
        const formattedVisitors = response.data.map(visitor => ({
          imageSrc: `data:image/jpeg;base64,${visitor.data}`, // Base64 image
          date: new Date(visitor.timestamp),
          id: visitor.id
        }));
        setVisitors(formattedVisitors);
        setFilteredVisitors(formattedVisitors);
      })
      .catch((error) => {
        console.error("Error fetching visitors:", error);
      });
  }, [rerender]);

  // Handle search filter
  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchSubmit = () => {
    setFilteredVisitors(visitors.filter(visitor =>
      visitor.date.toLocaleString().includes(searchQuery)
    ));
  };

  // Handle sorting order
  const handleSortChange = (event) => {
    setSortOrder(event.target.value);
  };

  // Handle individual image deletion
  const handleImageDelete = (image_id) => {
    // console.log("deleting: " + image_id);
    axios.post('http://localhost:5002/api/delete_photo', 
      {image_id : image_id}, { withCredentials: true }
    )
    .then(() => {setRerender(!rerender)})
    .catch(error => {
      console.error('Deleting image error:', error);
    });
  };


  const sortedVisitors = filteredVisitors.sort((a, b) => {
    return sortOrder === "newest"
      ? b.date - a.date
      : a.date - b.date;
  });

  return (
    <Box p={5}>
      <Text fontSize="2xl" fontWeight="bold" mb={4}>Visitors</Text>
      <VStack spacing={3} align="start" width="100%">
        <Input
          placeholder="Search by date (e.g., 2025-02-08)"
          value={searchQuery}
          onChange={handleSearchChange}
        />
        <Button onClick={handleSearchSubmit}>Search</Button>
        <Select value={sortOrder} onChange={handleSortChange}>
          <option value="newest">Newest First</option>
          <option value="oldest">Oldest First</option>
        </Select>
      </VStack>
      <SimpleGrid columns={[2, 3, 5]} spacing={4} mt={5}>
        {sortedVisitors.length > 0 ? (
          sortedVisitors.map((visitor, index) => (
            <Box key={index} p={2} borderWidth="1px" borderRadius="md" boxShadow="md" _hover={{p: "0"}}>
              <HStack>
                <Spacer/>
                <CloseButton variant="outline" color="red" onClick={() => {handleImageDelete(visitor.id)}}/>
              </HStack>
              <Image src={visitor.imageSrc} alt={`Visitor ${index}`} borderRadius="md" />
              <Text fontSize="sm" color="gray.500" textAlign="center">{visitor.date.toLocaleString()}</Text>
            </Box>
          ))
        ) : (
          <Text>No visitors found.</Text>
        )}
      </SimpleGrid>
    </Box>
  );
}

export default Visitors;
