import {
  Box, Card, CardContent, TextField, Typography, Button, Stack, Link,
} from '@mui/material';
import NotificationsNoneOutlinedIcon from '@mui/icons-material/NotificationsNoneOutlined';

export default function SignUpCard() {
  return (
    <Box
      minHeight="100dvh"
      display="flex"
      alignItems="center"
      justifyContent="center"
      sx={{
        p: 2,
        backgroundImage:
          'radial-gradient(1200px 500px at 20% -10%, rgba(59,130,246,0.10), transparent), radial-gradient(800px 400px at 90% 110%, rgba(59,130,246,0.06), transparent)',
      }}
    >
      <Box
          sx={{
              width: '100%',
              maxWidth: 720,
              borderRadius: 1,
              p: {xs: 3, md: 4},
              backgroundColor: 'transparent',
              boxShadow:
                  '0 0 0 1px rgba(255,255,255,0.04), 0 7px 24px rgba(59,130,246,0.1), 13 8px 32px rgba(0,0,0,0.4)',
              backgroundImage:
                  'radial-gradient(circle at 50% 0%, rgba(59,130,246,0.05) 0%, transparent 90%)',
          }}
      >
        <Box display="flex" justifyContent="center" mb={3}>
          <Stack direction="row" alignItems="center" spacing={1.5}>
            <NotificationsNoneOutlinedIcon sx={{ fontSize: 36 }} />
            <Typography variant="h4" fontWeight={800}>
              Pandora Wear
            </Typography>
          </Stack>
        </Box>

        <Box display="flex" justifyContent="center">
          <Card sx={{ maxWidth: 520, width: '100%' }}>
            <CardContent sx={{ p: { xs: 3, md: 4 } }}>
              <Typography variant="h5" fontWeight={700} mb={2}>
                Sign up
              </Typography>

              <Stack spacing={2.2}>
                <TextField label="Username" />
                <TextField label="Email" type="email" />
                <TextField label="Password" type="password" />

                <Button size="large">Sign up</Button>

                <Typography variant="body2" color="text.secondary" textAlign="center">
                  Already have an account?{' '}
                  <Link href="#">Log in</Link>
                </Typography>
              </Stack>
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Box>
  );
}