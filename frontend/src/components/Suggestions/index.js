// src/components/Suggestions/index.js
import React from 'react';
import { Box, Button, Typography } from '@mui/material';
import './styles.css';

const Suggestions = ({ suggestions, onSelect }) => {
  return (
    <Box className="suggestions-container" mt={1}>
      <Typography variant="subtitle1" gutterBottom sx={{ color: '#919fcf', fontSize: '0.9rem', mb: 0.5 }}>
        Suggested Questions:
      </Typography>
      <Box display="flex" flexWrap="wrap" gap={1}>
        {suggestions.map((suggestion, index) => (
          <Button
            key={index}
            variant="contained"
            color="secondary"
            onClick={() => onSelect(suggestion)}
            sx={{
              textTransform: 'none',
              backgroundColor: '#919fcf',
              color: '#FFFFFF',
              fontSize: '0.8rem',
            }}
          >
            {suggestion}
          </Button>
        ))}
      </Box>
    </Box>
  );
};

export default Suggestions;
