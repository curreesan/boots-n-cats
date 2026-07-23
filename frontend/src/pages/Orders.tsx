import { Link } from "react-router-dom";
import { useOrders } from "../hooks/useOrders";
import { Card } from "@/components/ui/card";

function Orders() {
  const { orders, loading, error } = useOrders();

  if (loading)
    return <div className="py-12 text-muted-foreground">Loading...</div>;
  if (error) return <div className="py-12 text-destructive">{error}</div>;

  return (
    <div className="flex flex-col gap-6 py-10">
      <h1 className="text-3xl font-bold">Orders</h1>

      {orders.length === 0 ? (
        <p className="text-muted-foreground">No orders yet.</p>
      ) : (
        <Card className="gap-0 overflow-hidden py-0">
          {orders.map((order, i) => (
            <Link
              key={order.id}
              to={`/orders/${order.id}`}
              className={`flex items-center justify-between px-6 py-4 hover:bg-accent ${
                i !== orders.length - 1 ? "border-b border-border" : ""
              }`}
            >
              <span className="font-medium">
                Order #{order.id.slice(0, 8)}
              </span>
              <span className="text-sm text-muted-foreground">
                {new Date(order.created_at).toLocaleDateString()}
              </span>
              <span className="font-medium">₹{order.total_amount}</span>
            </Link>
          ))}
        </Card>
      )}
    </div>
  );
}

export default Orders;
