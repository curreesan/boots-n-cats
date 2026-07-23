import type { Pet } from "../types/pet";
import type { Paginated } from "./products";
import { apiFetch } from "./apiFetch";

export async function getPets(
  options: { species?: string; limit?: number; offset?: number } = {},
): Promise<Paginated<Pet>> {
  const params = new URLSearchParams();
  if (options.species) params.set("species", options.species);
  params.set("limit", String(options.limit ?? 20));
  params.set("offset", String(options.offset ?? 0));

  const response = await apiFetch(`/pets?${params}`);

  if (!response.ok) {
    throw new Error("Failed to fetch pets");
  }

  return response.json();
}

export async function getPet(id: string): Promise<Pet> {
  const response = await apiFetch(`/pets/${id}`);
  if (!response.ok) throw new Error("Failed to fetch pet");
  return response.json();
}
