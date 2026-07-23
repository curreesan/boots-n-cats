import { useState } from "react";
import { useProducts, PRODUCTS_PAGE_SIZE } from "../hooks/useProducts";
import ProductCard from "../components/ProductCard";
import { Button } from "@/components/ui/button";

function Products() {
  const [page, setPage] = useState(1);
  const { products, total, loading, error } = useProducts(page);
  const totalPages = Math.max(1, Math.ceil(total / PRODUCTS_PAGE_SIZE));

  function goToPage(next: number) {
    setPage(next);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  if (loading)
    return <div className="py-12 text-muted-foreground">Loading...</div>;
  if (error) return <div className="py-12 text-destructive">{error}</div>;

  return (
    <div className="flex flex-col gap-6 py-10">
      <h1 className="text-3xl font-bold">Products</h1>
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
    </div>
  );
}

export default Products;
