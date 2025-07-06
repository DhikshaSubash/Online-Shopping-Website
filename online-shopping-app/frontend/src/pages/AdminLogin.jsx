// src/pages/admin/AdminLogin.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AdminLogin = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://localhost:5000/api/admin/login', {
        email,
        password,
      });
      if (res.data.message) {
        localStorage.setItem('admin', email);
        navigate('/admin/dashboard');
      }
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto mt-20 border rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Admin Login</h2>
      <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} className="block w-full mb-3 p-2 border" />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} className="block w-full mb-3 p-2 border" />
      {error && <p className="text-red-500">{error}</p>}
      <button onClick={handleLogin} className="bg-blue-600 text-white px-4 py-2 rounded">Login</button>
    </div>
  );
};

export default AdminLogin;
