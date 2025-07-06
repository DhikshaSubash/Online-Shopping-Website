import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Cart = () => {
  const userEmail = localStorage.getItem('user');
  const navigate = useNavigate();

  const [cartItems, setCartItems] = useState([]);
  const [msg, setMsg] = useState('');

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const res = await axios.get(`http://localhost:5000/user/cart/${userEmail}`);
      setCartItems(res.data);
    } catch (err) {
      setMsg('Failed to load cart');
    }
  };

  const updateQuantity = async (product_id, quantity) => {
    try {
      const res = await axios.put('http://localhost:5000/user/update-cart', {
        user_email: userEmail,
        product_id,
        quantity
      });
      setMsg(res.data.message);
      fetchCart(); // refresh cart
    } catch (err) {
      setMsg(err.response?.data?.error || 'Error updating cart');
    }
  };

  const removeItem = async (product_id) => {
    try {
      await axios.post('http://localhost:5000/user/remove-from-cart', {
        user_email: userEmail,
        product_id
      });
      fetchCart();
    } catch (err) {
      setMsg('Error removing item');
    }
  };

  const placeOrder = async () => {
    try {
      const res = await axios.post('http://localhost:5000/user/place-order', {
        user_email: userEmail
      });
      setMsg(res.data.message);
      setTimeout(() => navigate('/order'), 1500); // redirect after order
    } catch (err) {
      setMsg(err.response?.data?.error || 'Order failed');
    }
  };

  return (
    <div style={styles.container}>
      <h2>Your Cart</h2>

      {cartItems.length === 0 ? (
        <p>Cart is empty</p>
      ) : (
        <div>
          {cartItems.map((item) => (
            <div key={item.product_id} style={styles.card}>
              <h4>{item.name}</h4>
              <p>Price: ₹{item.price}</p>
              <p>In Stock: {item.stock}</p>
              <p>Current Quantity: {item.quantity}</p>
              <input
                type="number"
                min="1"
                placeholder="Update Quantity"
                onChange={(e) => updateQuantity(item.product_id, parseInt(e.target.value))}
              />
              <button onClick={() => removeItem(item.product_id)}>Remove</button>
            </div>
          ))}
          <button onClick={placeOrder} style={{ marginTop: 20 }}>Place Order</button>
        </div>
      )}
      <p style={{ color: 'green' }}>{msg}</p>
    </div>
  );
};

const styles = {
  container: { padding: 20, textAlign: 'center' },
  card: {
    border: '1px solid #ccc',
    margin: '10px auto',
    padding: 15,
    maxWidth: 400,
    borderRadius: 10
  }
};

export default Cart;
