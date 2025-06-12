import React, { useEffect, useState } from "react";
import "./../App.css"; // Use existing styles
import "./Dashboard.css"; // Import specific styles for the dashboard
import { useNavigate } from "react-router-dom";
import { FaFileExcel, FaFileCsv, FaFilePdf } from 'react-icons/fa'; // Import icons

function Dashboard() {
    const [orders, setOrders] = useState([]);
    const [error, setError] = useState(null);
    const [userInfo, setUserInfo] = useState({ userId: "", role: "", userName: "" });
    const [products, setProducts] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [selectedOrderId, setSelectedOrderId] = useState(null);
    const [loading, setLoading] = useState(false); // Estado para el indicador de carga
    const navigate = useNavigate();

    const handleUnauthorized = async () => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";
        try {
            if (accessToken) {
                await fetch("http://localhost:8000/api/auth/logout", {
                    method: "POST",
                    headers: {
                        Authorization: `${tokenType} ${accessToken}`,
                    },
                });
            }
        } catch (err) {
            // Ignore logout errors
        } finally {
            localStorage.removeItem("access_token");
            localStorage.removeItem("token_type");
            navigate("/");
        }
    };

    const fetchOrders = async () => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        setLoading(true); // Activar el indicador de carga

        try {
            const response = await fetch("http://localhost:8000/api/orders/", {
                headers: {
                    Authorization: `${tokenType} ${accessToken}`,
                },
            });

            if (response.status === 401) {
                handleUnauthorized();
                return;
            }

            if (!response.ok) {
                throw new Error("Failed to fetch orders.");
            }

            const data = await response.json();
            setOrders(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false); // Desactivar el indicador de carga
        }
    };

    const fetchProducts = async () => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        setLoading(true); // Activar el indicador de carga

        try {
            const response = await fetch("http://localhost:8000/api/products/", {
                headers: {
                    Authorization: `${tokenType} ${accessToken}`,
                },
            });

            if (response.status === 401) {
                handleUnauthorized();
                return;
            }

            if (!response.ok) {
                throw new Error("Failed to fetch products.");
            }

            const data = await response.json();
            setProducts(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false); // Desactivar el indicador de carga
        }
    };

    useEffect(() => {
        const accessToken = localStorage.getItem("access_token");
        if (!accessToken) {
            navigate("/");
        } else {
            const tokenData = JSON.parse(atob(accessToken.split('.')[1]));
            setUserInfo({ userId: tokenData.user_id, role: tokenData.role, userName: tokenData.user_username });
            fetchOrders();
        }
    }, []);

    const updateQuantity = async (orderId, productId, newQuantity) => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        setLoading(true); // Activar el indicador de carga

        try {
            const response = await fetch(`http://localhost:8000/api/orders/${orderId}/products/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `${tokenType} ${accessToken}`,
                },
                body: JSON.stringify({
                    order_id: orderId,
                    product_id: productId,
                    quantity: newQuantity,
                }),
            });

            if (response.status === 401) {
                handleUnauthorized();
                return;
            }

            if (!response.ok) {
                throw new Error("Failed to update item quantity.");
            }

        } catch (err) {
            setError(err.message);
        } finally {
            fetchOrders();
        }
    };

    const addProductToOrder = async (orderId, productId) => {
        setShowModal(false);
        
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        setLoading(true); // Activar el indicador de carga

        try {
            const response = await fetch(`http://localhost:8000/api/orders/${orderId}/products/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `${tokenType} ${accessToken}`,
                },
                body: JSON.stringify({
                    order_id: orderId,
                    product_id: productId,
                    quantity: 1,
                }),
            });

            if (response.status === 401) {
                handleUnauthorized();
                return;
            }

            if (!response.ok) {
                throw new Error("Failed to add product to order.");
            }

        } catch (err) {
            setError(err.message);
        } finally {
            fetchOrders();
        }
    };

    const deleteProductFromOrder = async (orderId, productId) => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        setLoading(true); // Activar el indicador de carga

        try {
            const response = await fetch(`http://localhost:8000/api/orders/${orderId}/products/${productId}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `${tokenType} ${accessToken}`,
                },
            });

            if (response.status === 401) {
                handleUnauthorized();
                return;
            }

            if (!response.ok) {
                throw new Error("Failed to delete product from order.");
            }

        } catch (err) {
            setError(err.message);
        } finally {
            fetchOrders();
        }
    };

    const deleteOrder = async (orderId) => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        setLoading(true); // Activar el indicador de carga

        try {
            const response = await fetch(`http://localhost:8000/api/orders/${orderId}`, {
                method: "DELETE",
                headers: {
                    Authorization: `${tokenType} ${accessToken}`,
                },
            });

            if (response.status === 401) {
                handleUnauthorized();
                return;
            }

            if (!response.ok) {
                throw new Error("Failed to delete order.");
            }

        } catch (err) {
            setError(err.message);
        } finally {
            fetchOrders();
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("token_type");
        navigate("/");
    };

    const handleAddProductClick = (orderId) => {
        setSelectedOrderId(orderId);
        fetchProducts();
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
    };

    const createNewOrder = async () => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        setLoading(true); // Activar el indicador de carga

        try {
            const response = await fetch("http://localhost:8000/api/orders/", {
                method: "POST",
                headers: {
                    Authorization: `${tokenType} ${accessToken}`,
                },
            });

            if (response.status === 401) {
                handleUnauthorized();
                return;
            }

            if (!response.ok) {
                throw new Error("Failed to create new order.");
            }

        } catch (err) {
            setError(err.message);
        } finally {
            fetchOrders(); // Actualizar la lista de órdenes después de crear una nueva
        }
    };

    const exportToExcel = async () => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/api/exports/excel", {
                headers: {
                    Authorization: `${tokenType} ${accessToken}`,
                },
            });

            if (response.status === 401) {
                handleUnauthorized();
                return;
            }

            if (!response.ok) {
                throw new Error("Failed to export to Excel.");
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'orders.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (err) {
            setError(err.message);
        }
    };

    const exportToCsv = async () => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/api/exports/csv", {
                headers: {
                    Authorization: `${tokenType} ${accessToken}`,
                },
            });

            if (response.status === 401) {
                handleUnauthorized();
                return;
            }

            if (!response.ok) {
                throw new Error("Failed to export to CSV.");
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'orders.csv';
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (err) {
            setError(err.message);
        }
    };

    const exportToPdf = async () => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/api/exports/pdf", {
                headers: {
                    Authorization: `${tokenType} ${accessToken}`,
                },
            });

            if (response.status === 401) {
                handleUnauthorized();
                return;
            }

            if (!response.ok) {
                throw new Error("Failed to export to PDF.");
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'orders.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (err) {
            setError(err.message);
        }
    };

    const updateOrderStatus = async (orderId, newStatus) => {
        const accessToken = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "bearer";

        if (!accessToken) {
            setError("User is not authenticated.");
            return;
        }

        try {
            const response = await fetch(`http://localhost:8000/api/orders/${orderId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `${tokenType} ${accessToken}`,
                },
                body: JSON.stringify({
                    status: newStatus,
                    user_id: userInfo.userId,
                }),
            });

            if (response.status === 401) {
                handleUnauthorized();
                return;
            }

            if (!response.ok) {
                throw new Error("Failed to update order status.");
            }

        } catch (err) {
            setError(err.message);
        } finally {
            fetchOrders();
        }
    };

    return (
        <div className="dashboard-container">
            <div className="top-bar">
                <span className="user-info">
                    {userInfo.userName} ({(userInfo.role).toUpperCase()})
                </span>
                <button className="logout-button" onClick={handleLogout}>
                    Cerrar sesión
                </button>
            </div>
            <div className="dashboard-title-container">
                {userInfo.role.toUpperCase() === "ADMIN" ? 
                (<h1 className="dashboard-title">All Orders</h1>) : 
                (<h1 className="dashboard-title">Your Orders</h1>)}
                {!loading ? (<button className="create-order-button" onClick={createNewOrder}>Crear nueva orden</button>) : null}
            </div>
            {!loading ? (<div className="export-buttons">
                    <button className="export-button excel-button" onClick={exportToExcel}>
                        <FaFileExcel /> Exportar a Excel
                    </button>
                    <button className="export-button csv-button" onClick={exportToCsv}>
                        <FaFileCsv /> Exportar a CSV
                    </button>
                    <button className="export-button pdf-button" onClick={exportToPdf}>
                        <FaFilePdf /> Exportar a PDF
                    </button>
                </div>) : null}
            {error && <p className="login-error">{error}</p>}

            {loading ? (
                <div className="loading-indicator">Cargando...</div>
            ) : orders.length === 0 && !error ? (
                <p>No se han encontrado órdenes.</p>
            ) : (
                orders.map((order) => (
                    <div key={order.id} className="order-card">
                        <div className="order-header">
                            <h2>Orden #{order.id}</h2>
                            <button className="add-product-button" onClick={() => handleAddProductClick(order.id)}>Añadir producto</button>
                            <button className="delete-order-button" onClick={() => deleteOrder(order.id)}>Eliminar orden</button>
                        </div>
                        <p>
                            <strong>Estado:</strong> {order.status}
                            {userInfo.role.toUpperCase() === "ADMIN" && (
                                <select
                                    value={order.status}
                                    onChange={(e) => updateOrderStatus(order.id, e.target.value)}
                                    style={{ marginLeft: "10px" }}
                                >
                                    <option value="in progress">In Progress</option>
                                    <option value="paid">Paid</option>
                                    <option value="delivered">Delivered</option>
                                    <option value="cancelled">Cancelled</option>
                                </select>
                            )}
                        </p>
                        <p><strong>Fecha:</strong> {new Date(order.created_at).toLocaleString()}</p>

                        <div className="order-items">
                            <h3>Productos</h3>
                            {order.items.map((item, idx) => (
                                <div key={idx} className="order-item">
                                    <div className="item-left">
                                        <span className="item-title">{item.product.title}</span>
                                        <span className="item-qty">Cantidad: {item.quantity}</span>
                                        <div className="button-group">
                                            <button onClick={() => updateQuantity(order.id, item.product.id, item.quantity + 1)}>+</button>
                                            <button onClick={() => updateQuantity(order.id, item.product.id, item.quantity - 1)}>-</button>
                                            <button className="delete-button" onClick={() => deleteProductFromOrder(order.id, item.product.id)}>
                                                <span role="img" aria-label="delete">🗑️</span>
                                            </button>
                                        </div>
                                    </div>
                                    <div className="item-right">
                                        <span className="item-price">{item.quantity} x {(item.product.price).toFixed(2)} € = {(item.product.price * item.quantity).toFixed(2)} €</span>
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

            {showModal && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close-button" onClick={handleCloseModal}>&times;</span>
                        <h2>Lista de Productos</h2>
                        <table className="product-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Nombre</th>
                                    <th>Precio</th>
                                    <th>Acción</th>
                                </tr>
                            </thead>
                            <tbody>
                                {products.map((product) => (
                                    <tr key={product.id}>
                                        <td>{product.id}</td>
                                        <td>{product.title}</td>
                                        <td>{product.price} €</td>
                                        <td>
                                            <button className="add-button" onClick={() => addProductToOrder(selectedOrderId, product.id)}>Añadir</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Dashboard;