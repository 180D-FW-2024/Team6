import React from "react";
import { Flex, Box, Heading, Spacer, Button, HStack, Link, Text } from "@chakra-ui/react";

function Navbar({
  isLandingPage,
  isLoggedIn,
  userName,
  onLogout,
  onNavigateHome,
  onNavigateDashboard,
  onNavigateSettings,
  onNavigateVoiceMemos,
  onNavigateVisitors,
  onNavigateResidents,
  onLoginClick,
  onSignupClick,
}) {
  return (
    <Flex
      as="nav"
      alignItems="center"
      bg="brand.darkBlue"
      color="white"
      padding="1rem"
    >
      {/* Logo / Home or Dashboard */}
      <Box
        cursor="pointer"
        onClick={isLoggedIn ? onNavigateDashboard : onNavigateHome}
      >
        <Heading size="md" _hover={{ textDecoration: "underline" }}>
          Locked In
        </Heading>
      </Box>

      {/* Links for Voice Memos and Visitors (only when logged in) */}
      {isLoggedIn && (
        <HStack spacing={6} ml={6}>
          <Link
            onClick={onNavigateVoiceMemos}
            color="white"
            fontWeight="bold"
            _hover={{ textDecoration: "underline" }}
          >
            Voice Memos
          </Link>
          <Link
            onClick={onNavigateVisitors}
            color="white"
            fontWeight="bold"
            _hover={{ textDecoration: "underline" }}
          >
            Visitors
          </Link>
          <Link
            onClick={onNavigateResidents}
            color="white"
            fontWeight="bold"
            _hover={{ textDecoration: "underline" }}
          >
            Manage Residents
          </Link>
        </HStack>
      )}

      <Spacer />

      {/* Login/Register or Logout with User Name */}
      {isLandingPage ? (
        <HStack spacing={4}>
          <Button
            variant="outline"
            color="white"
            borderColor="white"
            onClick={onLoginClick}
          >
            Login
          </Button>
          <Button colorScheme="teal" onClick={onSignupClick}>
            Register
          </Button>
        </HStack>
      ) : isLoggedIn ? (
        <HStack spacing={4}>
          <Text
            as="button"
            onClick={onNavigateSettings}
            fontWeight="bold"
            color="white"
            _hover={{ textDecoration: "underline", cursor: "pointer" }}
          >
            {userName}
          </Text>
          <Button colorScheme="red" onClick={onLogout}>
            Logout
          </Button>
        </HStack>
      ) : null}
    </Flex>
  );
}

export default Navbar;
