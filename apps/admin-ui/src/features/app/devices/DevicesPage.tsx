import {useEffect, useMemo, useRef, useState} from 'react';
import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    IconButton,
    Snackbar,
    Stack,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
} from '@mui/material';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import RefreshIcon from '@mui/icons-material/Refresh';
import {api} from '@/api/axios';
import PairDeviceDialog from "@/features/app/devices/PairDeviceDialog.tsx";

type Device = {
    id: string;
    name: string;
    expires_at: string;
    last_used_at: string | null;
    last_rotated_at: string
};


export default function DevicesPage() {
    const [rows, setRows] = useState<Device[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [confirmId, setConfirmId] = useState<string | null>(null);
    const [busyId, setBusyId] = useState<string | null>(null);

    const [snack, setSnack] = useState<{ open: boolean; text: string; kind?: 'success' | 'error' }>({
        open: false,
        text: '',
        kind: 'success',
    });
    const [pairOpen, setPairOpen] = useState(false);

    const didFetch = useRef(false);

    const load = async () => {
        setLoading(true);
        setError(null);
        try {
            const r = await api.get<Device[]>('/devices');
            setRows(r.data);
        } catch (e: any) {
            setError('Не удалось загрузить список устройств');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (didFetch.current) return;
        didFetch.current = true;
        void load();
    }, []);
    const fmtDate = (iso: string | null) =>
        iso ? new Date(iso).toLocaleString() : '—';

    const isBusy = useMemo(() => loading || Boolean(busyId), [loading, busyId]);

    const revoke = async (id: string) => {
        setBusyId(id);
        try {
            await api.delete(`/devices/${id}`);
            setRows((prev) => prev.filter((d) => d.id !== id));
            setSnack({open: true, text: 'Токен устройства отозван', kind: 'success'});
        } catch {
            setSnack({open: true, text: 'Не удалось отозвать токен', kind: 'error'});
        } finally {
            setBusyId(null);
            setConfirmId(null);
        }
    };
    return (
        <Stack spacing={1.5}>
            <Stack direction="row" alignItems="center" spacing={1}>
                <Typography variant="h5" fontWeight={700} color="white">My devices</Typography>
                <IconButton aria-label="refresh" onClick={load} disabled={isBusy} sx={{color: 'white'}}>
                    <RefreshIcon/>
                </IconButton>
            </Stack>

            {loading && (
                <Box display="flex" justifyContent="center" mt={6}>
                    <CircularProgress/>
                </Box>
            )}

            {!loading && error && (
                <Alert severity="error" variant="outlined">{error}</Alert>
            )}

            {!loading && !error && (
                <TableContainer component={Card} sx={{backgroundColor: '#111827', borderRadius: 0.5}}>
                    <Table size="medium">
                        <TableHead>
                            <TableRow>
                                <TableCell align="center" sx={{color: 'rgba(255,255,255,0.7)'}}>Device id</TableCell>
                                <TableCell align="center" sx={{color: 'rgba(255,255,255,0.7)'}}>Device name</TableCell>
                                <TableCell align="center" sx={{color: 'rgba(255,255,255,0.7)'}}>Last rotated</TableCell>
                                <TableCell align="center" sx={{color: 'rgba(255,255,255,0.7)'}}>Last used</TableCell>
                                <TableCell align="center" sx={{color: 'rgba(255,255,255,0.7)'}}>Actions</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {rows.length === 0 && (
                                <TableRow>
                                    <TableCell colSpan={4} sx={{color: 'rgba(255,255,255,0.6)'}}>
                                        Устройства не привязаны.
                                    </TableCell>
                                </TableRow>
                            )}
                            {rows.map((d) => (
                                <TableRow key={d.id} hover>
                                    <TableCell align="center" sx={{color: 'white'}}>{d.id}</TableCell>
                                    <TableCell align="center" sx={{color: 'white'}}>{d.name}</TableCell>
                                    <TableCell align="center" sx={{color: 'rgba(255,255,255,0.85)'}}>{fmtDate(d.last_rotated_at)}</TableCell>
                                    <TableCell align="center" sx={{color: 'rgba(255,255,255,0.85)'}}>{fmtDate(d.last_used_at)}</TableCell>
                                    <TableCell align="center">
                                        <Button
                                            size="small"
                                            color="error"
                                            variant="outlined"
                                            startIcon={<DeleteOutlineIcon/>}
                                            onClick={() => setConfirmId(d.id)}
                                            disabled={isBusy && busyId !== d.id}
                                        >
                                            Отозвать
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}

            <Card sx={{backgroundColor: '#111827', borderRadius: 0.5}}>
                <CardContent>
                    <Stack direction="row" alignItems="center" justifyContent="space-between">
                        <Box>
                            <Typography variant="h6" color="white" fontWeight={700}>Привязать новое
                                устройство</Typography>
                            <Typography variant="body2" sx={{color: 'rgba(255,255,255,0.65)'}}>
                                Нажмите «Привязать», чтобы сгенерировать токен для нового устройства.
                            </Typography>
                        </Box>
                        <Button
                            variant="contained"
                            size="large"
                            onClick={() => setPairOpen(true)}
                            disabled={busyId === 'pair'}
                        >
                            Привязать

                        </Button>
                    </Stack>
                </CardContent>
            </Card>
            <PairDeviceDialog
                open={pairOpen}
                onClose={() => setPairOpen(false)}
                onPaired={() => {
                    setSnack({open: true, text: 'Код сгенерирован. Проверьте устройство.', kind: 'success'});
                }}
            />
            {/* Диалог подтверждения отзыва */
            }
            <Dialog
                open={Boolean(confirmId)}
                onClose={() => setConfirmId(null)}
            >
                <DialogTitle>Отозвать токен устройства?</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Действие нельзя отменить. Устройство можно будет привязать снова.
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setConfirmId(null)}>Отмена</Button>
                    <Button color="error" variant="contained" onClick={() => revoke(confirmId!)}
                            disabled={busyId !== null}>
                        Отозвать
                    </Button>
                </DialogActions>
            </Dialog>

            <Snackbar
                open={snack.open}
                autoHideDuration={3500}
                onClose={() => setSnack((s) => ({...s, open: false}))}
                anchorOrigin={{vertical: 'bottom', horizontal: 'right'}}
            >
                <Alert
                    onClose={() => setSnack((s) => ({...s, open: false}))}
                    severity={snack.kind || 'success'}
                    variant="filled"
                    sx={{
                        bgcolor: snack.kind === 'error' ? 'rgba(239,68,68,0.2)' : 'rgba(34,197,94,0.2)',
                        color: snack.kind === 'error' ? '#fca5a5' : '#4ade80',
                        border: '1px solid rgba(255,255,255,0.15)',
                    }}
                >
                    {snack.text}
                </Alert>
            </Snackbar>
        </Stack>
    )
        ;
}