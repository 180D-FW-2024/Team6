import React from "react";
import { Flex, Box, Heading, Spacer, Button, HStack, Link } from "@chakra-ui/react";

function Navbar({
  isLandingPage,
  isLoggedIn,
  onLogout,
  onNavigateHome,
  onNavigateDashboard,
  onNavigateVoiceMemos,
  onNavigateVisitors,
  onNavigateProduct,
  onNavigateAbout,
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
        </HStack>
      )}

      {/* Links for About Us and Product (only on landing page) */}
      {isLandingPage && (
        <HStack spacing={6} ml={6}>
          <Link
            onClick={onNavigateProduct}
            color="white"
            fontWeight="bold"
            _hover={{ textDecoration: "underline" }}
          >
            Product
          </Link>
          <Link
            onClick={onNavigateAbout}
            color="white"
            fontWeight="bold"
            _hover={{ textDecoration: "underline" }}
          >
            About Us
          </Link>
        </HStack>
      )}

      <Spacer />

      {/* Login/Register or Logout */}
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
        <Button colorScheme="red" onClick={onLogout}>
          Logout
        </Button>
      ) : null}
    </Flex>
  );
}

export default Navbar;
