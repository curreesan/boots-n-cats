import type { Product } from "../types/product";
import type { Pet } from "../types/pet";
import { API_BASE_URL } from "./config";

export async function createProduct(
  product: Omit<Product, "id">,
): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/admin/products`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(product),
  });
  if (!response.ok) throw new Error("Failed to create product");
  return response.json();
}

export async function deleteProduct(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/admin/products/${id}`, {
    method: "DELETE",
    credentials: "include",
  });
  if (!response.ok) throw new Error("Failed to delete product");
}

export async function createPet(pet: Omit<Pet, "id">): Promise<Pet> {
  const response = await fetch(`${API_BASE_URL}/admin/pets`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(pet),
  });
  if (!response.ok) throw new Error("Failed to create pet");
  return response.json();
}

export async function deletePet(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/admin/pets/${id}`, {
    method: "DELETE",
    credentials: "include",
  });
  if (!response.ok) throw new Error("Failed to delete pet");
}
