import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line, Bar, Pie, Doughnut } from 'react-chartjs-2';
import API from '../api';
import './AdminAnalytics.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function AdminAnalytics() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const [revenueRes, ordersRes, productsRes, customersRes, conversionRes] = await Promise.all([
        API.get('/admin/analytics/revenue'),
        API.get('/admin/analytics/orders'),
        API.get('/admin/analytics/products'),
        API.get('/admin/analytics/customers'),
        API.get('/admin/analytics/conversion')
      ]);

      setAnalytics({
        revenue: revenueRes.data,
        orders: ordersRes.data,
        products: productsRes.data,
        customers: customersRes.data,
        conversion: conversionRes.data
      });
      setLoading(false);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="analytics-loading">Loading analytics...</div>;
  }

  if (!analytics) {
    return <div className="analytics-error">Failed to load analytics</div>;
  }

  // Revenue Line Chart Data
  const revenueChartData = {
    labels: analytics.revenue.daily_revenue.map(item => {
      const date = new Date(item.date);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }),
    datasets: [
      {
        label: 'Daily Revenue (₹)',
        data: analytics.revenue.daily_revenue.map(item => item.revenue),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4
      }
    ]
  };

  // Orders Bar Chart Data
  const ordersChartData = {
    labels: analytics.orders.daily_orders.map(item => {
      const date = new Date(item.date);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }),
    datasets: [
      {
        label: 'Daily Orders',
        data: analytics.orders.daily_orders.map(item => item.count),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }
    ]
  };

  // Product Distribution Pie Chart
  const productChartData = {
    labels: analytics.products.product_distribution.map(item => item.name),
    datasets: [
      {
        label: 'Revenue by Product',
        data: analytics.products.product_distribution.map(item => item.revenue),
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 159, 64, 0.6)',
          'rgba(199, 199, 199, 0.6)',
          'rgba(83, 102, 255, 0.6)',
          'rgba(255, 99, 255, 0.6)',
          'rgba(99, 255, 132, 0.6)'
        ],
        borderWidth: 2
      }
    ]
  };

  // Customer Types Doughnut Chart
  const customerTypes = analytics.customers.customer_types;
  const customerChartData = {
    labels: Object.keys(customerTypes),
    datasets: [
      {
        label: 'Customers',
        data: Object.values(customerTypes),
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(255, 99, 132, 0.6)'
        ],
        borderWidth: 2
      }
    ]
  };

  // Conversion Metrics Doughnut Chart
  const conversionChartData = {
    labels: ['Users with Orders', 'Users without Orders'],
    datasets: [
      {
        label: 'Users',
        data: [
          analytics.conversion.users_with_orders,
          analytics.conversion.users_without_orders
        ],
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 99, 132, 0.6)'
        ],
        borderWidth: 2
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top'
      },
      title: {
        display: true,
        position: 'top'
      }
    }
  };

  return (
    <div className="admin-analytics">
      <h2 className="analytics-title">📊 Analytics Dashboard</h2>

      {/* Key Metrics Cards */}
      <div className="metrics-grid">
        <div className="metric-card revenue">
          <div className="metric-icon">💰</div>
          <div className="metric-content">
            <h3>Total Revenue</h3>
            <p className="metric-value">₹{analytics.revenue.total_revenue.toLocaleString('en-IN')}</p>
          </div>
        </div>

        <div className="metric-card orders">
          <div className="metric-icon">📦</div>
          <div className="metric-content">
            <h3>Total Orders</h3>
            <p className="metric-value">{analytics.orders.total_orders}</p>
          </div>
        </div>

        <div className="metric-card customers">
          <div className="metric-icon">👥</div>
          <div className="metric-content">
            <h3>Total Users</h3>
            <p className="metric-value">{analytics.customers.total_users}</p>
          </div>
        </div>

        <div className="metric-card conversion">
          <div className="metric-icon">📈</div>
          <div className="metric-content">
            <h3>Conversion Rate</h3>
            <p className="metric-value">{analytics.conversion.conversion_rate}%</p>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-container">
        {/* Revenue Analytics */}
        <div className="chart-section">
          <h3>💵 Revenue Analytics</h3>
          <div className="chart-wrapper">
            <Line data={revenueChartData} options={{...chartOptions, plugins: {...chartOptions.plugins, title: {display: true, text: 'Daily Revenue Trend (Last 30 Days)'}}}} />
          </div>
          <div className="stats-row">
            <div className="stat-item">
              <span className="stat-label">Total Revenue:</span>
              <span className="stat-value">₹{analytics.revenue.total_revenue.toLocaleString('en-IN')}</span>
            </div>
          </div>
        </div>

        {/* Orders Analytics */}
        <div className="chart-section">
          <h3>📦 Orders Analytics</h3>
          <div className="chart-wrapper">
            <Bar data={ordersChartData} options={{...chartOptions, plugins: {...chartOptions.plugins, title: {display: true, text: 'Daily Orders (Last 30 Days)'}}}} />
          </div>
          <div className="stats-row">
            <div className="stat-item">
              <span className="stat-label">Total Orders:</span>
              <span className="stat-value">{analytics.orders.total_orders}</span>
            </div>
          </div>
        </div>

        {/* Product Analytics */}
        <div className="chart-section">
          <h3>🛍️ Product Analytics</h3>
          
          <div className="product-stats-grid">
            <div className="product-list">
              <h4>Top Selling Products</h4>
              <table className="product-table">
                <thead>
                  <tr>
                    <th>Product</th>
                    <th>Sold</th>
                    <th>Revenue</th>
                  </tr>
                </thead>
                <tbody>
                  {analytics.products.top_products.slice(0, 5).map(product => (
                    <tr key={product.id}>
                      <td>{product.name}</td>
                      <td>{product.total_sold}</td>
                      <td>₹{product.total_revenue.toLocaleString('en-IN')}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="chart-wrapper pie">
              <Pie data={productChartData} options={{...chartOptions, plugins: {...chartOptions.plugins, title: {display: true, text: 'Revenue Distribution'}}}} />
            </div>
          </div>
        </div>

        {/* Customer Analytics */}
        <div className="chart-section">
          <h3>👥 Customer Analytics</h3>
          
          <div className="customer-stats-grid">
            <div className="chart-wrapper doughnut">
              <Doughnut data={customerChartData} options={{...chartOptions, plugins: {...chartOptions.plugins, title: {display: true, text: 'Customer Types'}}}} />
            </div>

            <div className="customer-details">
              <h4>Customer Breakdown</h4>
              {Object.entries(customerTypes).map(([type, count]) => (
                <div key={type} className="customer-type-item">
                  <span className="customer-type-label">{type}:</span>
                  <span className="customer-type-value">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Conversion Metrics */}
        <div className="chart-section">
          <h3>📈 Conversion Metrics</h3>
          
          <div className="conversion-grid">
            <div className="chart-wrapper doughnut">
              <Doughnut data={conversionChartData} options={{...chartOptions, plugins: {...chartOptions.plugins, title: {display: true, text: 'User Conversion'}}}} />
            </div>

            <div className="conversion-details">
              <h4>Conversion Statistics</h4>
              <div className="conversion-item">
                <span className="conversion-label">Total Users:</span>
                <span className="conversion-value">{analytics.conversion.total_users}</span>
              </div>
              <div className="conversion-item">
                <span className="conversion-label">Users with Orders:</span>
                <span className="conversion-value">{analytics.conversion.users_with_orders}</span>
              </div>
              <div className="conversion-item">
                <span className="conversion-label">Users without Orders:</span>
                <span className="conversion-value">{analytics.conversion.users_without_orders}</span>
              </div>
              <div className="conversion-item highlight">
                <span className="conversion-label">Conversion Rate:</span>
                <span className="conversion-value">{analytics.conversion.conversion_rate}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminAnalytics;
