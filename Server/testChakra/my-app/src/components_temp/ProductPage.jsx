import React from "react";
import { Box, Heading, Text, Image, VStack, Grid, GridItem } from "@chakra-ui/react";

function ProductPage() {
  return (
    <Box textAlign="center" py={10} bg="brand.beige" minH="100vh">
      <Heading color="brand.darkBlue" mb={6}>
        Our Product
      </Heading>
      <Image
        src="https://via.placeholder.com/800x400?text=Locked+In+Product+Image"
        alt="Locked In Product"
        borderRadius="md"
        mx="auto"
        mb={6}
      />
      <Grid templateColumns={{ base: "1fr", md: "1fr 1fr" }} gap={6} maxW="800px" mx="auto">
        <GridItem>
          <Text fontSize="lg" fontWeight="bold">
            Advanced Facial Recognition
          </Text>
          <Text>
            Our system uses cutting-edge facial recognition to ensure that only authorized individuals gain access.
          </Text>
        </GridItem>
        <GridItem>
          <Text fontSize="lg" fontWeight="bold">
            Secure Voice Memo Alerts
          </Text>
          <Text>
            Leave secure voice memos for guests or family members that will be available upon unlocking the door.
          </Text>
        </GridItem>
        <GridItem>
          <Text fontSize="lg" fontWeight="bold">
            Remote Lock/Unlock
          </Text>
          <Text>
            Control your door remotely using our app, providing ultimate convenience and security.
          </Text>
        </GridItem>
        <GridItem>
          <Text fontSize="lg" fontWeight="bold">
            Easy Installation
          </Text>
          <Text>
            Our product is designed for easy installation, making it accessible for everyone.
          </Text>
        </GridItem>
      </Grid>
    </Box>
  );
}

export default ProductPage;
