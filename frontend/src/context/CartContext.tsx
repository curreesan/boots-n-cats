import { useState, type ReactNode } from "react";
import type { CartLine } from "../types/cart";
import type { Product } from "../types/product";
import { CartContext } from "./cartContextObject";

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartLine[]>([]);

  function addItem(product: Product) {
    setItems((current) => {
      const existing = current.find((line) => line.product.id === product.id);
      if (existing) {
        return current.map((line) =>
          line.product.id === product.id
            ? { ...line, quantity: line.quantity + 1 }
            : line,
        );
      }
      return [...current, { product, quantity: 1 }];
    });
  }

  function increaseQuantity(productId: string) {
    setItems((current) =>
      current.map((line) =>
        line.product.id === productId
          ? { ...line, quantity: line.quantity + 1 }
          : line,
      ),
    );
  }

  function decreaseQuantity(productId: string) {
    setItems((current) =>
      current
        .map((line) =>
          line.product.id === productId
            ? { ...line, quantity: line.quantity - 1 }
            : line,
        )
        .filter((line) => line.quantity > 0),
    );
  }

  function removeItem(productId: string) {
    setItems((current) =>
      current.filter((line) => line.product.id !== productId),
    );
  }

  function clearCart() {
    setItems([]);
  }

  return (
    <CartContext.Provider
      value={{
        items,
        addItem,
        increaseQuantity,
        decreaseQuantity,
        removeItem,
        clearCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}
