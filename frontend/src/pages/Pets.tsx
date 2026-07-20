import { usePets } from "../hooks/usePets";
import PetCard from "../components/PetCard";
import "../styles/Pets.css";

function Pets() {
  const { pets, loading, error } = usePets();

  if (loading) return <div className="products__status">Loading...</div>;
  if (error) return <div className="products__status">{error}</div>;

  return (
    <div className="products">
      <h1 className="products__heading">Pets</h1>
      <div className="products__list">
        {pets.map((pet) => (
          <PetCard key={pet.id} pet={pet} />
        ))}
      </div>
    </div>
  );
}

export default Pets;
