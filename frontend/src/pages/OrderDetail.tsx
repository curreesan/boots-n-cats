import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import type { OrderDetail as OrderDetailType } from "../types/order";
import { getOrder } from "../api/orders";
import "../styles/OrderDetail.css";

function OrderDetail() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<OrderDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const result = await getOrder(id!);
        setData(result);
      } catch {
        setError("Failed to load order");
      } finally {
        setLoading(false);
      }
    }
    void load();
  }, [id]);

  if (loading) return <div className="order-detail__status">Loading...</div>;
  if (error || !data)
    return <div className="order-detail__status">Order not found.</div>;

  const { order, items } = data;

  return (
    <div className="order-detail">
      <h1 className="order-detail__heading">Order #{order.id.slice(0, 8)}</h1>
      <div className="order-detail__meta">
        {new Date(order.created_at).toLocaleString()}
      </div>

      <table className="order-detail__table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Unit Price</th>
            <th>Quantity</th>
            <th>Line Total</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.product_name}</td>
              <td>₹{item.unit_price}</td>
              <td>{item.quantity}</td>
              <td>₹{item.unit_price * item.quantity}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="order-detail__total">Total: ₹{order.total_amount}</div>
    </div>
  );
}

export default OrderDetail;
