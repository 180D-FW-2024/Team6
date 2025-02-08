import React, { useState } from "react";
import { Box } from "@chakra-ui/react";
import Navbar from "./components_temp/Navbar";
import Login from "./components_temp/Login";
import Signup from "./components_temp/Signup";
import LandingPage from "./components_temp/LandingPage";
import Dashboard from "./components_temp/Dashboard";
import ProductPage from "./components_temp/ProductPage";
import AboutUsPage from "./components_temp/AboutUsPage";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPage, setCurrentPage] = useState("landing");

  const handleLogout = () => {
    setIsLoggedIn(false);
    setCurrentPage("landing");
  };

  return (
    <Box minH="100vh" bg="brand.beige">
      <Navbar
        isLandingPage={currentPage === "landing"}
        isLoggedIn={isLoggedIn}
        onLogout={handleLogout}
        onNavigateHome={() => setCurrentPage("landing")}
        onNavigateDashboard={() => setCurrentPage("dashboard")}
        onNavigateVoiceMemos={() => setCurrentPage("voiceMemos")}
        onNavigateVisitors={() => setCurrentPage("visitors")}
        onNavigateProduct={() => setCurrentPage("product")}
        onNavigateAbout={() => setCurrentPage("about")}
        onLoginClick={() => setCurrentPage("login")}
        onSignupClick={() => setCurrentPage("signup")}
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
          onLoginSuccess={() => {
            setIsLoggedIn(true);
            setCurrentPage("dashboard");
          }}
          onGoBack={() => setCurrentPage("landing")}
        />
      )}
      {currentPage === "signup" && (
        <Signup
          onSignupSuccess={() => setCurrentPage("login")}
          onGoBack={() => setCurrentPage("landing")}
        />
      )}
      {currentPage === "dashboard" && isLoggedIn && <Dashboard />}
      {currentPage === "voiceMemos" && <div>Voice Memos Page</div>}
      {currentPage === "visitors" && <div>Visitors Page</div>}
      {currentPage === "product" && <ProductPage />}
      {currentPage === "about" && <AboutUsPage />}
    </Box>
  );
}

export default App;
