import { useState, useMemo, useEffect, type ChangeEvent } from 'react';
import {
  Box,
  Tabs,
  Tab,
  Card,
  CardHeader,
  CardContent,
  Divider,
  TextField,
  IconButton,
  InputAdornment,
  Button,
  Stack,
  Typography,
  Chip,
} from '@mui/material';
import { Visibility, VisibilityOff, Save } from '@mui/icons-material';
import { api } from '@/api/axios';

type TabId = 'pandora' | 'telegram';

interface PandoraCreds {
  email: string;
  password: string;
}

const EMPTY_CREDS: PandoraCreds = {
  email: '',
  password: '',
};

export default function SettingsPage() {
  const [tab, setTab] = useState<TabId>('pandora');

  return (
    <Box>
      <Typography variant="h5" mb={2}>
        Настройки
      </Typography>

      <Tabs
        value={tab}
        onChange={(_, v) => setTab(v)}
        aria-label="Integration settings"
        sx={{ mb: 3 }}
      >
        <Tab label="Pandora" value="pandora" />
        <Tab
          label={
            <Box display="flex" alignItems="center" gap={1}>
              <span>Telegram</span>
              <Chip
                label="soon"
                size="small"
                sx={{ fontSize: '0.6rem', height: 16 }}
              />
            </Box>
          }
          value="telegram"
          disabled
        />
      </Tabs>

      {tab === 'pandora' && <PandoraSettingsCard />}
    </Box>
  );
}

// ---------------------------------------------------------------------------

const PandoraSettingsCard = () => {
  const [initialCreds, setInitialCreds] = useState<PandoraCreds>(EMPTY_CREDS);
  const [creds, setCreds] = useState<PandoraCreds>(EMPTY_CREDS);

  const [showPassword, setShowPassword] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // --- загрузка текущей конфигурации с бэка ---
  useEffect(() => {
    let isActive = true;

    const fetchCreds = async () => {
      try {
        setIsLoading(true);
        const { data } = await api.get('/config/pandora/credentials');

        if (!isActive) return;

        // допускаем, что бэк может не возвращать пароль по соображениям безопасности
        const next: PandoraCreds = {
          email: data?.email ?? '',
          password: data?.password ?? '',
        };

        setInitialCreds(next);
        setCreds(next);
      } catch (error: any) {
        // 404 / отсутствует конфиг — считаем как пустую конфигурацию
        if (error?.response?.status === 404) {
          if (!isActive) return;
          setInitialCreds(EMPTY_CREDS);
          setCreds(EMPTY_CREDS);
        } else {
          console.error('Failed to load Pandora credentials', error);
        }
      } finally {
        if (isActive) setIsLoading(false);
      }
    };

    fetchCreds();

    return () => {
      isActive = false;
    };
  }, []);

  const isDirty = useMemo(
    () =>
      creds.email !== initialCreds.email ||
      creds.password !== initialCreds.password,
    [creds, initialCreds],
  );

  const handleChange =
    (field: keyof PandoraCreds) =>
    (e: ChangeEvent<HTMLInputElement>) => {
      setCreds((prev) => ({ ...prev, [field]: e.target.value }));
    };

  const handleTogglePassword = () => setShowPassword((v) => !v);

  const handleSave = async () => {
    if (!isDirty || isSaving || isLoading) return;

    try {
      setIsSaving(true);

      await api.post('/config/pandora/credentials', {
        email: creds.email,
        password: creds.password,
      });

      setInitialCreds(creds);
      setShowPassword(false);
    } catch (error) {
      console.error('Failed to save Pandora credentials', error);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Card
      sx={{
        borderRadius: 0.5,
        bgcolor: 'rgba(15,23,42,0.96)',
        border: '1px solid rgba(148,163,253,0.12)',
      }}
    >
      <CardHeader
        title="Pandora integration"
        subheader="Настройки подключения и доступа к Pandora API."
        sx={{
          '& .MuiCardHeader-title': { fontSize: 18, fontWeight: 600 },
          '& .MuiCardHeader-subheader': { color: 'text.secondary' },
        }}
      />
      <CardContent>
        <Box mb={1}>
          <Stack spacing={0.7} sx={{ maxWidth: 360 }}>
            <TextField
              label="Email"
              placeholder="Email"
              type="email"
              value={creds.email}
              onChange={handleChange('email')}
              size="small"
              margin="dense"
              fullWidth
              disabled={isLoading}
              InputProps={{
                sx: {
                  borderRadius: 0.5,
                  bgcolor: 'rgba(255,255,255,0.02)',
                  '& .MuiInputBase-input::placeholder': {
                    color: 'rgba(148, 163, 253, 0.4)',
                    opacity: 1,
                  },
                },
              }}
            />

            <TextField
              label="Password"
              placeholder="Password"
              type={showPassword ? 'text' : 'password'}
              value={creds.password}
              onChange={handleChange('password')}
              size="small"
              margin="dense"
              fullWidth
              disabled={isLoading}
              InputProps={{
                sx: {
                  borderRadius: 0.5,
                  bgcolor: 'rgba(255,255,255,0.02)',
                  '& .MuiInputBase-input::placeholder': {
                    color: 'rgba(148, 163, 253, 0.4)',
                    opacity: 1,
                  },
                },
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label={
                        showPassword ? 'Hide password' : 'Show password'
                      }
                      onClick={handleTogglePassword}
                      edge="end"
                      size="small"
                      sx={{ color: 'text.secondary' }}
                      disabled={isLoading}
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </Stack>

          <Box mt={2} display="flex" justifyContent="flex-end">
            <Button
              variant="contained"
              size="small"
              startIcon={<Save />}
              onClick={handleSave}
              disabled={!isDirty || isSaving || isLoading}
              sx={{
                borderRadius: 0.5,
                textTransform: 'none',
                fontWeight: 500,
                px: 2.5,
              }}
            >
              Save credentials
            </Button>
          </Box>
        </Box>

        <Divider sx={{ my: 2, borderColor: 'rgba(148,163,253,0.12)' }} />

        {/* Секция 2: Advanced options */}
        <Box>
          <Typography variant="subtitle1" fontWeight={600} mb={0.5}>
            Advanced options
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Здесь позже появятся дополнительные параметры интеграции Pandora.
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};
