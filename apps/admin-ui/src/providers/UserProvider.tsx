import React, { createContext, useContext, useEffect, useState } from 'react';
import { api } from '../api/axios';

export type CurrentUser = {
  username: string;
  email: string;
  full_name?: string;
} | null;

type Ctx = {
  user: CurrentUser;
  loading: boolean;
  reload: () => Promise<void>;
  setUser: React.Dispatch<React.SetStateAction<CurrentUser>>;
};

const UserCtx = createContext<Ctx | undefined>(undefined);

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<CurrentUser>(null);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const r = await api.get('/users/me'); // cookie уедет автоматически
      setUser(r.data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  return (
    <UserCtx.Provider value={{ user, loading, reload: load, setUser }}>
      {children}
    </UserCtx.Provider>
  );
}

export function useUser() {
  const ctx = useContext(UserCtx);
  if (!ctx) throw new Error('useUser must be used inside <UserProvider>');
  return ctx;
}