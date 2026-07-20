import { useProducts } from "../hooks/useProducts";
import ProductCard from "../components/ProductCard";
import "../styles/Products.css";

function Products() {
  const { products, loading, error } = useProducts();

  if (loading) return <div className="products__status">Loading...</div>;
  if (error)
    return (
      <div className="products__status products__status--error">{error}</div>
    );

  return (
    <div className="products">
      <h1 className="products__heading">Products</h1>
      <div className="products__list">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}

export default Products;
