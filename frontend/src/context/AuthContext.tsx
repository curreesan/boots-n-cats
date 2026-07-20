import { useState, useEffect, type ReactNode } from "react";
import type { User } from "../types/user";
import {
  getCurrentUser,
  loginUser,
  registerUser,
  logoutUser,
} from "../api/auth";
import { AuthContext } from "./authContextObject";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function checkExistingSession() {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
      setLoading(false);
    }

    checkExistingSession();
  }, []);

  async function login(email: string, password: string) {
    const loggedInUser = await loginUser(email, password);
    setUser(loggedInUser);
  }

  async function register(email: string, name: string, password: string) {
    const newUser = await registerUser(email, name, password);
    setUser(newUser);
  }

  async function logout() {
    await logoutUser();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
