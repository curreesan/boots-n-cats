import { useState, useEffect } from "react";
import type { Product } from "../types/product";
import { getProduct } from "../api/products";

export function useProduct(id: string) {
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadProduct() {
      try {
        const data = await getProduct(id);
        setProduct(data);
      } catch {
        setError("Failed to load product");
      } finally {
        setLoading(false);
      }
    }
    void loadProduct();
  }, [id]);

  return { product, loading, error };
}
