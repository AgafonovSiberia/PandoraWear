import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Collapse,
    Link,
    Snackbar,
    Stack,
    TextField,
    Typography,
} from '@mui/material';
import {useForm} from 'react-hook-form';
import {z} from 'zod';
import {zodResolver} from '@hookform/resolvers/zod';
import NotificationsNoneOutlinedIcon from '@mui/icons-material/NotificationsNoneOutlined';
import {api} from '@/api/axios.ts';
import {extractApiError} from '@/api/errors.ts';
import React, {useEffect, useState} from 'react';
import {Link as RouterLink, useNavigate} from 'react-router-dom';

const loginSchema = z.object({
    email: z.email('Некорректный email'),   // ✅ исправлено
    password: z.string().min(6, 'Минимум 6 символов'),
});
type LoginForm = z.infer<typeof loginSchema>;

export default function LoginCard() {
    const {
        register,
        handleSubmit,
        formState: {errors, isSubmitting},
        watch,
    } = useForm<LoginForm>({
        resolver: zodResolver(loginSchema),
        mode: 'onChange',
    });

    const [serverError, setServerError] = useState<string | null>(null);
    const [emailValue, passwordValue] = watch(['email', 'password']);
    useEffect(() => {
        setServerError(null);
    }, [emailValue, passwordValue]);

    const [registerSuccess, setRegisterSuccess] = useState(false);
    useEffect(() => {
        const t = sessionStorage.getItem('toast');
        if (t === 'registered') {
            setRegisterSuccess(true);
            sessionStorage.removeItem('toast');
        }
    }, []);

    const handleToastClose = (_?: React.SyntheticEvent | Event, reason?: string) => {
        if (reason === 'clickaway') return;
        setRegisterSuccess(false);
    };
    const navigate = useNavigate();

    const onSubmit = async (data: LoginForm) => {
        try {
            setServerError(null);
            const res = await api.post('/users/login', data);
            const token = res.data.access_token
            localStorage.setItem('token', token);
            api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            console.log('Авторизация успешна:', res.data);
            navigate('/')
        } catch (e: any) {
            const err = extractApiError(e);
            const uxMessage = (() => {
                switch (err.code) {
                    case 'USER_NOT_FOUND':
                        return 'Пользователь с таким email не зарегистрирован';
                    case 'INVALID_CREDENTIALS':
                        return 'Неверный email или пароль';
                    case 'NETWORK_ERROR':
                        return 'Произошла ошибка. Попробуйте позже.';
                    default:
                        return err.message || 'Произошла ошибка. Попробуйте позже.';
                }
            })();
            setServerError(uxMessage);
            console.error('API Error:', err);
        }
    };

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
            {/* toast */}
            <Snackbar
                open={registerSuccess}
                autoHideDuration={4000}
                onClose={handleToastClose}
                anchorOrigin={{vertical: 'bottom', horizontal: 'right'}}
            >
                <Alert
                    onClose={handleToastClose}
                    severity="success"
                    variant="filled"
                    sx={{
                        bgcolor: 'rgba(34,197,94,0.2)',
                        color: '#4ade80',
                        border: '1px solid rgba(34,197,94,0.35)',
                        backdropFilter: 'saturate(120%) blur(2px)',
                        boxShadow: '0 8px 24px rgba(0,0,0,0.35)',
                    }}
                >
                    Регистрация завершена. Войдите в свой аккаунт.
                </Alert>
            </Snackbar>

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
                        <NotificationsNoneOutlinedIcon sx={{fontSize: 36}}/>
                        <Typography variant="h4" fontWeight={800}>
                            Pandora Custom API
                        </Typography>
                    </Stack>
                </Box>

                <Box display="flex" justifyContent="center">
                    <Card sx={{maxWidth: 520, width: '100%'}}>
                        <CardContent sx={{p: {xs: 3, md: 4}}}>
                            <Typography variant="h5" fontWeight={700} mb={2}>
                                Log in
                            </Typography>

                            <form onSubmit={handleSubmit(onSubmit)}>
                                <Stack spacing={2.2}>
                                    <TextField
                                        type="email"
                                        autoComplete="email"
                                        {...register('email')}
                                        slotProps={{input: {'aria-label': 'Email', placeholder: 'Email'}}}
                                        error={!!errors.email}
                                        helperText={errors.email?.message}
                                    />
                                    <TextField
                                        type="password"
                                        autoComplete="current-password"
                                        {...register('password')}
                                        slotProps={{input: {'aria-label': 'Password', placeholder: 'Password'}}}
                                        error={!!errors.password}
                                        helperText={errors.password?.message}
                                    />

                                    <Button type="submit" size="large" disabled={isSubmitting}>
                                        {isSubmitting ? 'Загрузка...' : 'Войти'}
                                    </Button>

                                    <Typography variant="body2" color="text.secondary" textAlign="center">
                                        Нет аккаунта?{' '}
                                        <Link
                                            component={RouterLink}
                                            to="/register"
                                            underline="hover"
                                            sx={{color: 'primary.main', fontWeight: 500}}
                                        >
                                            Зарегистрироваться
                                        </Link>
                                    </Typography>

                                    <Collapse in={Boolean(serverError)} sx={{mt: 1}}>
                                        <Alert
                                            severity="error"
                                            variant="outlined"
                                            sx={{
                                                borderColor: 'rgba(239,68,68,0.35)',
                                                color: 'error.main',
                                                bgcolor: 'transparent',
                                                textAlign: 'center',
                                            }}
                                        >
                                            {serverError}
                                        </Alert>
                                    </Collapse>
                                </Stack>
                            </form>
                        </CardContent>
                    </Card>
                </Box>
            </Box>
        </Box>
    );
}
