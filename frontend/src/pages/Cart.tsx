import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../context/useCart";
import { useAuth } from "../context/useAuth";
import { API_BASE_URL } from "../api/config";
import "../styles/Cart.css";

function Cart() {
  const { items, increaseQuantity, decreaseQuantity, removeItem, clearCart } =
    useCart();
  const { user } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const total = items.reduce(
    (sum, line) => sum + line.product.price * line.quantity,
    0,
  );

  async function handleCheckout() {
    if (!user) {
      navigate("/login");
      return;
    }

    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/orders`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
          items.map((line) => ({
            product_id: line.product.id,
            quantity: line.quantity,
          })),
        ),
      });

      if (!response.ok) throw new Error("Checkout failed");

      clearCart();
      navigate("/orders");
    } catch {
      setError("Checkout failed — please try again");
    }
  }

  if (items.length === 0) {
    return (
      <div className="cart">
        <h1 className="cart__heading">Cart</h1>
        <div className="cart__empty">Your cart is empty.</div>
      </div>
    );
  }

  return (
    <div className="cart">
      <h1 className="cart__heading">Cart</h1>
      <table className="cart__table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Unit Price</th>
            <th>Quantity</th>
            <th>Line Total</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {items.map((line) => (
            <tr key={line.product.id}>
              <td>{line.product.name}</td>
              <td>₹{line.product.price}</td>
              <td>
                <div className="cart__qty">
                  <button onClick={() => decreaseQuantity(line.product.id)}>
                    -
                  </button>
                  <span>{line.quantity}</span>
                  <button onClick={() => increaseQuantity(line.product.id)}>
                    +
                  </button>
                </div>
              </td>
              <td>₹{line.product.price * line.quantity}</td>
              <td>
                <button
                  className="cart__remove"
                  onClick={() => removeItem(line.product.id)}
                >
                  Remove
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="cart__footer">
        <div className="cart__total">Total: ₹{total}</div>
        <button className="cart__checkout" onClick={handleCheckout}>
          Place Order
        </button>
      </div>
      {error && <div className="cart__error">{error}</div>}
    </div>
  );
}

export default Cart;
