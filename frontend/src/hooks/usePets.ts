import { useState, useEffect } from "react";
import type { Pet } from "../types/pet";
import { getPets } from "../api/pets";

export function usePets() {
  const [pets, setPets] = useState<Pet[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadPets() {
      try {
        const data = await getPets();
        setPets(data);
      } catch {
        setError("Failed to load pets");
      } finally {
        setLoading(false);
      }
    }

    loadPets();
  }, []);

  return { pets, loading, error };
}
