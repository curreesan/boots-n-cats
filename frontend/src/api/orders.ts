import type { Order, OrderDetail } from "../types/order";
import type { Paginated } from "./products";
import { apiFetch } from "./apiFetch";

export async function checkout(): Promise<Order> {
  const response = await apiFetch("/orders", { method: "POST" });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? "Checkout failed");
  }
  return response.json();
}

export async function getOrders(): Promise<Paginated<Order>> {
  const response = await apiFetch("/orders");
  if (!response.ok) throw new Error("Failed to fetch orders");
  return response.json();
}

export async function getOrder(orderId: string): Promise<OrderDetail> {
  const response = await apiFetch(`/orders/${orderId}`);
  if (!response.ok) throw new Error("Failed to fetch order");
  return response.json();
}
