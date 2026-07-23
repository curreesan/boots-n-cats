import type { CartLine } from "../types/cart";
import { apiFetch } from "./apiFetch";

export interface CartResponse {
  items: CartLine[];
  subtotal: number;
}

async function handle(response: Response): Promise<CartResponse> {
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? "Cart request failed");
  }
  return response.json();
}

export async function getCart(): Promise<CartResponse> {
  const response = await apiFetch("/cart");
  return handle(response);
}

export async function addToCart(
  productId: string,
  quantity = 1,
): Promise<CartResponse> {
  const response = await apiFetch("/cart", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, quantity }),
  });
  return handle(response);
}

export async function setCartItemQuantity(
  productId: string,
  quantity: number,
): Promise<CartResponse> {
  const response = await apiFetch(`/cart/${productId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ quantity }),
  });
  return handle(response);
}

export async function removeCartItem(productId: string): Promise<CartResponse> {
  const response = await apiFetch(`/cart/${productId}`, { method: "DELETE" });
  return handle(response);
}

export async function clearCartApi(): Promise<CartResponse> {
  const response = await apiFetch("/cart", { method: "DELETE" });
  return handle(response);
}
