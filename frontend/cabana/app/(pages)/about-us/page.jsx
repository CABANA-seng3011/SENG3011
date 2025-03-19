'use client';

import { Container, Typography } from '@mui/material';
import FlipCard from '../../../components/FlipCard';

export default function ESGPage() {
  return (
    <Container className='flex flex-col items-center justify-center h-screen'>
      <Typography variant='h4' className='mb-8 font-bold'>
        ESG Pillars
      </Typography>
      <FlipCard imagePath='/favicon.ico' cardTitle='Environmental' description='hello' />
      <FlipCard imagePath='/favicon.ico' cardTitle='Social' description='hello' />
      <FlipCard imagePath='/favicon.ico' cardTitle='Governance' description='hello' />
    </Container>
  );
}