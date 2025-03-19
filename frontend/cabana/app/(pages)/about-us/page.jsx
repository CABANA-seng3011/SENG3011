'use client';

import { Container, Typography, Stack } from '@mui/material';
import FlipCard from '../../../components/FlipCard';
import { esgDesc } from '../../../public/data';

export default function ESGPage() {
  return (
    <Container 
      maxWidth='lg'
      height='100vh'
      py='4'
    >
      <Typography 
        textAlign='center' 
        variant='h2' 
        className='mb-12 font-bold'
      >
        ESG Pillars
      </Typography>
      <Typography 
        textAlign='center' 
        variant='body' 
        className='mb-12 font-bold'
      >
        {esgDesc}
      </Typography>
      <Stack 
        direction='row' 
        spacing={6} 
        justifyContent='center' 
        alignItems='center'
      >
        <FlipCard imagePath='/enviro.jpeg' imageAlt='Graphic of a tree' cardTitle='Environmental' description='hello' />
        <FlipCard imagePath='/social.jpg' imageAlt='Graphic of people and a globe' cardTitle='Social' description='hello' />
        <FlipCard imagePath='/govern.png' imageAlt='Graphic of people and a cog'  cardTitle='Governance' description='hello' />
      </Stack>
    </Container>
  );
}