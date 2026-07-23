import { useEffect, useState, type ReactNode } from "react";
import type { CartLine } from "../types/cart";
import {
  getCart,
  addToCart,
  setCartItemQuantity,
  removeCartItem,
  clearCartApi,
} from "../api/cart";
import { useAuth } from "./useAuth";
import { CartContext } from "./cartContextObject";

export function CartProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [items, setItems] = useState<CartLine[]>([]);
  const [subtotal, setSubtotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Cart is server-side and tied to user_id — logging out clears what's
  // shown here (not the actual cart, which is still on the server), and
  // logging back in re-fetches it. No local/guest cart exists.
  useEffect(() => {
    if (!user) {
      // Syncing displayed cart state to auth state, not deriving it from
      // props/state available during render — legitimate external sync,
      // same reasoning as AdminKnowledge's loadDocs suppression.
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setItems([]);
      setSubtotal(0);
      return;
    }

    let cancelled = false;
    setLoading(true);
    getCart()
      .then((cart) => {
        if (cancelled) return;
        setItems(cart.items);
        setSubtotal(cart.subtotal);
      })
      .catch(() => {
        if (!cancelled) setError("Failed to load cart");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [user]);

  // Re-fetches the cart from the server without touching `loading` (no
  // full-page spinner) — for syncing after something OUTSIDE this
  // context's own mutation functions changed the server-side cart, e.g.
  // the chatbot's add_to_cart tool, which the frontend has no other way
  // of finding out about.
  async function refreshCart() {
    if (!user) return;
    try {
      const cart = await getCart();
      setItems(cart.items);
      setSubtotal(cart.subtotal);
    } catch {
      setError("Failed to refresh cart");
    }
  }

  async function addItem(productId: string, quantity = 1) {
    setError(null);
    try {
      const cart = await addToCart(productId, quantity);
      setItems(cart.items);
      setSubtotal(cart.subtotal);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add item");
    }
  }

  async function updateQuantity(productId: string, quantity: number) {
    setError(null);
    try {
      const cart = await setCartItemQuantity(productId, quantity);
      setItems(cart.items);
      setSubtotal(cart.subtotal);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update item");
    }
  }

  async function increaseQuantity(productId: string) {
    const line = items.find((l) => l.product_id === productId);
    if (!line) return;
    await updateQuantity(productId, line.quantity + 1);
  }

  async function decreaseQuantity(productId: string) {
    const line = items.find((l) => l.product_id === productId);
    if (!line) return;
    if (line.quantity <= 1) {
      await removeItem(productId);
      return;
    }
    await updateQuantity(productId, line.quantity - 1);
  }

  async function removeItem(productId: string) {
    setError(null);
    try {
      const cart = await removeCartItem(productId);
      setItems(cart.items);
      setSubtotal(cart.subtotal);
    } catch {
      setError("Failed to remove item");
    }
  }

  async function clearCart() {
    setError(null);
    try {
      const cart = await clearCartApi();
      setItems(cart.items);
      setSubtotal(cart.subtotal);
    } catch {
      setError("Failed to clear cart");
    }
  }

  return (
    <CartContext.Provider
      value={{
        items,
        subtotal,
        loading,
        error,
        addItem,
        increaseQuantity,
        decreaseQuantity,
        removeItem,
        clearCart,
        refreshCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}
