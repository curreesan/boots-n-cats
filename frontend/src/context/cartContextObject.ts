import { createContext } from "react";
import type { CartLine } from "../types/cart";
import type { Product } from "../types/product";

export type CartContextType = {
  items: CartLine[];
  addItem: (product: Product) => void;
  increaseQuantity: (productId: string) => void;
  decreaseQuantity: (productId: string) => void;
  removeItem: (productId: string) => void;
  clearCart: () => void;
};

export const CartContext = createContext<CartContextType | null>(null);
