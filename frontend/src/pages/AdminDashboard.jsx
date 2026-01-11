import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api';
import AdminAnalytics from '../components/AdminAnalytics';
import './AdminDashboard.css'; 

function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('analytics'); // 'analytics' or 'management'
  const [users, setUsers] = useState([]);
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [stock, setStock] = useState('');
  const [image, setImage] = useState(null);
  const [date, setDate] = useState('');
  const [deleteId, setDeleteId] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    API.get('/admin/users').then(res => setUsers(res.data));
    API.get('/admin/orders').then(res => setOrders(res.data));
    API.get('/admin/products').then(res => setProducts(res.data));
  }, []);

  const addProduct = () => {
    if (!name || !price || !stock || !image) {
      alert('Please fill all product fields and select an image');
      return;
    }

    const formData = new FormData();
    formData.append('name', name);
    formData.append('price', price);
    formData.append('stock', stock);
    formData.append('image', image);

    API.post('/admin/add-product', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
      .then(() => {
        alert('Product added');
        setName('');
        setPrice('');
        setStock('');
        setImage(null);
        return API.get('/admin/products');
      })
      .then(res => setProducts(res.data))
      .catch(() => alert('Error adding product'));
  };

  const deleteProduct = () => {
    if (!deleteId) {
      alert('Please enter product ID to delete');
      return;
    }

    API.delete(`/admin/remove-product/${deleteId}`)
      .then(() => {
        alert('Product removed');
        setDeleteId('');
        return API.get('/admin/products');
      })
      .then(res => setProducts(res.data))
      .catch(() => alert('Error deleting product'));
  };

  const filterOrders = () => {
    if (!date) {
      alert('Please enter a date to filter');
      return;
    }
    API.get(`/admin/orders?date=${date}`).then(res => {
      setOrders(res.data);
      setDate('');
    });
  };

  const logout = () => {
    navigate('/');
  };

  return (
    <div className="admin-dashboard-container">
      <div className="admin-header">
        <h2>Admin Dashboard</h2>
        <button className="logout-button" onClick={logout}>Logout</button>
      </div>

      {/* Tab Navigation */}
      <div className="admin-tabs">
        <button 
          className={`tab-button ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          📊 Analytics
        </button>
        <button 
          className={`tab-button ${activeTab === 'management' ? 'active' : ''}`}
          onClick={() => setActiveTab('management')}
        >
          ⚙️ Management
        </button>
      </div>

      {/* Analytics Tab */}
      {activeTab === 'analytics' && (
        <AdminAnalytics />
      )}

      {/* Management Tab */}
      {activeTab === 'management' && (
        <div className="management-content">

      <section>
        <h3>Add Product</h3>
        <div className="input-group">
          <input
            placeholder="Name"
            value={name}
            onChange={e => setName(e.target.value)}
          />
          <input
            type="number"
            placeholder="Price"
            value={price}
            onChange={e => setPrice(e.target.value)}
          />
          <input
            type="number"
            placeholder="Stock"
            value={stock}
            onChange={e => setStock(e.target.value)}
          />
          <input
            type="file"
            accept="image/*"
            onChange={e => setImage(e.target.files[0])}
          />
          <button onClick={addProduct}>Add</button>
        </div>
      </section>

      <section>
        <h3>Delete Product</h3>
        <div className="input-group">
          <input
            placeholder="Product ID"
            value={deleteId}
            onChange={e => setDeleteId(e.target.value)}
          />
          <button onClick={deleteProduct}>Delete</button>
        </div>
      </section>

      <section>
        <h3>Products</h3>
        {products.length === 0 ? (
          <p>No products found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Image</th>
              </tr>
            </thead>
            <tbody>
              {products.map(p => (
                <tr key={p.ID}>
                  <td>{p.ID}</td>
                  <td>{p.name}</td>
                  <td>₹{p.price}</td>
                  <td>{p.stock}</td>
                  <td>
                    {p.image ? (
                      <img
                        src={p.image}
                        alt={p.name}
                        className="product-image"
                      />
                    ) : (
                      'No Image'
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section>
        <h3>Filter Orders</h3>
        <div className="input-group">
          <input
            placeholder="YYYY-MM-DD"
            value={date}
            onChange={e => setDate(e.target.value)}
          />
          <button onClick={filterOrders}>Filter</button>
        </div>
      </section>

      <section>
        <h3>Orders</h3>
        {orders.length === 0 ? (
          <p>No orders found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Order ID</th>
                <th>User Email</th>
                <th>Amount</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(o => (
                <tr key={o.order_id}>
                  <td>{o.order_id}</td>
                  <td>{o.user_email || o.email}</td>
                  <td>₹{o.total_price || o.amount}</td>
                  <td>{o.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section>
        <h3>Users</h3>
        {users.length === 0 ? (
          <p>No users found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Email</th>
              </tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.email}>
                  <td>{u.email}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        </section>
        </div>
      )}
    </div>
  );
}

export default AdminDashboard;
