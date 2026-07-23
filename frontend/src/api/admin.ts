import type { Product } from "../types/product";
import type { Pet } from "../types/pet";
import { apiFetch } from "./apiFetch";

export async function createProduct(
  product: Omit<Product, "id">,
): Promise<Product> {
  const response = await apiFetch("/admin/products", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(product),
  });
  if (!response.ok) throw new Error("Failed to create product");
  return response.json();
}

export async function updateProduct(
  id: string,
  product: Omit<Product, "id">,
): Promise<Product> {
  const response = await apiFetch(`/admin/products/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(product),
  });
  if (!response.ok) throw new Error("Failed to update product");
  return response.json();
}

export async function deleteProduct(id: string): Promise<void> {
  const response = await apiFetch(`/admin/products/${id}`, { method: "DELETE" });
  if (!response.ok) throw new Error("Failed to delete product");
}

export async function createPet(pet: Omit<Pet, "id">): Promise<Pet> {
  const response = await apiFetch("/admin/pets", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(pet),
  });
  if (!response.ok) throw new Error("Failed to create pet");
  return response.json();
}

export async function updatePet(
  id: string,
  pet: Omit<Pet, "id">,
): Promise<Pet> {
  const response = await apiFetch(`/admin/pets/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(pet),
  });
  if (!response.ok) throw new Error("Failed to update pet");
  return response.json();
}

export async function deletePet(id: string): Promise<void> {
  const response = await apiFetch(`/admin/pets/${id}`, { method: "DELETE" });
  if (!response.ok) throw new Error("Failed to delete pet");
}
