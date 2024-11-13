// src/components/LoadingSpinner/index.js
import React from 'react';
import { CircularProgress, Box } from '@mui/material';
import './styles.css';

const LoadingSpinner = () => {
  return (
    <Box display="flex" justifyContent="center" alignItems="center" mt={2} mb={2}>
      <CircularProgress color="secondary" />
    </Box>
  );
};

export default LoadingSpinner;
