// src/components/ChatWindow/index.js
import React, { useRef, useEffect } from 'react';
import { Paper, Box, Typography } from '@mui/material';
import Message from '../Message';
import './styles.css';

const ChatWindow = ({ messages, imageResponse }) => {
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, imageResponse]);

  return (
    <Paper
      elevation={0}
      sx={{
        flexGrow: 1,
        padding: 2,
        marginBottom: 1,
        overflowY: 'auto',
        backgroundColor: 'transparent',
        borderRadius: 0,
      }}
    >
      {messages.map((msg, index) => (
        <Message key={index} message={msg} />
      ))}

      {/* Display the image response if present */}
      {imageResponse && (
        <Box display="flex" justifyContent="center" mt={2} mb={2}>
          <img src={imageResponse} alt="Value Chain" style={{ maxWidth: '100%', maxHeight: '300px' }} />
        </Box>
      )}

      <div ref={chatEndRef} />
    </Paper>
  );
};

export default ChatWindow;
