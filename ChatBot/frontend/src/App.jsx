import React from 'react'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


//import pages
import Login from "./pages/login"
import Chatbot from "./pages/chatbox"
import Signup from "./pages/signup"

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login/>} />
        <Route path="/chat" element={<Chatbot/>} />
        <Route path="/signup" element={<Signup/>} />

      </Routes>

    </Router>
  )
}

export default App