import { useState, useEffect } from "react";
import { useProducts, PRODUCTS_PAGE_SIZE } from "../hooks/useProducts";
import { getProductCategories } from "../api/products";
import ProductCard from "../components/ProductCard";
import { Button } from "@/components/ui/button";

const SPECIES_OPTIONS = [
  { label: "All", value: undefined },
  { label: "Dog", value: "dog" },
  { label: "Cat", value: "cat" },
] as const;

function Products() {
  const [page, setPage] = useState(1);
  const [species, setSpecies] = useState<string | undefined>(undefined);
  const [category, setCategory] = useState<string | undefined>(undefined);
  const [categories, setCategories] = useState<string[]>([]);
  const { products, total, loading, error } = useProducts(page, species, category);
  const totalPages = Math.max(1, Math.ceil(total / PRODUCTS_PAGE_SIZE));

  useEffect(() => {
    // Fetched once on mount — the category list itself doesn't depend on
    // the current species/page filters, it's every category in use.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void getProductCategories().then(setCategories);
  }, []);

  function goToPage(next: number) {
    setPage(next);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function selectSpecies(next: string | undefined) {
    setSpecies(next);
    setPage(1);
  }

  function selectCategory(next: string) {
    setCategory(next === "" ? undefined : next);
    setPage(1);
  }

  return (
    <div className="flex flex-col gap-6 py-10">
      <h1 className="text-3xl font-bold">Products</h1>

      <div className="flex flex-wrap items-center gap-3">
        <div className="flex gap-2">
          {SPECIES_OPTIONS.map((opt) => (
            <Button
              key={opt.label}
              size="sm"
              variant={species === opt.value ? "default" : "outline"}
              onClick={() => selectSpecies(opt.value)}
            >
              {opt.label}
            </Button>
          ))}
        </div>

        <select
          className="h-8 rounded-md border border-input bg-transparent px-3 text-sm capitalize"
          value={category ?? ""}
          onChange={(e) => selectCategory(e.target.value)}
        >
          <option value="">All categories</option>
          {categories.map((cat) => (
            <option key={cat} value={cat} className="capitalize">
              {cat}
            </option>
          ))}
        </select>
      </div>

      {loading && <div className="py-12 text-muted-foreground">Loading...</div>}
      {error && <div className="py-12 text-destructive">{error}</div>}

      {!loading && !error && (
        <>
          <div className="grid grid-cols-2 gap-5 sm:grid-cols-3 lg:grid-cols-4">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-4 pt-4">
              <Button
                variant="outline"
                size="sm"
                disabled={page === 1}
                onClick={() => goToPage(page - 1)}
              >
                Previous
              </Button>
              <span className="text-sm text-muted-foreground">
                Page {page} of {totalPages}
              </span>
              <Button
                variant="outline"
                size="sm"
                disabled={page === totalPages}
                onClick={() => goToPage(page + 1)}
              >
                Next
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Products;
