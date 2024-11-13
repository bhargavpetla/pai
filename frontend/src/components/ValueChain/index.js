// src/components/ValueChain/index.js
import React from 'react';
import { Box, Typography, Paper, List, ListItem, ListItemText } from '@mui/material';
import { styled } from '@mui/material/styles';
import './styles.css';

const Step = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(1.5), // Reduced padding
  margin: theme.spacing(0.5), // Reduced margin
  textAlign: 'center',
  color: '#FFFFFF', // Set text color to white
  flex: 1,
  backgroundColor: 'rgba(255, 165, 0, 0.2)', // Light orange with transparency
  fontSize: '0.8rem', // Reduced font size
}));

const ValueChain = ({ industry, valueChain }) => {
  return (
    <Box className="value-chain-container" mt={2}>
      <Typography variant="h6" gutterBottom sx={{ color: '#FFA500', fontWeight: 'bold', fontSize: '1rem' }}>
        Value Chain for {industry}
      </Typography>
      <Box display="flex" justifyContent="space-between" flexWrap="wrap" alignItems="center">
        {valueChain.map((step, index) => (
          <React.Fragment key={index}>
            <Box display="flex" flexDirection="column" alignItems="center" flexBasis="30%">
              <Step elevation={1}>
                <Typography variant="subtitle2" gutterBottom sx={{ fontSize: '0.9rem' }}>
                  {step.name}
                </Typography>
                <List dense>
                  {step.useCases.map((useCase, idx) => (
                    <ListItem key={idx} sx={{ padding: '0px', fontSize: '0.75rem' }}>
                      <ListItemText primary={`• ${useCase}`} />
                    </ListItem>
                  ))}
                </List>
              </Step>
            </Box>
            {index < valueChain.length - 1 && (
              <Typography variant="h5" sx={{ color: '#FFA500', fontSize: '1rem', mx: 1 }}>
                →
              </Typography>
            )}
          </React.Fragment>
        ))}
      </Box>
    </Box>
  );
};

export default ValueChain;
