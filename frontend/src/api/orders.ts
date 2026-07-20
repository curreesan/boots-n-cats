import type { Order, OrderDetail } from "../types/order";
import { API_BASE_URL } from "./config";

export async function getOrders(): Promise<Order[]> {
  const response = await fetch(`${API_BASE_URL}/orders`, {
    credentials: "include",
  });
  if (!response.ok) throw new Error("Failed to fetch orders");
  return response.json();
}

export async function getOrder(orderId: string): Promise<OrderDetail> {
  const response = await fetch(`${API_BASE_URL}/orders/${orderId}`, {
    credentials: "include",
  });
  if (!response.ok) throw new Error("Failed to fetch order");
  return response.json();
}
