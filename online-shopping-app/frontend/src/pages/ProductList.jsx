import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProductList = () => {
  const userEmail = localStorage.getItem('user');
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState('');
  const [quantities, setQuantities] = useState({});
  const [msg, setMsg] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async (query = '') => {
    try {
      const url = query
        ? `http://localhost:5000/products/search?q=${query}`
        : 'http://localhost:5000/products/';
      const res = await axios.get(url);
      setProducts(res.data);
    } catch (err) {
      console.error('Error fetching products', err);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchProducts(search);
  };

  const handleAddToCart = async (productId) => {
    const qty = quantities[productId] || 1;
    try {
      const res = await axios.post('http://localhost:5000/user/add-to-cart', {
        user_email: userEmail,
        product_id: productId,
        quantity: qty
      });
      setMsg(res.data.message);
    } catch (err) {
      setMsg(err.response?.data?.error || 'Failed to add to cart');
    }
  };

  return (
    <div style={styles.container}>
      <h2>Available Products</h2>

      <form onSubmit={handleSearch} style={styles.searchBox}>
        <input
          type="text"
          placeholder="Search by name"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>

      <div style={styles.productList}>
        {products.map((p) => (
          <div key={p.id} style={styles.card}>
            <h4>{p.name}</h4>
            <p>Price: ₹{p.price}</p>
            <p>Stock: {p.stock}</p>
            <input
              type="number"
              min="1"
              placeholder="Quantity"
              value={quantities[p.id] || ''}
              onChange={(e) =>
                setQuantities({ ...quantities, [p.id]: e.target.value })
              }
            />
            <button onClick={() => handleAddToCart(p.id)}>Add to Cart</button>
          </div>
        ))}
      </div>

      <p style={{ color: 'green' }}>{msg}</p>
    </div>
  );
};

const styles = {
  container: { padding: 20, textAlign: 'center' },
  searchBox: { marginBottom: 20 },
  productList: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: 20
  },
  card: {
    border: '1px solid #ccc',
    borderRadius: 10,
    padding: 15,
    width: 200,
    boxShadow: '0 0 5px rgba(0,0,0,0.2)'
  }
};

export default ProductList;
