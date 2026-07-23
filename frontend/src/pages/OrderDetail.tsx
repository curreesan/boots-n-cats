import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import type { OrderDetail as OrderDetailType } from "../types/order";
import { getOrder } from "../api/orders";

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

  if (loading)
    return <div className="py-12 text-muted-foreground">Loading...</div>;
  if (error || !data)
    return <div className="py-12 text-muted-foreground">Order not found.</div>;

  const { order, items } = data;

  return (
    <div className="flex flex-col gap-2 py-10">
      <h1 className="text-3xl font-bold">Order #{order.id.slice(0, 8)}</h1>
      <p className="mb-4 text-sm text-muted-foreground">
        {new Date(order.created_at).toLocaleString()}
      </p>

      <div className="overflow-x-auto rounded-xl border border-border">
        <table className="w-full text-sm">
          <thead className="bg-muted text-muted-foreground">
            <tr>
              <th className="px-4 py-3 text-left font-medium">Product</th>
              <th className="px-4 py-3 text-left font-medium">Unit Price</th>
              <th className="px-4 py-3 text-left font-medium">Quantity</th>
              <th className="px-4 py-3 text-left font-medium">Line Total</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, i) => (
              <tr
                key={item.id}
                className={i !== items.length - 1 ? "border-b border-border" : ""}
              >
                <td className="px-4 py-3">{item.product_name}</td>
                <td className="px-4 py-3">₹{item.unit_price}</td>
                <td className="px-4 py-3">{item.quantity}</td>
                <td className="px-4 py-3">₹{item.unit_price * item.quantity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="mt-2 text-right text-lg font-semibold text-primary">
        Total: ₹{order.total_amount}
      </p>
    </div>
  );
}

export default OrderDetail;
