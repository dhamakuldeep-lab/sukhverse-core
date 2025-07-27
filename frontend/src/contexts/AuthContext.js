import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      // TODO: Decode token or fetch user from auth API
      setUser({});
    }
  }, [token]);

  const login = async (email, password) => {
    const resp = await axios.post(process.env.REACT_APP_AUTH_API_URL + '/login', null, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      params: { username: email, password },
    });
    const { access_token } = resp.data;
    localStorage.setItem('token', access_token);
    setToken(access_token);
    setUser({}); // In real implementation decode JWT to get user info
  };

  const register = async (email, password, role) => {
    /**
     * Send registration request.  A role can be supplied to allow the backend to assign
     * appropriate permissions at sign‑up.  If the backend chooses to ignore the role, it
     * will simply be discarded.  Including a role here enables the UI to capture the
     * user’s desired profile (e.g. student or trainer) during registration.
     */
    await axios.post(
      process.env.REACT_APP_AUTH_API_URL + '/register',
      { email, password, role }
    );
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}