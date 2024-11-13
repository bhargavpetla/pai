// src/components/ChatInput/index.js
import React, { useState } from 'react';
import { Box, TextField, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import './styles.css';

const ChatInput = ({ onSend, isLoading }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() === '') return;
    onSend(input);
    setInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <Box display="flex" alignItems="center" mt={1}>
      <TextField
        variant="outlined"
        placeholder="Type your message..."
        fullWidth
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        disabled={isLoading}
        sx={{
          backgroundColor: 'rgba(255, 255, 255, 0.2)',
          borderRadius: 2,
          mr: 1,
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.3)',
            },
            '&:hover fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.5)',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#049dd9',
            },
          },
          '& .MuiInputBase-input': {
            color: '#fff',
            fontSize: '0.8rem', // Reduced font size
          },
        }}
      />
      <IconButton
        color="primary"
        onClick={handleSend}
        sx={{
          backgroundColor: '#919fcf', // Orange background
          color: '#fff',
          '&:hover': {
            backgroundColor: '#049dd9',
          },
          fontSize: '1rem', // Standard icon size
          padding: '6px', // Reduced padding
        }}
        disabled={isLoading}
      >
        <SendIcon />
      </IconButton>
    </Box>
  );
};

export default ChatInput;
