import React, { useState } from "react";
import {
  Box,
  Button,
  Input,
  Heading,
  Alert,
  AlertIcon,
  VStack,
  Text,
} from "@chakra-ui/react";
import axios from "axios";

function Login({ onLoginSuccess, onGoBack, onSignupClick }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    axios
      .post(
        "http://localhost:5002/login",
        { username, password },
        { headers: { "Content-Type": "application/json" }, withCredentials: true }
      )
      .then((response) => {
        const loggedInUsername = response.data.username; // Expect username from API
        onLoginSuccess(loggedInUsername); // Pass username to parent component
      })
      .catch(() => setError("Invalid username or password"));
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
        Login
      </Heading>
      {error && (
        <Alert status="error" mb={4}>
          <AlertIcon />
          {error}
        </Alert>
      )}
      <VStack spacing={3} as="form" onSubmit={handleLogin}>
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
        <Button
          type="submit"
          bg="brand.aqua"
          color="white"
          width="full"
          _hover={{ bg: "brand.darkBlue" }}
        >
          Login
        </Button>
      </VStack>
      <Text textAlign="center" mt={4}>
        Don’t have an account?{" "}
        <Text as="span" color="blue.500" cursor="pointer" onClick={onSignupClick}>
          Sign Up
        </Text>
      </Text>
      <Text
        textAlign="center"
        mt={2}
        cursor="pointer"
        color="blue.500"
        onClick={onGoBack}
      >
        Go Back to Landing Page
      </Text>
    </Box>
  );
}

export default Login;
