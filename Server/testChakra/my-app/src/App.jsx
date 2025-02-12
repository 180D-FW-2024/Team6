import React, { useState, useEffect } from "react";
import axios from "axios";
import { Box } from "@chakra-ui/react";
import Navbar from "./components_temp/Navbar";
import Login from "./components_temp/Login";
import Signup from "./components_temp/Signup";
import LandingPage from "./components_temp/LandingPage";
import Dashboard from "./components_temp/Dashboard";
import ProductPage from "./components_temp/ProductPage";
import AboutUsPage from "./components_temp/AboutUsPage";
import SettingsPage from "./components_temp/SettingsPage";
import VoiceMemos from "./components_temp/VoiceMemos";
import Residents from "./components_temp/Residents";
import Visitors from "./components_temp/Visitors"; 


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPage, setCurrentPage] = useState("landing");
  const [userName, setUserName] = useState(""); // State to hold the username

  // Check login status on app load
  useEffect(() => {
    axios
      .get("http://localhost:5002/check_login", { withCredentials: true })
      .then((response) => {
        if (response.data.logged_in) {
          setIsLoggedIn(true);
          setUserName(response.data.username); // Update username
          setCurrentPage("dashboard");
        }
      })
      .catch(() => {
        // User is not logged in
        setIsLoggedIn(false);
        setUserName("");
      });
  }, [isLoggedIn]);

  const handleLogout = () => {
    axios
      .post("http://localhost:5002/logout", {}, { withCredentials: true })
      .then(() => {
        setIsLoggedIn(false);
        setUserName("");
        setCurrentPage("landing");
      });
  };

  const handleLoginSuccess = (username) => {
    setIsLoggedIn(true);
    setUserName(username); // Update username immediately upon login
    setCurrentPage("dashboard");
  };

  return (
    <Box minH="100vh" bg="brand.beige">
      <Navbar
        currentPage={currentPage} // Pass currentPage prop to Navbar
        isLandingPage={currentPage === "landing"} // ONLY landing page gets this
        isLoggedIn={isLoggedIn}
        userName={userName}
        onLogout={handleLogout}
        onNavigateHome={() => setCurrentPage(isLoggedIn ? "dashboard" : "landing")}
        onNavigateDashboard={() => setCurrentPage("dashboard")}
        onNavigateSettings={() => setCurrentPage("settings")}
        onNavigateVoiceMemos={() => setCurrentPage("voiceMemos")}
        onNavigateVisitors={() => setCurrentPage("visitors")}
        onNavigateResidents={() => setCurrentPage("residents")}
        onNavigateProduct={() => setCurrentPage("product")}
        onNavigateAbout={() => setCurrentPage("about")}
      />
      {/* Page Rendering */}
      {currentPage === "landing" && (
        <LandingPage
          onLoginClick={() => setCurrentPage("login")}
          onSignupClick={() => setCurrentPage("signup")}
        />
      )}
      {currentPage === "login" && (
        <Login
          onLoginSuccess={handleLoginSuccess} // Pass success handler
          onGoBack={() => setCurrentPage("landing")}
          onSignupClick={() => setCurrentPage("signup")} // Fix redirection to signup
        />
      )}

      {currentPage === "signup" && (
        <Signup
          onSignupSuccess={() => setCurrentPage("login")} // Fix redirection to login
          onGoBack={() => setCurrentPage("landing")}
          onLoginClick={() => setCurrentPage("login")} // Fix redirection to login
        />
      )}
      {currentPage === "dashboard" && isLoggedIn && <Dashboard />}
      {currentPage === "voiceMemos" && <VoiceMemos />}
      {currentPage === "residents" && <Residents />}
      {currentPage === "product" && <ProductPage />}
      {currentPage === "about" && <AboutUsPage />}
      {currentPage === "settings" && <SettingsPage />}
      {currentPage === "visitors" && <Visitors />}

    </Box>
  );
}

export default App;
