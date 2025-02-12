import React from "react";
import { Box, Text, Heading, Flex, Button } from "@chakra-ui/react";
import lockImage from "../assets/images/lock.jpg";

function LandingPage() {
  return (
      <Flex w="100vw" h="85vh">
        {/* Left Side - Image */}
        <Box
          flex="1"
          height="100%"
          backgroundImage={`url(${lockImage})`}
          backgroundSize="cover"
          backgroundPosition="top left"
          backgroundRepeat="no-repeat"
        />

        {/* Right Side - Text Content */}
        <Box flex="1" display="flex" alignItems="center" justifyContent="center" p="6">
          <Box maxW="500px">
            <Heading fontSize="2xl" fontWeight="bold">
              Same Look, New Sound
            </Heading>
            <Text mt={2}>
              Custom 40mm titanium drivers deliver precise, expansive sound with clearer highs and richer lows so you can hear your favorite songs in a whole new way. Our signature removable magnetic ear pads are easily replaceable and provide serious sound isolation.
            </Text>
          </Box>
        </Box>
      </Flex>
  );
}

export default LandingPage;
