// src/components/NewChatButton/index.js
import React from 'react';
import { Button, Tooltip } from '@mui/material';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import './styles.css';

const NewChatButton = ({ onNewChat }) => {
  return (
    <Tooltip title="Start a new conversation" arrow>
      <Button
        variant="contained"
        startIcon={<RestartAltIcon />}
        onClick={onNewChat}
        sx={{
          backgroundColor: '#919fcf', // Blue background
          color: '#fff',
          '&:hover': {
            backgroundColor: '#049dd9',
          },
          transition: 'background-color 0.3s ease',
          fontSize: '0.8rem', // Reduced font size
          padding: '4px 8px', // Reduced padding
          minWidth: 'auto', // Adjust button width to content
        }}
      >
        New Chat
      </Button>
    </Tooltip>
  );
};

export default NewChatButton;
