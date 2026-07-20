import { Link } from "react-router-dom";
import { useOrders } from "../hooks/useOrders";
import "../styles/Orders.css";

function Orders() {
  const { orders, loading, error } = useOrders();

  if (loading) return <div className="orders__status">Loading...</div>;
  if (error)
    return <div className="orders__status orders__status--error">{error}</div>;

  return (
    <div className="orders">
      <h1 className="orders__heading">Orders</h1>

      {orders.length === 0 ? (
        <div className="orders__status">No orders yet.</div>
      ) : (
        <div className="orders__list">
          {orders.map((order) => (
            <Link
              key={order.id}
              to={`/orders/${order.id}`}
              className="orders__row"
            >
              <span className="orders__id">Order #{order.id.slice(0, 8)}</span>
              <span className="orders__date">
                {new Date(order.created_at).toLocaleDateString()}
              </span>
              <span className="orders__total">₹{order.total_amount}</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default Orders;
