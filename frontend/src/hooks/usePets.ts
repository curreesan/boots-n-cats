import { useState, useEffect } from "react";
import type { Pet } from "../types/pet";
import { getPets } from "../api/pets";

export const PETS_PAGE_SIZE = 20;

export function usePets(page: number = 1, species?: string) {
  const [pets, setPets] = useState<Pet[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    // Resetting to a loading state when `page`/`species` changes so
    // pagination shows a spinner again instead of silently swapping the
    // list — syncing to the external fetch, not deriving state from render.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setLoading(true);

    async function loadPets() {
      try {
        const data = await getPets({
          species,
          limit: PETS_PAGE_SIZE,
          offset: (page - 1) * PETS_PAGE_SIZE,
        });
        if (cancelled) return;
        setPets(data.items);
        setTotal(data.total);
      } catch {
        if (!cancelled) setError("Failed to load pets");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadPets();
    return () => {
      cancelled = true;
    };
  }, [page, species]);

  return { pets, total, loading, error };
}
