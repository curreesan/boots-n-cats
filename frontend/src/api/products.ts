import type { Product } from "../types/product";
import { API_BASE_URL } from "./config";

export async function getProducts(): Promise<Product[]> {
  const response = await fetch(`${API_BASE_URL}/products`, {
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch products");
  }

  return response.json();
}

export async function getProduct(id: string): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/products/${id}`, {
    credentials: "include",
  });
  if (!response.ok) throw new Error("Failed to fetch product");
  return response.json();
}
