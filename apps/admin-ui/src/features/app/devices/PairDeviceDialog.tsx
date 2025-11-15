import { useState } from 'react';
import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  InputAdornment,
  Stack,
  TextField,
  Tooltip,
  Typography,
} from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import { api } from '@/api/axios';

type Props = {
  open: boolean;
  onClose: () => void;
  onPaired?: (payload: { code: string; name: string }) => void;
};

export default function PairDeviceDialog({ open, onClose, onPaired }: Props) {
  const [name, setName] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [code, setCode] = useState<string | null>(null);
  const canSubmit = name.trim().length > 0 && !submitting;

  const handleClose = () => {
    if (submitting) return;
    setName('');
    setError(null);
    setCode(null);
    onClose();
  };

  const requestCode = async () => {
    try {
      setSubmitting(true);
      setError(null);
      const res = await api.post<{ pair_code: string }>('/devices/pairing/code', { name: name.trim() });
      setCode(res.data.pair_code);
      onPaired?.({ code: res.data.pair_code, name: name.trim() });
    } catch (e: any) {
      setError('Не удалось получить код сопряжения. Повторите попытку.');
    } finally {
      setSubmitting(false);
    }
  };

  const copyCode = async () => {
    if (!code) return;
    try {
      await navigator.clipboard.writeText(code);
    } catch {
      /* ignore */
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
      <DialogTitle>Привязать устройство</DialogTitle>
      <DialogContent>
        <Stack spacing={2} mt={1}>
          <TextField
            autoFocus
            label="Название устройства"
            placeholder="Например: Galaxy Watch Ultra"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={submitting || Boolean(code)}
            fullWidth
          />

          {error && <Alert severity="error">{error}</Alert>}

          {code && (
            <Box
              sx={{
                p: 2,
                borderRadius: 2,
                bgcolor: '#0f172a',
                color: 'white',
                border: '1px solid rgba(255,255,255,0.12)',
              }}
            >
              <Typography variant="subtitle2" gutterBottom>
                Код сопряжения
              </Typography>
              <TextField
                value={code}
                InputProps={{
                  readOnly: true,
                  endAdornment: (
                    <InputAdornment position="end">
                      <Tooltip title="Скопировать">
                        <IconButton onClick={copyCode} edge="end">
                          <ContentCopyIcon />
                        </IconButton>
                      </Tooltip>
                    </InputAdornment>
                  ),
                }}
                fullWidth
              />
              <Typography variant="body2" sx={{ mt: 1.5, color: 'rgba(255,255,255,0.7)' }}>
                Введите этот 6-значный код на устройстве.
              </Typography>
            </Box>
          )}
        </Stack>
      </DialogContent>

      <DialogActions sx={{ p: 2 }}>
        <Button onClick={handleClose} disabled={submitting}>
          Закрыть
        </Button>
        {!code && (
          <Button
            variant="contained"
            onClick={requestCode}
            disabled={!canSubmit}
          >
            {submitting ? 'Запрос...' : 'Код сопряжения'}
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
}