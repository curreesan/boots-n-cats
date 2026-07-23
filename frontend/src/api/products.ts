import type { Product } from "../types/product";
import { apiFetch } from "./apiFetch";

export interface Paginated<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export async function getProducts(
  options: { species?: string; category?: string; limit?: number; offset?: number } = {},
): Promise<Paginated<Product>> {
  const params = new URLSearchParams();
  if (options.species) params.set("species", options.species);
  if (options.category) params.set("category", options.category);
  params.set("limit", String(options.limit ?? 20));
  params.set("offset", String(options.offset ?? 0));

  const response = await apiFetch(`/products?${params}`);

  if (!response.ok) {
    throw new Error("Failed to fetch products");
  }

  return response.json();
}

export async function getProduct(id: string): Promise<Product> {
  const response = await apiFetch(`/products/${id}`);
  if (!response.ok) throw new Error("Failed to fetch product");
  return response.json();
}
