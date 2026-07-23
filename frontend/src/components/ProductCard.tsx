import { Link, useNavigate } from "react-router-dom";
import type { Product } from "../types/product";
import { useCart } from "../context/useCart";
import { useAuth } from "../context/useAuth";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import SpeciesBadge from "./SpeciesBadge";

type ProductCardProps = {
  product: Product;
};

function ProductCard({ product }: ProductCardProps) {
  const { items, addItem, increaseQuantity, decreaseQuantity } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();
  const line = items.find((l) => l.product_id === product.id);

  function handleAdd() {
    if (!user) {
      navigate("/login");
      return;
    }
    void addItem(product.id);
  }

  return (
    <Card className="gap-0 overflow-hidden py-0">
      <Link to={`/products/${product.id}`} className="block">
        <div className="aspect-[4/3] w-full overflow-hidden bg-muted">
          {product.image_url && (
            <img
              src={product.image_url}
              alt={product.name}
              className="size-full object-cover"
              loading="lazy"
            />
          )}
        </div>
      </Link>
      <CardContent className="flex flex-col gap-2 px-4 py-4">
        <div className="flex flex-wrap gap-1.5">
          <SpeciesBadge species={product.species} />
          <Badge variant="secondary" className="capitalize">
            {product.category}
          </Badge>
        </div>
        <Link
          to={`/products/${product.id}`}
          className="truncate font-medium hover:text-primary"
        >
          {product.name}
        </Link>
        <p className="text-sm text-muted-foreground">₹{product.price}</p>

        {line ? (
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="icon-sm"
              onClick={() => void decreaseQuantity(product.id)}
            >
              -
            </Button>
            <span className="w-6 text-center text-sm">{line.quantity}</span>
            <Button
              variant="outline"
              size="icon-sm"
              onClick={() => void increaseQuantity(product.id)}
            >
              +
            </Button>
          </div>
        ) : (
          <Button size="sm" onClick={handleAdd}>
            Add to cart
          </Button>
        )}
      </CardContent>
    </Card>
  );
}

export default ProductCard;
