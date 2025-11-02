import {createTheme} from '@mui/material/styles';

const darkBg = '#0f172a';
const surface = '#111827';
const cardBg = '#1f2937';
const divider = 'rgba(255,255,255,0.08)';

export const theme = createTheme({
        palette: {
            mode: 'dark',
            primary: {
                main: '#3B82F6',
                contrastText: '#fff',
            },
            background: {
                default: darkBg,
                paper: surface,
            },
            text: {
                primary: '#E5E7EB',
                secondary: '#9CA3AF',
            },
            divider,
        },
        shape: {borderRadius: 14},
        typography: {
            fontFamily: 'Inter, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, "Helvetica Neue", Arial, "Apple Color Emoji", "Segoe UI Emoji"',
            h3: {fontWeight: 800, letterSpacing: -0.5},
            h4: {fontWeight: 700, letterSpacing: -0.2},
            button: {textTransform: 'none', fontWeight: 600},
        },
        components: {
            MuiCssBaseline: {
                styleOverrides: {
                    body: {
                        backgroundColor: darkBg,
                    },
                },
            },
            MuiPaper: {
                defaultProps: {elevation: 0},
                styleOverrides: {
                    root: {
                        backgroundColor: cardBg,
                        border: 'none',
                        backdropFilter: 'saturate(110%) blur(2px)',
                    },
                },
            },
            MuiCard: {
                styleOverrides: {
                    root: {
                        backgroundColor: cardBg,
                        border: 'none',
                        boxShadow: '0 8px 32px rgba(0,0,0,0.35)',
                    },
                },
            },
            MuiButton: {
                defaultProps: {variant: 'contained', disableElevation: true},
                styleOverrides: {
                    root: {
                        height: 44,
                        borderRadius: 12,
                    },
                },
            },
            MuiTextField: {
                defaultProps: {
                    variant: 'filled',
                    fullWidth: true,
                    size: 'medium',
                    slotProps: {inputLabel: {shrink: true}}, // пусть останется
                },
                styleOverrides: {
                    root: {
                        // Гарантируем, что именно "корневой блок инпута" имеет radius и режет всё внутри
                        '& .MuiFilledInput-root': {
                            borderRadius: 14,
                            overflow: 'hidden',             // ← главное: ничего не «выпирает» за радиус
                            backgroundClip: 'padding-box',  // ← убирает «срез» у теней/фона по углам
                        },
                        // На всякий случай уберём нижнее подчёркивание псевдоэлементов
                        '& .MuiFilledInput-root:before, & .MuiFilledInput-root:after': {
                            display: 'none',
                        },
                    },
                },
            },
            MuiInputLabel: {
                styleOverrides: {
                    root: {
                        '&.MuiInputLabel-filled': {
                            opacity: 0,
                            transform: 'translateY(-50%) scale(0.9)',
                            transition: 'opacity 0.2s ease, transform 0.2s ease',
                        },
                        color: 'rgba(255,255,255,0.6)',
                    },
                },
            },
            MuiFilledInput: {
                defaultProps: {disableUnderline: true},
                styleOverrides: {
                    root: {
                        borderRadius: 14,                // совпадает с TextField override выше
                        backgroundColor: '#121926',
                        ':hover': {backgroundColor: '#151b2e'},
                        '&.Mui-focused': {
                            backgroundColor: '#1a2136',
                            // Мягкая подсветка, которая не «режет» радиусы
                            boxShadow: 'inset 0 0 0 2px rgba(59,130,246,0.35)',
                            outline: '1px solid transparent',     // фикс артефактов рендера
                            backgroundClip: 'padding-box',
                        },
                        // Немного воздуха внутри
                        input: {
                            paddingTop: 14,
                            paddingBottom: 14,
                            '::placeholder': {
                                opacity: 1,
                                color: 'rgba(255,255,255,0.65)',
                                transition: 'opacity 0.2s ease',
                            },
                            ':focus::placeholder': {opacity: 0.35},
                        },
                    },
                },
            },
            MuiLink: {
                styleOverrides: {
                    root: {
                        color: '#93C5FD',
                        '&:hover': {textDecorationColor: '#93C5FD'},
                    },
                },
            },
            MuiDivider: {
                styleOverrides: {
                    root: {borderColor: divider},
                },
            },
        },
    })
;