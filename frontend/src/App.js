import { useState, useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Dashboard from "@/pages/Dashboard";
import Landing from "@/pages/Landing";
import SignIn from "@/pages/SignIn";
import SignUp from "@/pages/SignUp";
import RequireAuth from "@/auth/RequireAuth";
import { AuthProvider } from "@/auth/AuthContext";
import { Toaster } from "@/components/ui/sonner";
import { AnimatePresence, motion } from "framer-motion";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <AuthProvider>
          <RouteTransitions />
        </AuthProvider>
      </BrowserRouter>
      <Toaster position="top-right" />
    </div>
  );
}

export default App;

function RouteTransitions() {
  const location = useLocation();
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route
          path="/"
          element={
            <FadePage>
              <Landing />
            </FadePage>
          }
        />
        <Route
          path="/signin"
          element={
            <FadePage>
              <SignIn />
            </FadePage>
          }
        />
        <Route
          path="/signup"
          element={
            <FadePage>
              <SignUp />
            </FadePage>
          }
        />
        <Route
          path="/dashboard"
          element={
            <RequireAuth>
              <FadePage>
                <Dashboard />
              </FadePage>
            </RequireAuth>
          }
        />
      </Routes>
    </AnimatePresence>
  );
}

function FadePage({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}