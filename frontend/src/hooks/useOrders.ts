import { useState, useEffect } from "react";
import type { Order } from "../types/order";
import { getOrders } from "../api/orders";

export function useOrders() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadOrders() {
      try {
        const data = await getOrders();
        setOrders(data.items);
      } catch {
        setError("Failed to load orders");
      } finally {
        setLoading(false);
      }
    }
    void loadOrders();
  }, []);

  return { orders, loading, error };
}
