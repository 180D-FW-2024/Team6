import React from "react";
import { Box, Button, Heading, Text, VStack, Image } from "@chakra-ui/react";

function LandingPage({ onLoginClick, onSignupClick, onNavigateProduct, onNavigateAbout }) {
  return (
    <Box textAlign="center" py={10} bg="brand.beige" minH="100vh">
      {/* Navbar */}
      <Box>
        <Heading color="brand.darkBlue">Locked In</Heading>
      </Box>

      <Box maxW="600px" mx="auto" mb={6}>
        {/* Replace this with a product image */}
        <Image
          src="https://via.placeholder.com/600x300?text=Locked+In+Product+Image"
          alt="Locked In Product"
          borderRadius="md"
        />
      </Box>

      <VStack spacing={4} mb={6}>
        <Text fontSize="xl" fontWeight="bold">
          Welcome to the future of smart door access.
        </Text>
        <Text>- Advanced Facial Recognition</Text>
        <Text>- Secure Voice Memo Alerts</Text>
        <Text>- Remote Lock/Unlock</Text>
      </VStack>

      <Button colorScheme="teal" size="lg" onClick={onNavigateProduct}>
        Learn More About Our Product
      </Button>
    </Box>
  );
}

export default LandingPage;
