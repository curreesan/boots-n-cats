import { useState } from "react";
import { useProducts } from "../../hooks/useProducts";
import { createProduct, deleteProduct } from "../../api/admin";
import "../../styles/AdminForm.css";

function AdminProducts() {
  const { products, loading } = useProducts();

  const [form, setForm] = useState({
    name: "",
    species: "dog",
    category: "",
    price: 0,
    stock_quantity: 0,
    image_url: null as string | null,
  });

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    await createProduct(form);
    window.location.reload();
  }

  async function handleDelete(id: string) {
    await deleteProduct(id);
    window.location.reload();
  }

  return (
    <div className="admin-section">
      <h2 className="admin-section__heading">Products</h2>

      <form className="admin-form" onSubmit={handleAdd}>
        <input
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />
        <select
          value={form.species}
          onChange={(e) => setForm({ ...form, species: e.target.value })}
        >
          <option value="dog">Dog</option>
          <option value="cat">Cat</option>
        </select>
        <input
          placeholder="Category"
          value={form.category}
          onChange={(e) => setForm({ ...form, category: e.target.value })}
          required
        />
        <input
          type="number"
          placeholder="Price"
          value={form.price}
          onChange={(e) => setForm({ ...form, price: Number(e.target.value) })}
          required
        />
        <input
          type="number"
          placeholder="Stock"
          value={form.stock_quantity}
          onChange={(e) =>
            setForm({ ...form, stock_quantity: Number(e.target.value) })
          }
          required
        />
        <button type="submit" className="admin-form__submit">
          Add Product
        </button>
      </form>

      {loading ? (
        <div className="admin-section__status">Loading...</div>
      ) : (
        <div className="admin-section__list">
          {products.map((product) => (
            <div key={product.id} className="admin-section__row">
              <span>
                {product.name} — ₹{product.price}
              </span>
              <button
                className="admin-section__delete"
                onClick={() => handleDelete(product.id)}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AdminProducts;
