// src/components/Sidebar/index.js
import React from 'react';
import { Box, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';
import './styles.css';

const Sidebar = ({ recentChats, onSelectChat }) => {
  return (
    <Box
      className="sidebar-container"
      sx={{
        width: '18vw', // Reduced width from 25vw to 20vw
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        color: '#fff',
        padding: 1.5, // Reduced padding
        borderRadius: 2,
        overflowY: 'auto',
        height: '100vh', // Extend to bottom
        boxSizing: 'border-box',
      }}
    >
      <Typography variant="h6" gutterBottom sx={{ color: '#a6a6a6', fontSize: '1rem' }}>
        Recent Chats
      </Typography>
      <Divider sx={{ backgroundColor: '#a6a6a6', mb: 1.5 }} />
      <List>
        {recentChats.length === 0 && (
          <ListItem>
            <ListItemText primary="No recent chats." sx={{ color: '#ffffff', fontSize: '0.85rem' }} />
          </ListItem>
        )}
        {recentChats.map((chat, index) => (
          <ListItem button key={index} onClick={() => onSelectChat(chat)}>
            <ListItemText
              primary={chat.title}
              secondary={chat.timestamp}
              primaryTypographyProps={{ fontSize: '0.85rem', color: '#ffffff' }} // Enhanced visibility
              secondaryTypographyProps={{ fontSize: '0.75rem', color: '#a6a6a6' }} // Timestamp in orange
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default Sidebar;
