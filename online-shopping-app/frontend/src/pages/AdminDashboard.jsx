// src/pages/admin/AdminDashboard.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AdminDashboard = () => {
  const [tab, setTab] = useState('users');
  const [users, setUsers] = useState([]);
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');
  const [newProduct, setNewProduct] = useState({ name: '', price: '', stock: '' });
  const [removeId, setRemoveId] = useState('');
  const adminEmail = localStorage.getItem('admin');

  const fetchUsers = async () => {
    const res = await axios.get('http://localhost:5000/api/users');
    setUsers(res.data);
  };

  const fetchOrders = async () => {
    const res = await axios.get('http://localhost:5000/api/orders', {
      params: { from: fromDate, to: toDate }
    });
    setOrders(res.data);
  };

  const addProduct = async () => {
    await axios.post('http://localhost:5000/api/add-product', newProduct);
    alert('Product added');
    setNewProduct({ name: '', price: '', stock: '' });
  };

  const deleteProduct = async () => {
    try {
      await axios.delete(`http://localhost:5000/api/remove-product/${removeId}`);
      alert('Product removed');
      setRemoveId('');
    } catch (err) {
      alert('Product not found');
    }
  };

  const logout = () => {
    localStorage.removeItem('admin');
    window.location.href = '/admin/login';
  };

  useEffect(() => {
    if (tab === 'users') fetchUsers();
    if (tab === 'orders') fetchOrders();
  }, [tab]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
      <div className="mb-4 space-x-4">
        <button onClick={() => setTab('users')} className="bg-gray-300 px-3 py-1 rounded">Users</button>
        <button onClick={() => setTab('orders')} className="bg-gray-300 px-3 py-1 rounded">Orders</button>
        <button onClick={() => setTab('add')} className="bg-gray-300 px-3 py-1 rounded">Add Product</button>
        <button onClick={() => setTab('remove')} className="bg-gray-300 px-3 py-1 rounded">Remove Product</button>
        <button onClick={logout} className="bg-red-600 text-white px-3 py-1 rounded">Logout</button>
      </div>

      {tab === 'users' && (
        <div>
          <h2 className="font-semibold">All Users</h2>
          <ul className="list-disc ml-5">
            {users.map(u => <li key={u.email}>{u.email}</li>)}
          </ul>
        </div>
      )}

      {tab === 'orders' && (
        <div>
          <div className="flex gap-4 mb-2">
            <input type="date" value={fromDate} onChange={e => setFromDate(e.target.value)} className="border p-1" />
            <input type="date" value={toDate} onChange={e => setToDate(e.target.value)} className="border p-1" />
            <button onClick={fetchOrders} className="bg-blue-600 text-white px-3 py-1 rounded">Filter</button>
          </div>
          <ul>
            {orders.map(o => (
              <li key={o.order_id}>
                Order #{o.order_id} - {o.user_email} - ₹{o.total_price} - {o.date}
              </li>
            ))}
          </ul>
        </div>
      )}

      {tab === 'add' && (
        <div>
          <h2 className="font-semibold mb-2">Add Product</h2>
          <input type="text" placeholder="Name" value={newProduct.name} onChange={e => setNewProduct({ ...newProduct, name: e.target.value })} className="border p-1 mr-2" />
          <input type="number" placeholder="Price" value={newProduct.price} onChange={e => setNewProduct({ ...newProduct, price: e.target.value })} className="border p-1 mr-2" />
          <input type="number" placeholder="Stock" value={newProduct.stock} onChange={e => setNewProduct({ ...newProduct, stock: e.target.value })} className="border p-1 mr-2" />
          <button onClick={addProduct} className="bg-green-600 text-white px-3 py-1 rounded">Add</button>
        </div>
      )}

      {tab === 'remove' && (
        <div>
          <h2 className="font-semibold mb-2">Remove Product by ID</h2>
          <input type="text" placeholder="Product ID" value={removeId} onChange={e => setRemoveId(e.target.value)} className="border p-1 mr-2" />
          <button onClick={deleteProduct} className="bg-red-500 text-white px-3 py-1 rounded">Remove</button>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
