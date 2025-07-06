import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div style={styles.container}>
      <h1>Welcome to ShopSmart</h1>
      <p>Your one-stop shop for all your needs.</p>

      <div style={styles.buttons}>
        <Link to="/signup"><button>Sign Up</button></Link>
        <Link to="/login"><button>Login</button></Link>
        <Link to="/admin-login"><button>Admin Login</button></Link>
      </div>

      <div style={styles.footer}>
        <h4>About Us</h4>
        <p>We provide a seamless online shopping experience with the best products at the best prices.</p>
        <h4>Contact</h4>
        <p>Email: support@shopsmart.com</p>
      </div>
    </div>
  );
};

const styles = {
  container: { textAlign: 'center', padding: 30 },
  buttons: { margin: 20 },
  footer: { marginTop: 50 }
};

export default LandingPage;
