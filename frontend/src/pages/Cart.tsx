import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../context/useCart";
import { useAuth } from "../context/useAuth";
import { checkout } from "../api/orders";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

function Cart() {
  const {
    items,
    subtotal,
    loading,
    increaseQuantity,
    decreaseQuantity,
    removeItem,
    clearCart,
  } = useCart();
  const { user } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  async function handleCheckout() {
    if (!user) {
      navigate("/login");
      return;
    }

    setError(null);
    try {
      await checkout();
      await clearCart();
      navigate("/orders");
    } catch {
      setError("Checkout failed — please try again");
    }
  }

  if (!user) {
    return (
      <div className="py-12">
        <h1 className="mb-4 text-3xl font-bold">Cart</h1>
        <p className="text-muted-foreground">Log in to see your cart.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="py-12">
        <h1 className="mb-4 text-3xl font-bold">Cart</h1>
        <p className="text-muted-foreground">Loading...</p>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="py-12">
        <h1 className="mb-4 text-3xl font-bold">Cart</h1>
        <p className="text-muted-foreground">Your cart is empty.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6 py-10">
      <h1 className="text-3xl font-bold">Cart</h1>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
        <div className="flex flex-col gap-3 lg:col-span-2">
          {items.map((line) => (
            <Card
              key={line.product_id}
              className="flex-row items-center gap-4 p-4"
            >
              <div className="size-20 shrink-0 overflow-hidden rounded-lg bg-muted">
                {line.image_url && (
                  <img
                    src={line.image_url}
                    alt={line.product_name}
                    className="size-full object-cover"
                  />
                )}
              </div>
              <CardContent className="flex flex-1 flex-col gap-1 p-0">
                <p className="font-medium">{line.product_name}</p>
                <p className="text-sm text-muted-foreground">
                  ₹{line.unit_price} each
                </p>
              </CardContent>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="icon-sm"
                  onClick={() => void decreaseQuantity(line.product_id)}
                >
                  -
                </Button>
                <span className="w-6 text-center text-sm">
                  {line.quantity}
                </span>
                <Button
                  variant="outline"
                  size="icon-sm"
                  onClick={() => void increaseQuantity(line.product_id)}
                >
                  +
                </Button>
              </div>
              <p className="w-20 text-right font-medium">
                ₹{line.unit_price * line.quantity}
              </p>
              <Button
                variant="ghost"
                size="sm"
                className="text-destructive hover:text-destructive"
                onClick={() => void removeItem(line.product_id)}
              >
                Remove
              </Button>
            </Card>
          ))}
        </div>

        <Card className="h-fit p-6">
          <CardContent className="flex flex-col gap-4 p-0">
            <div className="flex items-center justify-between text-lg font-semibold">
              <span>Total</span>
              <span>₹{subtotal}</span>
            </div>
            <Button size="lg" onClick={handleCheckout}>
              Place Order
            </Button>
            {error && <p className="text-sm text-destructive">{error}</p>}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default Cart;
