import axios from 'axios';

export type ApiError = {
  code: string
  message?: string
  status?: number
  field?: string
  details?: unknown
};

export function extractApiError(err: unknown): ApiError {
  if (axios.isAxiosError(err) && !err.response) {
    return { code: 'NETWORK_ERROR', message: 'Сетевая ошибка' };
  }

  if (!axios.isAxiosError(err) || !err.response) {
    return { code: 'UNKNOWN_ERROR', message: (err as any)?.message || 'Неизвестная ошибка.' };
  }

  const { status, data } = err.response;
  const detail = (data as any)?.detail ?? (data as any)?.error ?? data;

  if (typeof detail === 'string') {
    return { code: detail, status, details: data };
  }

  if (typeof detail === 'object' && detail) {
      const code = (detail as any).code
          || (detail as any).error_code
          || (data as any).code
          || (data as any).error_code;

      const message = (detail as any).message
          || (detail as any).error
          || (data as any).message;

      const field = (detail as any).field;

      if (code) {
          return {code: code, message: message, status: status, field: field, details: data};
      }
  }

  return { code: 'UNKNOWN_ERROR', message: 'Неизвестная ошибка.' };

}