// src/App.js

import React, { useState, useEffect } from 'react';
import { Container, Typography, Box } from '@mui/material';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import NewChatButton from './components/NewChatButton';
import LoadingSpinner from './components/LoadingSpinner';
import Suggestions from './components/Suggestions';
import Sidebar from './components/Sidebar';
import axios from 'axios';
import './App.css';
import background from './assets/background.jpg';

const MAX_RECENT_CHATS = 5; // Limit the number of recent chats stored

const App = () => {
  const [messages, setMessages] = useState([
    { sender: 'Aiko', text: 'Hello! I am Aiko. How can I assist you today?' },
    { sender: 'Description', text: 'Select a suggested question below or type your own to get started.' },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [recentChats, setRecentChats] = useState([]);
  const [suggestions, setSuggestions] = useState([
    "Tell me about the Asset Reconstruction value chain.",
    "What are some AI use cases in manufacturing?",
    "How can AI improve customer service?",
    "Show me AI use cases for Retail."
  ]);
  const [imageResponse, setImageResponse] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5002';

  // Load recent chats from localStorage on mount
  useEffect(() => {
    try {
      const storedChats = JSON.parse(localStorage.getItem('recentChats'));
      if (storedChats) {
        setRecentChats(storedChats.slice(0, MAX_RECENT_CHATS)); // Load only up to MAX_RECENT_CHATS
      }
    } catch (error) {
      console.warn("Error loading recent chats from localStorage:", error);
    }
  }, []);

  // Save recent chats to localStorage when recentChats changes
  useEffect(() => {
    try {
      localStorage.setItem('recentChats', JSON.stringify(recentChats.slice(0, MAX_RECENT_CHATS))); // Save only up to MAX_RECENT_CHATS
    } catch (error) {
      if (error.name === "QuotaExceededError") {
        console.warn("localStorage quota exceeded; clearing recentChats.");
        localStorage.removeItem('recentChats'); // Clear storage if quota is exceeded
      } else {
        console.error("Error saving recent chats to localStorage:", error);
      }
    }
  }, [recentChats]);

  const handleSend = async (text) => {
    const userMessage = { sender: 'CEO', text };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${backendUrl}/chat`, { message: text });
      const botMessage = { sender: 'Aiko', text: response.data.response };

      if (response.data.image) {
        setImageResponse(response.data.image); // Display image if included
      } else {
        setImageResponse(null); // Clear any previous image response
      }

      setMessages((prev) => [...prev, botMessage]);

      const chatTitle = text.length > 20 ? text.substring(0, 20) + '...' : text;
      const timestamp = new Date().toLocaleString();
      
      // Add to recentChats and limit its size
      setRecentChats((prev) => [
        { title: chatTitle, timestamp, messages: [userMessage, botMessage] },
        ...prev.slice(0, MAX_RECENT_CHATS - 1) // Keep only up to MAX_RECENT_CHATS
      ]);
    } catch (error) {
      console.error(error);
      const errorMsg = error.response && error.response.data && error.response.data.error
        ? error.response.data.error
        : 'Sorry, something went wrong. Please try again.';
      const errorMessage = { sender: 'Aiko', text: errorMsg };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = async () => {
    setIsLoading(true);
    try {
      await axios.post(`${backendUrl}/reset_chat`); 
      setMessages([
        { sender: 'Aiko', text: 'Hello! I am Aiko. How can I assist you today?' },
        { sender: 'Description', text: 'Select a suggested question below or type your own to get started.' },
      ]);
      setRecentChats([]);
      setImageResponse(null); // Clear any displayed image on new chat
    } catch (error) {
      console.error(error);
      const errorMsg = error.response && error.response.data && error.response.data.error
        ? error.response.data.error
        : 'Failed to reset the conversation. Please try again.';
      const errorMessage = { sender: 'Aiko', text: errorMsg };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionSelect = async (suggestion) => {
    handleSend(suggestion);

    try {
      const response = await axios.post(`${backendUrl}/suggestions`, { message: suggestion });
      setSuggestions(response.data.suggestions);
    } catch (error) {
      console.error("Error fetching suggestions:", error);
    }
  };

  const handleSelectRecentChat = (chat) => {
    setMessages(chat.messages);
  };

  return (
    <div
      style={{
        backgroundImage: `url(${background})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        backgroundAttachment: 'fixed',
        height: '100vh',
        width: '100%',
        display: 'flex',
        overflow: 'hidden',
        boxSizing: 'border-box',
      }}
    >
      <Sidebar recentChats={recentChats} onSelectChat={handleSelectRecentChat} />

      <Container
        maxWidth={false}
        disableGutters
        sx={{
          display: 'flex',
          flexDirection: 'column',
          height: '100vh',
          width: '85vw',
          marginLeft: '20vw',
          padding: 1,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          borderRadius: 1,
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.3)',
          overflow: 'hidden',
        }}
      >
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={0.5}>
          <Typography variant="h6" sx={{ color: '#f38168', fontWeight: 'bold', fontSize: '1.1rem' }}>
            Aiko Chatbot
          </Typography>
          <NewChatButton onNewChat={handleNewChat} />
        </Box>

        <Typography variant="body2" align="left" gutterBottom sx={{ color: '#a6a6a6', fontSize: '0.8rem', mb: 0.5 }}>
          I can help you understand our value chains and AI use cases for various industries.
        </Typography>

        <Box flexGrow={1} mb={0.5} sx={{ overflowY: 'auto', paddingRight: '5px' }}>
          <ChatWindow messages={messages} imageResponse={imageResponse} />
          {isLoading && <LoadingSpinner />}
        </Box>

        <Suggestions suggestions={suggestions} onSelect={handleSuggestionSelect} />

        <ChatInput onSend={handleSend} isLoading={isLoading} />
      </Container>
    </div>
  );
};

export default App;
