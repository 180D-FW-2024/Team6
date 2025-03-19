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
              Locked In: The Future of Smart Security
            </Heading>
            <Text mt={2}>
              Revolutionizing home security with AI-driven intelligence and seamless access control.
            </Text>
            <Text mt={4}>
              Traditional locks are outdated. Locked In is an all-in-one front door security system that combines facial 
              recognition, speech recording, and door position monitoring for enhanced safety and convenience.
            </Text>
            <Text mt={4} fontWeight="semibold">Why Locked In?</Text>
            <Text mt={2}>
              - Hands-Free, Keyless Entry <br />
              - Real-Time Security Alerts <br />
              - Voice Memo Integration <br />
              - Plug & Play Installation  <br />
              - Cloud-Connected Control 
            </Text>
            <Text mt={4} fontWeight="semibold">
              Upgrade your home security today—because peace of mind should be effortless.
            </Text>
          </Box>
        </Box>
      </Flex>
  );
}

export default LandingPage;
