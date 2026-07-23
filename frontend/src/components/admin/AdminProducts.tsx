import { useState } from "react";
import { useProducts, PRODUCTS_PAGE_SIZE } from "../../hooks/useProducts";
import { createProduct, updateProduct, deleteProduct } from "../../api/admin";
import type { Product } from "../../types/product";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type ProductFormState = Omit<Product, "id">;

function AdminProducts() {
  const [page, setPage] = useState(1);
  const { products, total, loading } = useProducts(page);
  const totalPages = Math.max(1, Math.ceil(total / PRODUCTS_PAGE_SIZE));

  const [form, setForm] = useState<ProductFormState>({
    name: "",
    species: "dog",
    category: "",
    price: 0,
    stock_quantity: 0,
    image_url: null,
  });

  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState<ProductFormState | null>(null);

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    await createProduct(form);
    window.location.reload();
  }

  async function handleDelete(id: string) {
    await deleteProduct(id);
    window.location.reload();
  }

  function startEdit(product: Product) {
    setEditingId(product.id);
    setEditForm({
      name: product.name,
      species: product.species,
      category: product.category,
      price: product.price,
      stock_quantity: product.stock_quantity,
      image_url: product.image_url,
    });
  }

  function cancelEdit() {
    setEditingId(null);
    setEditForm(null);
  }

  async function handleSaveEdit(id: string) {
    if (!editForm) return;
    await updateProduct(id, editForm);
    window.location.reload();
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Products</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-6">
        <form
          className="flex flex-wrap items-end gap-3 border-b border-border pb-6"
          onSubmit={handleAdd}
        >
          <Input
            className="w-40"
            placeholder="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
          />
          <select
            className="h-9 rounded-md border border-input bg-transparent px-3 text-sm"
            value={form.species}
            onChange={(e) => setForm({ ...form, species: e.target.value })}
          >
            <option value="dog">Dog</option>
            <option value="cat">Cat</option>
          </select>
          <Input
            className="w-32"
            placeholder="Category"
            value={form.category}
            onChange={(e) => setForm({ ...form, category: e.target.value })}
            required
          />
          <Input
            className="w-28"
            type="number"
            placeholder="Price"
            value={form.price}
            onChange={(e) =>
              setForm({ ...form, price: Number(e.target.value) })
            }
            required
          />
          <Input
            className="w-28"
            type="number"
            placeholder="Stock"
            value={form.stock_quantity}
            onChange={(e) =>
              setForm({ ...form, stock_quantity: Number(e.target.value) })
            }
            required
          />
          <Button type="submit">Add Product</Button>
        </form>

        {loading ? (
          <p className="text-sm text-muted-foreground">Loading...</p>
        ) : (
          <div className="divide-y divide-border overflow-hidden rounded-lg border border-border">
            {products.map((product) =>
              editingId === product.id && editForm ? (
                <div
                  key={product.id}
                  className="flex flex-wrap items-end gap-3 px-4 py-3"
                >
                  <Input
                    className="w-40"
                    value={editForm.name}
                    onChange={(e) =>
                      setEditForm({ ...editForm, name: e.target.value })
                    }
                  />
                  <select
                    className="h-9 rounded-md border border-input bg-transparent px-3 text-sm"
                    value={editForm.species}
                    onChange={(e) =>
                      setEditForm({ ...editForm, species: e.target.value })
                    }
                  >
                    <option value="dog">Dog</option>
                    <option value="cat">Cat</option>
                  </select>
                  <Input
                    className="w-32"
                    value={editForm.category}
                    onChange={(e) =>
                      setEditForm({ ...editForm, category: e.target.value })
                    }
                  />
                  <Input
                    className="w-28"
                    type="number"
                    value={editForm.price}
                    onChange={(e) =>
                      setEditForm({
                        ...editForm,
                        price: Number(e.target.value),
                      })
                    }
                  />
                  <Input
                    className="w-28"
                    type="number"
                    value={editForm.stock_quantity}
                    onChange={(e) =>
                      setEditForm({
                        ...editForm,
                        stock_quantity: Number(e.target.value),
                      })
                    }
                  />
                  <Button size="sm" onClick={() => handleSaveEdit(product.id)}>
                    Save
                  </Button>
                  <Button variant="outline" size="sm" onClick={cancelEdit}>
                    Cancel
                  </Button>
                </div>
              ) : (
                <div
                  key={product.id}
                  className="flex items-center justify-between px-4 py-3 text-sm"
                >
                  <span>
                    {product.name} — ₹{product.price}
                  </span>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => startEdit(product)}
                    >
                      Edit
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      className="border-destructive text-destructive hover:bg-destructive hover:text-white"
                      onClick={() => handleDelete(product.id)}
                    >
                      Delete
                    </Button>
                  </div>
                </div>
              ),
            )}
          </div>
        )}

        {totalPages > 1 && (
          <div className="flex items-center justify-center gap-4">
            <Button
              variant="outline"
              size="sm"
              disabled={page === 1}
              onClick={() => setPage((p) => p - 1)}
            >
              Previous
            </Button>
            <span className="text-sm text-muted-foreground">
              Page {page} of {totalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              disabled={page === totalPages}
              onClick={() => setPage((p) => p + 1)}
            >
              Next
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default AdminProducts;
