import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://localhost:5000/auth/login', { email, password });
      localStorage.setItem('user', email);
      setMsg(res.data.message);
      setTimeout(() => navigate('/products'), 1500);
    } catch (err) {
      setMsg(err.response?.data?.error || 'Login failed');
    }
  };

  return (
    <div style={styles.container}>
      <h2>User Login</h2>
      <input type="email" placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
      <p>{msg}</p>
    </div>
  );
};

const styles = {
  container: { padding: 20, textAlign: 'center' }
};

export default Login;
