import { useState } from "react";
import { usePets, PETS_PAGE_SIZE } from "../hooks/usePets";
import PetCard from "../components/PetCard";
import { Button } from "@/components/ui/button";

const SPECIES_OPTIONS = [
  { label: "All", value: undefined },
  { label: "Dog", value: "dog" },
  { label: "Cat", value: "cat" },
] as const;

function Pets() {
  const [page, setPage] = useState(1);
  const [species, setSpecies] = useState<string | undefined>(undefined);
  const { pets, total, loading, error } = usePets(page, species);
  const totalPages = Math.max(1, Math.ceil(total / PETS_PAGE_SIZE));

  function goToPage(next: number) {
    setPage(next);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function selectSpecies(next: string | undefined) {
    setSpecies(next);
    setPage(1);
  }

  return (
    <div className="flex flex-col gap-6 py-10">
      <h1 className="text-3xl font-bold">Pets</h1>

      <div className="flex gap-2">
        {SPECIES_OPTIONS.map((opt) => (
          <Button
            key={opt.label}
            size="sm"
            variant={species === opt.value ? "default" : "outline"}
            onClick={() => selectSpecies(opt.value)}
          >
            {opt.label}
          </Button>
        ))}
      </div>

      {loading && <div className="py-12 text-muted-foreground">Loading...</div>}
      {error && <div className="py-12 text-destructive">{error}</div>}

      {!loading && !error && (
        <>
          <div className="grid grid-cols-2 gap-5 sm:grid-cols-3 lg:grid-cols-4">
            {pets.map((pet) => (
              <PetCard key={pet.id} pet={pet} />
            ))}
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-4 pt-4">
              <Button
                variant="outline"
                size="sm"
                disabled={page === 1}
                onClick={() => goToPage(page - 1)}
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
                onClick={() => goToPage(page + 1)}
              >
                Next
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Pets;
