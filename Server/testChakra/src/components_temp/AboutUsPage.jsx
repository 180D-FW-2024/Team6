import React from "react";
import { Box, Heading, Text, VStack } from "@chakra-ui/react";

function AboutUsPage() {
  return (
    <Box textAlign="center" py={10} bg="brand.beige" minH="100vh">
      <Heading color="brand.darkBlue" mb={6}>
        About Us
      </Heading>
      <VStack spacing={6} maxW="800px" mx="auto">
        <Text fontSize="lg">
          Locked In is a cutting-edge technology company dedicated to revolutionizing home security. 
        </Text>
        <Text fontSize="lg">
          Our mission is to provide the most secure, innovative, and user-friendly smart door lock system. 
          By leveraging advanced technology like facial recognition and voice memos, we ensure the safety 
          and convenience of your household.
        </Text>
        <Text fontSize="lg">
          Founded in 2025, our team of experienced engineers and security experts is passionate about 
          creating solutions that make life easier and safer.
        </Text>
      </VStack>
    </Box>
  );
}

export default AboutUsPage;
