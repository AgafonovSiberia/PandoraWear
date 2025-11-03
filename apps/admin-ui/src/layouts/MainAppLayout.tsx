import { Outlet, NavLink } from 'react-router-dom';
import {
  Avatar,
  Box,
  Divider,
  List,
  ListItemButton,
  ListItemText,
  Stack,
  Typography,
} from '@mui/material';
import { useUser } from '../providers/UserProvider';

export default function MainLayout() {
  const { user } = useUser();

  return (
    <Box display="flex" height="100dvh" bgcolor="#0f172a" color="white">
      {/* Sidebar */}
      <Box
        width={240}
        bgcolor="#1e293b"
        py={2}
        px={2}
        display="flex"
        flexDirection="column"
        justifyContent="flex-start"
      >
        {/* User info */}
        <Stack direction="row" spacing={1.2} alignItems="center" sx={{ mb: 1 }}>
          <Avatar
            sx={{
              width: 38,
              height: 38,
              bgcolor: 'rgba(59,130,246,0.25)',
              color: '#93c5fd',
              fontWeight: 700,
              fontSize: 18,
            }}
          >
            {(user?.username?.[0] || '?').toUpperCase()}
          </Avatar>

          <Box overflow="hidden">
            <Typography variant="subtitle1" fontWeight={700} noWrap>
              {user?.username ?? '—'}
            </Typography>
            <Typography
              variant="body2"
              sx={{ color: 'rgba(255,255,255,0.65)' }}
              noWrap
              title={user?.email}
            >
              {user?.email ?? '—'}
            </Typography>
          </Box>
        </Stack>

        <Divider sx={{ borderColor: 'rgba(255,255,255,0.08)', my: 1 }} />

        {/* Navigation */}
        <List sx={{ py: 0 }}>
          {[
            { to: '/app/profile', label: 'Profile' },
            { to: '/app/devices', label: 'My devices' },
            { to: '/app/settings', label: 'Settings' },
          ].map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              style={{ textDecoration: 'none' }}
              end
            >
              {({ isActive }: { isActive: boolean }) => (
                <ListItemButton
                  sx={{
                    borderRadius: 1.5,
                    mb: 0.5,
                    color: isActive ? 'white' : 'rgba(255,255,255,0.8)',
                    bgcolor: isActive ? 'rgba(59,130,246,0.15)' : 'transparent',
                    transition: 'background-color 0.2s ease',
                    '&:hover': { bgcolor: 'rgba(59,130,246,0.1)' },
                  }}
                >
                  <ListItemText primary={item.label} />
                </ListItemButton>
              )}
            </NavLink>
          ))}
        </List>
      </Box>

      <Box flexGrow={1} p={4}>
        <Outlet />
      </Box>
    </Box>
  );
}