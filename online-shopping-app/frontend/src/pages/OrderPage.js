import React, { useEffect, useState } from 'react';
import axios from 'axios';

const OrderPage = () => {
  const userEmail = localStorage.getItem('user');
  const [order, setOrder] = useState(null);
  const [msg, setMsg] = useState('');

  useEffect(() => {
    fetchLatestOrder();
  }, []);

  const fetchLatestOrder = async () => {
    try {
      const res = await axios.get(`http://localhost:5000/user/latest-order/${userEmail}`);
      setOrder(res.data);
    } catch (err) {
      setMsg('No recent order found');
    }
  };

  return (
    <div style={styles.container}>
      <h2>Order Confirmation</h2>
      {msg && <p>{msg}</p>}

      {order ? (
        <div style={styles.card}>
          <p><strong>Order ID:</strong> {order.order_id}</p>
          <p><strong>Date:</strong> {order.date}</p>
          <p><strong>Total Price:</strong> ₹{order.total_price}</p>
          <h4>Items:</h4>
          <ul>
            {order.items.map((item, index) => (
              <li key={index}>
                {item.name} × {item.quantity} @ ₹{item.price} each
              </li>
            ))}
          </ul>
        </div>
      ) : (
        !msg && <p>Loading order...</p>
      )}
    </div>
  );
};

const styles = {
  container: { padding: 20, textAlign: 'center' },
  card: {
    border: '1px solid #ccc',
    padding: 20,
    maxWidth: 500,
    margin: '0 auto',
    borderRadius: 10,
    boxShadow: '0 0 8px rgba(0,0,0,0.1)'
  }
};

export default OrderPage;
