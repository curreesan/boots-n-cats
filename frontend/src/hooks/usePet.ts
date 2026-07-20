import { useState, useEffect } from "react";
import type { Pet } from "../types/pet";
import { getPet } from "../api/pets";

export function usePet(id: string) {
  const [pet, setPet] = useState<Pet | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadPet() {
      try {
        const data = await getPet(id);
        setPet(data);
      } catch {
        setError("Failed to load pet");
      } finally {
        setLoading(false);
      }
    }
    void loadPet();
  }, [id]);

  return { pet, loading, error };
}
