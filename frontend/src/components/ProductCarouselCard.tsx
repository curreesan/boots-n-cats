import { Link } from "react-router-dom";
import type { Product } from "../types/product";
import { Card, CardContent } from "@/components/ui/card";

type ProductCarouselCardProps = {
  product: Product;
};

function ProductCarouselCard({ product }: ProductCarouselCardProps) {
  return (
    <Link to={`/products/${product.id}`}>
      <Card className="gap-0 overflow-hidden py-0 transition-shadow hover:shadow-md">
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
        <CardContent className="px-4 py-3">
          <p className="truncate text-sm font-medium">{product.name}</p>
          <p className="text-sm text-muted-foreground">₹{product.price}</p>
        </CardContent>
      </Card>
    </Link>
  );
}

export default ProductCarouselCard;
