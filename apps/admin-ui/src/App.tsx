import { Routes, Route, Navigate } from 'react-router-dom'
import SignUpCard from './features/auth/SignUpCard'
import LoginCard from './features/auth/LoginCard'


export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginCard />} />
      <Route path="/register" element={<SignUpCard />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}