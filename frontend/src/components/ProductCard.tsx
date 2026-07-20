import { Link } from "react-router-dom";
import type { Product } from "../types/product";
import { useCart } from "../context/useCart";
import SpeciesBadge from "./SpeciesBadge";
import "../styles/ProductCard.css";

type ProductCardProps = {
  product: Product;
};

function ProductCard({ product }: ProductCardProps) {
  const { items, addItem, increaseQuantity, decreaseQuantity } = useCart();
  const line = items.find((l) => l.product.id === product.id);

  return (
    <div className="product-row">
      <Link to={`/products/${product.id}`} className="product-row__info">
        <SpeciesBadge species={product.species} />
        <span className="product-row__name">{product.name}</span>
        <span className="product-row__price">₹{product.price}</span>
      </Link>

      {line ? (
        <div className="product-row__qty">
          <button onClick={() => decreaseQuantity(product.id)}>-</button>
          <span>{line.quantity}</span>
          <button onClick={() => increaseQuantity(product.id)}>+</button>
        </div>
      ) : (
        <button className="product-row__add" onClick={() => addItem(product)}>
          Add to cart
        </button>
      )}
    </div>
  );
}

export default ProductCard;
