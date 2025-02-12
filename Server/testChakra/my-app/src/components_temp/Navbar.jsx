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
  onNavigateProduct,
  onNavigateAbout,
  onNavigateResidents,
  onLoginClick,
  onSignupClick,
  currentPage,
}) {
  return (
    <Flex
      as="nav"
      alignItems="center"
      bg="brand.darkBlue"
      color="white"
      padding="1rem"
      minHeight="75px" // Set a fixed minimum height
    >
      {/* Logo */}
      <Box
        cursor="pointer"
        onClick={isLoggedIn ? onNavigateDashboard : onNavigateHome}
      >
        <Heading size="md" _hover={{ textDecoration: "underline" }}>
          Locked In
        </Heading>
      </Box>

      {/* Links for "About Us" and "Product" (Landing, Product, About pages) */}
      {(!isLoggedIn || currentPage === "landing" || currentPage === "product" || currentPage === "about") && (
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

      {/* ✅ Fixed Navbar Width & Buttons Section */}
      <Box minW="250px" display="flex" justifyContent="flex-end">
        {isLoggedIn ? (
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
        ) : (
          /* ✅ Even when no buttons, this ensures width stays the same */
          <HStack spacing={4}>
            {isLandingPage || currentPage === "product" || currentPage === "about" ? (
              <>
                <Button variant="outline" color="white" borderColor="white" onClick={onLoginClick}>
                  Login
                </Button>
                <Button colorScheme="teal" onClick={onSignupClick}>
                  Register
                </Button>
              </>
            ) : (
              <Box minW="150px" /> // Placeholder for spacing
            )}
          </HStack>
        )}
      </Box>
    </Flex>
  );
}

export default Navbar;
