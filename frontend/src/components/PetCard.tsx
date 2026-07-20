import { Link } from "react-router-dom";
import type { Pet } from "../types/pet";
import SpeciesBadge from "./SpeciesBadge";
import "../styles/PetCard.css";

type PetCardProps = {
  pet: Pet;
};

function PetCard({ pet }: PetCardProps) {
  return (
    <Link to={`/pets/${pet.id}`} className="pet-row">
      <SpeciesBadge species={pet.species} />
      <span className="pet-row__name">{pet.name}</span>
      <span className="pet-row__breed">{pet.breed}</span>
    </Link>
  );
}

export default PetCard;
