import { useState } from "react";
import { usePets } from "../../hooks/usePets";
import { createPet, deletePet } from "../../api/admin";
import "../../styles/AdminForm.css";

function AdminPets() {
  const { pets, loading } = usePets();

  const [form, setForm] = useState({
    name: "",
    species: "dog",
    breed: "",
    description: "",
    image_url: null as string | null,
  });

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    await createPet(form);
    window.location.reload();
  }

  async function handleDelete(id: string) {
    await deletePet(id);
    window.location.reload();
  }

  return (
    <div className="admin-section">
      <h2 className="admin-section__heading">Pets</h2>

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
          placeholder="Breed"
          value={form.breed}
          onChange={(e) => setForm({ ...form, breed: e.target.value })}
          required
        />
        <input
          placeholder="Description"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          required
        />
        <button type="submit" className="admin-form__submit">
          Add Pet
        </button>
      </form>

      {loading ? (
        <div className="admin-section__status">Loading...</div>
      ) : (
        <div className="admin-section__list">
          {pets.map((pet) => (
            <div key={pet.id} className="admin-section__row">
              <span>
                {pet.name} — {pet.breed}
              </span>
              <button
                className="admin-section__delete"
                onClick={() => handleDelete(pet.id)}
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

export default AdminPets;
