import { useState, useEffect } from "react";
import type { Product } from "../types/product";
import { getProducts } from "../api/products";

export const PRODUCTS_PAGE_SIZE = 20;

export function useProducts(page: number = 1) {
  const [products, setProducts] = useState<Product[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    // Resetting to a loading state when `page` changes so pagination
    // shows a spinner again instead of silently swapping the list —
    // syncing to the external fetch, not deriving state from render.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setLoading(true);

    async function loadProducts() {
      try {
        const data = await getProducts({
          limit: PRODUCTS_PAGE_SIZE,
          offset: (page - 1) * PRODUCTS_PAGE_SIZE,
        });
        if (cancelled) return;
        setProducts(data.items);
        setTotal(data.total);
      } catch {
        if (!cancelled) setError("Failed to load products");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadProducts();
    return () => {
      cancelled = true;
    };
  }, [page]);

  return { products, total, loading, error };
}
