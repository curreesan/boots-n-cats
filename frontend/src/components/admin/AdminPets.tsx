import { useState } from "react";
import { usePets, PETS_PAGE_SIZE } from "../../hooks/usePets";
import { createPet, updatePet, deletePet } from "../../api/admin";
import type { Pet } from "../../types/pet";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type PetFormState = Omit<Pet, "id">;

function AdminPets() {
  const [page, setPage] = useState(1);
  const { pets, total, loading } = usePets(page);
  const totalPages = Math.max(1, Math.ceil(total / PETS_PAGE_SIZE));

  const [form, setForm] = useState<PetFormState>({
    name: "",
    species: "dog",
    breed: "",
    description: "",
    image_url: null,
  });

  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState<PetFormState | null>(null);

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    await createPet(form);
    window.location.reload();
  }

  async function handleDelete(id: string) {
    await deletePet(id);
    window.location.reload();
  }

  function startEdit(pet: Pet) {
    setEditingId(pet.id);
    setEditForm({
      name: pet.name,
      species: pet.species,
      breed: pet.breed,
      description: pet.description,
      image_url: pet.image_url,
    });
  }

  function cancelEdit() {
    setEditingId(null);
    setEditForm(null);
  }

  async function handleSaveEdit(id: string) {
    if (!editForm) return;
    await updatePet(id, editForm);
    window.location.reload();
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Pets</CardTitle>
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
            placeholder="Breed"
            value={form.breed}
            onChange={(e) => setForm({ ...form, breed: e.target.value })}
            required
          />
          <Input
            className="w-56"
            placeholder="Description"
            value={form.description}
            onChange={(e) =>
              setForm({ ...form, description: e.target.value })
            }
            required
          />
          <Button type="submit">Add Pet</Button>
        </form>

        {loading ? (
          <p className="text-sm text-muted-foreground">Loading...</p>
        ) : (
          <div className="divide-y divide-border overflow-hidden rounded-lg border border-border">
            {pets.map((pet) =>
              editingId === pet.id && editForm ? (
                <div
                  key={pet.id}
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
                    value={editForm.breed}
                    onChange={(e) =>
                      setEditForm({ ...editForm, breed: e.target.value })
                    }
                  />
                  <Input
                    className="w-56"
                    value={editForm.description}
                    onChange={(e) =>
                      setEditForm({
                        ...editForm,
                        description: e.target.value,
                      })
                    }
                  />
                  <Button size="sm" onClick={() => handleSaveEdit(pet.id)}>
                    Save
                  </Button>
                  <Button variant="outline" size="sm" onClick={cancelEdit}>
                    Cancel
                  </Button>
                </div>
              ) : (
                <div
                  key={pet.id}
                  className="flex items-center justify-between px-4 py-3 text-sm"
                >
                  <span>
                    {pet.name} — {pet.breed}
                  </span>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => startEdit(pet)}
                    >
                      Edit
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      className="border-destructive text-destructive hover:bg-destructive hover:text-white"
                      onClick={() => handleDelete(pet.id)}
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

export default AdminPets;
