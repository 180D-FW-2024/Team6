import React, { useState } from "react";
import { Box, Button, Input, Heading, Alert, AlertIcon, VStack, Text } from "@chakra-ui/react";
import axios from "axios";

function Signup({ onSignupSuccess, onGoBack, onLoginClick }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [userId, setUserId] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSignup = (e) => {
    e.preventDefault();
    axios
      .post(
        "http://localhost:5002/signup",
        { username, password, id: userId },
        { headers: { "Content-Type": "application/json" } }
      )
      .then(() => {
        setSuccess("Signup successful! You can now log in.");
        setError("");
        onSignupSuccess();
      })
      .catch(() => setError("Signup failed. Try again."));
  };

  return (
    <Box
      maxW="400px"
      mx="auto"
      mt="50px"
      p="6"
      borderWidth="1px"
      borderRadius="lg"
      boxShadow="lg"
      bg="brand.beige"
    >
      <Heading mb={4} textAlign="center" color="brand.darkBlue">
        Signup
      </Heading>
      {error && (
        <Alert status="error" mb={4}>
          <AlertIcon />
          {error}
        </Alert>
      )}
      {success && (
        <Alert status="success" mb={4}>
          <AlertIcon />
          {success}
        </Alert>
      )}
      <VStack spacing={3} as="form" onSubmit={handleSignup}>
        <Input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          focusBorderColor="brand.aqua"
        />
        <Input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          focusBorderColor="brand.aqua"
        />
        <Input
          placeholder="Choose a unique ID"
          type="number"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          focusBorderColor="brand.aqua"
        />
        <Button type="submit" bg="brand.brown" color="white" width="full" _hover={{ bg: "brand.darkBlue" }}>
          Sign Up
        </Button>
      </VStack>
      <Text textAlign="center" mt={4}>
        Already have an account?{" "}
        <Text
          as="span"
          color="blue.500"
          cursor="pointer"
          onClick={onLoginClick}
        >
          Login
        </Text>
      </Text>
      <Text textAlign="center" mt={2} cursor="pointer" color="blue.500" onClick={onGoBack}>
        Go Back to Landing Page
      </Text>
    </Box>
  );
}

export default Signup;
