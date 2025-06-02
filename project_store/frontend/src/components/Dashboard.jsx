import React, { useEffect, useState } from "react";
import "./../App.css"; // Use existing styles
import "./Dashboard.css"; // Import specific styles for the dashboard

function Dashboard() {
    const [orders, setOrders] = useState([]);
    const [error, setError] = useState(null);

    const fetchOrders = async () => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/api/orders/", {
                headers: {
                    Authorization: `${tokenType} ${accessToken}`,
                },
            });

            if (!response.ok) {
                throw new Error("Failed to fetch orders.");
            }

            const data = await response.json();
            setOrders(data);
        } catch (err) {
            setError(err.message);
        }
    };

    useEffect(() => {
        if (!localStorage.getItem("access_token")) {
            navigate("/");
        } else {
            fetchOrders();
        }
    }, []);

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Your Orders</h1>
      {error && <p className="login-error">{error}</p>}

      {orders.length === 0 && !error ? (
        <p>No se han encontrado órdenes.</p>
      ) : (
        orders.map((order) => (
          <div key={order.id} className="order-card">
            <h2>Orden #{order.id}</h2>
            <p><strong>Estado:</strong> {order.status}</p>
            <p><strong>Fecha:</strong> {new Date(order.created_at).toLocaleString()}</p>

            <div className="order-items">
                <h3>Productos</h3>
                {order.items.map((item, idx) => (
                <div key={idx} className="order-item">
                    <div className="item-left">
                    <span className="item-title">{item.product.title}</span>
                    <span className="item-qty">Cantidad: {item.quantity}</span>
                    </div>
                    <div className="item-right">
                    <span className="item-price">{(item.product.price * item.quantity).toFixed(2)} €</span>
                    </div>
                </div>
                ))}
                <div className="order-total">
                <span>Total:</span>
                <strong>
                    {order.items
                    .reduce(
                        (sum, item) => sum + item.product.price * item.quantity,
                        0
                    )
                    .toFixed(2)} €
                </strong>
                </div>
            </div>
        </div>
        ))
      )}
    </div>
  );
}

export default Dashboard;
