import { Routes, Route, Navigate } from 'react-router-dom';

import SignUpCard from './features/auth/SignUpCard';
import LoginCard from './features/auth/LoginCard';

import ProtectedLayout from './layouts/ProtectedLayout';
import MainAppLayout from '@/layouts/MainAppLayout';

import ProfilePage from '@/features/app/profile/ProfilePage';
import DevicesPage from '@/features/app/devices/DevicesPage';
import SettingsPage from '@/features/app/settings/SettingsPage';

export default function App() {
  return (
    <Routes>
      {/* Публичные маршруты */}
      <Route path="/login" element={<LoginCard />} />
      <Route path="/register" element={<SignUpCard />} />

      {/* Защищённая зона */}
      <Route element={<ProtectedLayout />}>
        <Route path="/app" element={<MainAppLayout />}>
          {/* /app -> /app/devices */}
          <Route index element={<Navigate to="devices" replace />} />

          {/* Вложенные страницы */}
          <Route path="profile" element={<ProfilePage />} />
          <Route path="devices" element={<DevicesPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>
      </Route>

      {/* Редиректы по умолчанию */}
      <Route path="/" element={<Navigate to="/app/devices" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
