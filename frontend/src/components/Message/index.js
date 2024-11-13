// src/components/Message/index.js

import React, { useState } from 'react';
import { Box, Typography, Avatar, Dialog } from '@mui/material';
import { deepOrange, deepPurple } from '@mui/material/colors';
import './styles.css';

const Message = ({ message, image }) => {
  const isUser = message.sender === 'CEO';
  const isDescription = message.sender === 'Description';

  const [openDialog, setOpenDialog] = useState(false); // State to control full-screen dialog

  let backgroundColor = 'rgba(243, 129, 104, 0.7)';
  let textColor = '#fff';

  if (isUser) {
    backgroundColor = 'rgba(243, 129, 104, 0.7)';
  } else if (isDescription) {
    backgroundColor = 'rgba(166, 166, 166, 0.5)';
    textColor = '#a6a6a6';
  } else {
    backgroundColor = 'rgba(4, 157, 217, 0.7)';
  }

  const renderMessageText = (text) => {
    const lines = text.split('\n').filter(line => line.trim() !== '');

    return lines.map((line, index) => {
      const listItemMatch = line.match(/^(\d+)\.\s+(.*)/);
      if (listItemMatch) {
        const number = listItemMatch[1];
        const content = listItemMatch[2];
        return (
          <Box key={index} display="flex" alignItems="flex-start" mb={0.5}>
            <Typography variant="body1" sx={{ color: textColor, fontSize: '0.85rem', mr: 0.5 }}>
              {number}.
            </Typography>
            <Typography variant="body1" sx={{ color: textColor, fontSize: '0.85rem' }}>
              {content}
            </Typography>
          </Box>
        );
      } else {
        return (
          <Typography key={index} variant="body1" sx={{ color: textColor, fontSize: '0.85rem', mb: 0.5 }}>
            {line}
          </Typography>
        );
      }
    });
  };

  const handleImageClick = () => {
    setOpenDialog(true); // Open full-screen dialog on click
  };

  const handleCloseDialog = () => {
    setOpenDialog(false); // Close dialog on click of escape or outside
  };

  return (
    <Box
      className="message"
      display="flex"
      flexDirection={isUser ? 'row-reverse' : 'row'}
      alignItems="flex-start"
      mb={1}
    >
      {!isDescription && (
        <Avatar
          sx={{
            bgcolor: isUser ? deepPurple[50] : deepOrange[50],
            marginLeft: isUser ? 0 : 1,
            marginRight: isUser ? 1 : 0,
            width: 28,
            height: 28,
            fontSize: '0.7rem',
          }}
        >
          {isUser ? 'CEO' : 'P(AI)'}
        </Avatar>
      )}

      {isDescription && (
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '100%',
          }}
        >
          <Typography variant="body2" sx={{ color: textColor, fontStyle: 'italic', fontSize: '0.8rem' }}>
            {message.text}
          </Typography>
        </Box>
      )}

      {!isDescription && (
        <Box
          color={textColor}
          borderRadius={2}
          p={1.5}
          maxWidth="80%"
          sx={{
            backgroundColor: backgroundColor,
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
            fontStyle: 'italic',
            fontSize: '0.85rem',
          }}
        >
          {renderMessageText(message.text)}

          {/* Display the value chain image if available */}
          {image && (
            <Box
              mt={2}
              sx={{
                cursor: 'pointer',
                textAlign: 'center',
              }}
              onClick={handleImageClick}
            >
              <img
                src={image}
                alt="Value Chain"
                style={{
                  width: '100%', // Make the image bigger on initial display
                  maxWidth: '1000px', // Set larger max width for bigger display
                  borderRadius: '8px',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)',
                }}
              />
            </Box>
          )}
        </Box>
      )}

      {/* Full-screen Dialog for Image */}
      {image && (
        <Dialog
          open={openDialog}
          onClose={handleCloseDialog}
          maxWidth="xl"
          fullScreen
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            backgroundColor: 'rgba(0, 0, 0, 0.9)', // Darken background for full-screen effect
          }}
        >
          <Box
            onClick={handleCloseDialog}
            sx={{
              width: '100%',
              maxHeight: '100vh',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              cursor: 'zoom-out',
            }}
          >
            <img
              src={image}
              alt="Full Size Value Chain"
              style={{ width: '100%', maxWidth: '90vw', maxHeight: '90vh', borderRadius: '8px' }}
            />
          </Box>
        </Dialog>
      )}
    </Box>
  );
};

export default Message;
