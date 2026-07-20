import { useParams } from "react-router-dom";
import { useProduct } from "../hooks/useProduct";
import { useCart } from "../context/useCart";
import SpeciesBadge from "../components/SpeciesBadge";
import "../styles/ProductDetail.css";

function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const { product, loading, error } = useProduct(id!);
  const { items, addItem, increaseQuantity, decreaseQuantity } = useCart();

  if (loading) return <div className="product-detail__status">Loading...</div>;
  if (error || !product)
    return <div className="product-detail__status">Product not found.</div>;

  const line = items.find((l) => l.product.id === product.id);

  return (
    <div className="product-detail">
      <SpeciesBadge species={product.species} />
      <h1 className="product-detail__name">{product.name}</h1>
      <div className="product-detail__meta">{product.category}</div>
      <div className="product-detail__price">₹{product.price}</div>
      <div className="product-detail__stock">
        In stock: {product.stock_quantity}
      </div>

      {line ? (
        <div className="product-detail__qty">
          <button onClick={() => decreaseQuantity(product.id)}>-</button>
          <span>{line.quantity}</span>
          <button onClick={() => increaseQuantity(product.id)}>+</button>
        </div>
      ) : (
        <button
          className="product-detail__add"
          onClick={() => addItem(product)}
        >
          Add to cart
        </button>
      )}
    </div>
  );
}

export default ProductDetail;
