import type { Pet } from "../types/pet";
import { API_BASE_URL } from "./config";

export async function getPets(): Promise<Pet[]> {
  const response = await fetch(`${API_BASE_URL}/pets`, {
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch pets");
  }

  return response.json();
}

export async function getPet(id: string): Promise<Pet> {
  const response = await fetch(`${API_BASE_URL}/pets/${id}`, {
    credentials: "include",
  });
  if (!response.ok) throw new Error("Failed to fetch pet");
  return response.json();
}
