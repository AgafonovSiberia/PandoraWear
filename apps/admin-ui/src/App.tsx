import { Routes, Route, Navigate } from 'react-router-dom'
import SignUpCard from './features/auth/SignUpCard'
import LoginCard from './features/auth/LoginCard'

import ProtectedLayout from './layouts/ProtectedLayout';
import ProfilePage from './features/app/profile/ProfilePage';
// import DevicesPage from './features/app/devices/DevicesPage';
// import SettingsPage from './features/app/settings/SettingsPage';
import MainAppLayout from './layouts/MainAppLayout';

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginCard />} />
      <Route path="/register" element={<SignUpCard />} />

      {/* защищённая зона */}
      <Route element={<ProtectedLayout />}>
        <Route element={<MainAppLayout />}>
          <Route path="/app/profile" element={<ProfilePage />} />
          {/*<Route path="/app/devices" element={<DevicesPage />} />*/}
          {/*<Route path="/app/settings" element={<SettingsPage />} />*/}
        </Route>
      </Route>

       <Route path="/" element={<Navigate to="/app/devices" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}