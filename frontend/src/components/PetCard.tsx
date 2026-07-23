import { Link } from "react-router-dom";
import type { Pet } from "../types/pet";
import { Card, CardContent } from "@/components/ui/card";
import SpeciesBadge from "./SpeciesBadge";

type PetCardProps = {
  pet: Pet;
};

function PetCard({ pet }: PetCardProps) {
  return (
    <Link to={`/pets/${pet.id}`}>
      <Card className="gap-0 overflow-hidden py-0 transition-shadow hover:shadow-md">
        <div className="aspect-[4/3] w-full overflow-hidden bg-muted">
          {pet.image_url && (
            <img
              src={pet.image_url}
              alt={pet.name}
              className="size-full object-cover"
              loading="lazy"
            />
          )}
        </div>
        <CardContent className="flex flex-col gap-1 px-4 py-4">
          <div className="flex items-center justify-between gap-2">
            <p className="truncate font-medium">{pet.name}</p>
            <SpeciesBadge species={pet.species} />
          </div>
          <p className="text-sm text-muted-foreground">{pet.breed}</p>
        </CardContent>
      </Card>
    </Link>
  );
}

export default PetCard;
