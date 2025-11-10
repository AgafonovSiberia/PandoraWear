import {
  AppBar,
  Toolbar,
  Container,
  Box,
  Typography,
  IconButton,
  Avatar,
  Menu,
  MenuItem,
  ListItemIcon,
  Divider,
} from '@mui/material';
import {
  KeyboardArrowDown,
  Logout,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { useState, type MouseEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '@/providers/UserProvider';
import { api } from '@/api/axios';

export const AppTopBar = () => {
  const navigate = useNavigate();
  const { user, setUser } = useUser();

  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const menuOpen = Boolean(anchorEl);

  const userName = user?.username || user?.email || 'User';
  const userEmail = user?.email || '';

  const handleOpenMenu = (event: MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleCloseMenu = () => setAnchorEl(null);

  const handleLogout = async () => {
    handleCloseMenu();
    try {
      await api.post('/users/logout');
    } catch {
      // даже если запрос не удался — локально разлогиниваемся
    }
    setUser(null);
    navigate('/login', { replace: true });
  };

  const goToProfile = () => {
    handleCloseMenu();
    navigate('/app/profile');
  };

  return (
    <AppBar
      position="fixed"
      elevation={0}
      sx={{
        bgcolor: '#0F172A',
        borderBottom: '1px solid rgba(148, 163, 253, 0.12)',
      }}
    >
      <Container maxWidth="lg" sx={{ px: 2 }}>
        <Toolbar
          disableGutters
          sx={{
            minHeight: 64,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: 3,
          }}
        >
          {/* Логотип / бренд */}
          <Box display="flex" alignItems="center" gap={1.2}>
            <Box
              sx={{
                width: 22,
                height: 22,
                borderRadius: '6px',
                bgcolor: 'primary.main',
              }}
            />
            <Typography
              variant="h6"
              sx={{ fontWeight: 600, letterSpacing: 0.2 }}
            >
              PandoraWear
            </Typography>
          </Box>

          {/* Справа: аккаунт */}
          <Box
            onClick={handleOpenMenu}
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              cursor: 'pointer',
              px: 1,
              py: 0.5,
              borderRadius: 999,
              '&:hover': {
                bgcolor: 'rgba(148, 163, 253, 0.08)',
              },
            }}
          >
            <Avatar
              sx={{
                width: 28,
                height: 28,
                bgcolor: 'primary.main',
                fontSize: 14,
              }}
            >
              {userName[0]?.toUpperCase() ?? 'U'}
            </Avatar>
            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
              <Typography
                variant="body2"
                sx={{ lineHeight: 1.1, fontWeight: 500 }}
              >
                {userName}
              </Typography>
              {userEmail && (
                <Typography
                  variant="caption"
                  sx={{ lineHeight: 1.1, color: 'text.secondary' }}
                >
                  {userEmail}
                </Typography>
              )}
            </Box>
            <IconButton size="small" sx={{ color: 'text.secondary', p: 0 }}>
              <KeyboardArrowDown fontSize="small" />
            </IconButton>
          </Box>

          <Menu
            open={menuOpen}
            anchorEl={anchorEl}
            onClose={handleCloseMenu}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            PaperProps={{
              sx: {
                mt: 1,
                bgcolor: '#020817',
                color: 'text.primary',
                minWidth: 220,
                borderRadius: 2,
                border: '1px solid rgba(148, 163, 253, 0.18)',
              },
            }}
          >
            <MenuItem onClick={goToProfile}>
              <ListItemIcon>
                <SettingsIcon fontSize="small" />
              </ListItemIcon>
              Account settings
            </MenuItem>

            <Divider sx={{ borderColor: 'rgba(148, 163, 253, 0.18)' }} />

            <MenuItem onClick={handleLogout}>
              <ListItemIcon>
                <Logout fontSize="small" />
              </ListItemIcon>
              Logout
            </MenuItem>
          </Menu>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
