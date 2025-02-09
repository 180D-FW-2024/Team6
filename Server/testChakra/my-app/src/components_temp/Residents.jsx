import React, { useState, useEffect } from "react";
import axios from "axios";
import { Box, Heading, VStack, HStack, Text, Grid, Image, Button, Spacer } from "@chakra-ui/react";

function Residents() {
  const [residents, setResidents] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5002/api/residents", { withCredentials: true })
      .then((response) => {setResidents(response.data); console.log(typeof(residents))})
      .catch((error) => { console.error("Error fetching residents:", error);});
  }, []);

  const handleResidentDelete = (name) => {
    // TODO
    console.log("deleting: " + name);
  };


  return (
 <Box p={5}>
      <Text fontSize="2xl" fontWeight="bold" mb={4}>Residents</Text>
      <VStack spacing={3} align="start" width="100%">
        {residents.map((resident, index) => (
        <Box key={index} bg="white" p={4} borderRadius="md" width="100%">
            <HStack>
                <Heading size="md" mb={4} color="brand.darkBlue">
                    {resident.name}
                </Heading>
                <Spacer />
                <Button colorScheme="red" onClick={() => {handleResidentDelete(resident.name)}}>Delete resident(To do)</Button>
            </HStack>
            <Grid templateColumns="repeat(auto-fill, minmax(100px, 1fr))" gap={4}>
                {resident.images.map((photo, index) => (
                <Box key={index} textAlign="center" bg="brand.beige" borderRadius="md">
                    <Image src={`data:image/png;base64,${photo}`} borderRadius="md" />
                </Box>
                ))}
            </Grid>
            </Box>
        ))}

    </VStack>
    </Box>

  );
}

export default Residents;
