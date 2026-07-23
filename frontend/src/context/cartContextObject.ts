import { createContext } from "react";
import type { CartLine } from "../types/cart";

export type CartContextType = {
  items: CartLine[];
  subtotal: number;
  loading: boolean;
  error: string | null;
  addItem: (productId: string, quantity?: number) => Promise<void>;
  increaseQuantity: (productId: string) => Promise<void>;
  decreaseQuantity: (productId: string) => Promise<void>;
  removeItem: (productId: string) => Promise<void>;
  clearCart: () => Promise<void>;
};

export const CartContext = createContext<CartContextType | null>(null);
