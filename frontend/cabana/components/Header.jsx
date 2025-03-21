import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import { useRouter } from 'next/navigation';

const pages = [
  { label: 'Home', path: '/' },
  { label: 'About Us', path: '/about-us' },
  { label: '/get Demo', path: '/get-demo' }
];

function Header() {
  const router = useRouter();
  
  const handleNavigation = (path) => {
    router.push(path);
  };

  return (
    <AppBar position="static">
      <Toolbar sx={{ backgroundColor: '#2d325a'}}>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          CABANA
        </Typography>
        <Box>
          {pages.map((page) => (
            <Button
              key={page.label}
              color="inherit"
              onClick={() => handleNavigation(page.path)}
            >
              {page.label}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Header;
