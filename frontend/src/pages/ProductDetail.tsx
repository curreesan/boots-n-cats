import { useParams, useNavigate } from "react-router-dom";
import { useProduct } from "../hooks/useProduct";
import { useCart } from "../context/useCart";
import { useAuth } from "../context/useAuth";
import { Button } from "@/components/ui/button";
import SpeciesBadge from "../components/SpeciesBadge";

function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const { product, loading, error } = useProduct(id!);
  const { items, addItem, increaseQuantity, decreaseQuantity } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  if (loading)
    return <div className="py-12 text-muted-foreground">Loading...</div>;
  if (error || !product)
    return <div className="py-12 text-muted-foreground">Product not found.</div>;

  const line = items.find((l) => l.product_id === product.id);

  function handleAdd() {
    if (!user) {
      navigate("/login");
      return;
    }
    void addItem(product!.id);
  }

  return (
    <div className="grid grid-cols-1 gap-10 py-10 md:grid-cols-2">
      <div className="aspect-[4/3] w-full overflow-hidden rounded-xl bg-muted">
        {product.image_url && (
          <img
            src={product.image_url}
            alt={product.name}
            className="size-full object-cover"
          />
        )}
      </div>

      <div className="flex flex-col gap-4">
        <SpeciesBadge species={product.species} />
        <h1 className="text-3xl font-bold">{product.name}</h1>
        <p className="text-sm text-muted-foreground capitalize">
          {product.category}
        </p>
        <p className="text-2xl font-semibold text-primary">
          ₹{product.price}
        </p>
        <p className="text-sm text-muted-foreground">
          In stock: {product.stock_quantity}
        </p>

        {line ? (
          <div className="flex items-center gap-3 pt-2">
            <Button
              variant="outline"
              size="icon"
              onClick={() => void decreaseQuantity(product.id)}
            >
              -
            </Button>
            <span className="w-8 text-center font-medium">
              {line.quantity}
            </span>
            <Button
              variant="outline"
              size="icon"
              onClick={() => void increaseQuantity(product.id)}
            >
              +
            </Button>
          </div>
        ) : (
          <Button size="lg" className="mt-2 w-fit" onClick={handleAdd}>
            Add to cart
          </Button>
        )}
      </div>
    </div>
  );
}

export default ProductDetail;
