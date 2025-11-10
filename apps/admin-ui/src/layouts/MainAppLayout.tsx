import { Outlet, useLocation, Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Container,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import DevicesIcon from '@mui/icons-material/Devices';
import SettingsIcon from '@mui/icons-material/Settings';
import { AppTopBar } from './AppTopBar';

const NAV_ITEMS = [
  {
    label: 'Устройства',
    to: '/app/devices',
    icon: <DevicesIcon fontSize="small" />,
  },
  {
    label: 'Настройки',
    to: '/app/settings',
    icon: <SettingsIcon fontSize="small" />,
  },
];

export default function MainAppLayout() {
  const location = useLocation();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        bgcolor: '#020817',
        color: '#E5E7EB',
      }}
    >
      <AppTopBar />

      <Box
        component="main"
        sx={{
          pt: 10,
          pb: 4,
        }}
      >
        <Container
          maxWidth="lg"
          sx={{
            display: 'flex',
            gap: 2,
          }}
        >
          <Box
            sx={{
              width: 200,
              flexShrink: 0,
              bgcolor: 'rgba(15,23,42,0.98)',
              borderRadius: 0.5,
              border: '0.5px solid rgba(148, 163, 253, 0.12)',
              p: 0.6,
            }}
          >

            <List dense disablePadding>
              {NAV_ITEMS.map((item) => {
                const active = location.pathname.startsWith(item.to);
                return (
                  <ListItemButton
                    key={item.to}
                    component={RouterLink}
                    to={item.to}
                    selected={active}
                    sx={{
                      mt: 0.5,
                      borderRadius: 0.3,
                      px: 1.25,
                      py: 0.75,
                      '&.Mui-selected': {
                        bgcolor: 'rgba(129, 140, 248, 0.16)',
                        '&:hover': {
                          bgcolor: 'rgba(129, 140, 248, 0.22)',
                        },
                      },
                      '&:hover': {
                        bgcolor: 'rgba(148, 163, 253, 0.08)',
                      },
                    }}
                  >
                    <ListItemIcon
                      sx={{
                        minWidth: 32,
                        color: active ? 'primary.main' : 'text.secondary',
                      }}
                    >
                      {item.icon}
                    </ListItemIcon>
                    <ListItemText
                      primary={item.label}
                      primaryTypographyProps={{
                        fontSize: 12,
                        fontWeight: active ? 600 : 400,
                      }}
                    />
                  </ListItemButton>
                );
              })}
            </List>
          </Box>


          <Box
            sx={{
              flex: 1,
              minWidth: 0,
            }}
          >
            <Outlet />
          </Box>
        </Container>
      </Box>
    </Box>
  );
}
