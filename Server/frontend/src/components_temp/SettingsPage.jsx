import React from "react";
import { Box, Heading, Text, VStack } from "@chakra-ui/react";

function SettingsPage() {
  return (
    <Box textAlign="center" py={10} bg="brand.beige" minH="100vh">
      <Heading color="brand.darkBlue" mb={6}>
        Settings
      </Heading>
      <VStack spacing={6} maxW="600px" mx="auto">
        <Text fontSize="lg">
          Welcome to your settings page! Here, you can manage your account preferences, update your
          profile, and adjust notifications.
        </Text>
        {/* Add additional settings options here */}
      </VStack>
    </Box>
  );
}

export default SettingsPage;
