import { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import { UserProvider, useUser } from '@/providers/UserProvider'

function GuardedOutlet() {
  const { user, loading } = useUser();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && !user) {
      navigate('/login', { replace: true });
    }
  }, [loading, user, navigate]);

  if (loading) {
    return (
      <Box display="flex" alignItems="center" justifyContent="center" height="100dvh">
        <CircularProgress />
      </Box>
    );
  }

  // user === null уже обработали редиректом
  return <Outlet />;
}

export default function ProtectedLayout() {
  return (
    <UserProvider>
      <GuardedOutlet />
    </UserProvider>
  );
}