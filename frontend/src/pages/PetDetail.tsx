import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { usePet } from "../hooks/usePet";
import { useAuth } from "../context/useAuth";
import { createConsultation } from "../api/consultations";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import SpeciesBadge from "../components/SpeciesBadge";

function PetDetail() {
  const { id } = useParams<{ id: string }>();
  const { pet, loading, error } = usePet(id!);
  const { user } = useAuth();
  const navigate = useNavigate();

  const [showForm, setShowForm] = useState(false);
  const [preferredTime, setPreferredTime] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  if (loading)
    return <div className="py-12 text-muted-foreground">Loading...</div>;
  if (error || !pet)
    return <div className="py-12 text-muted-foreground">Pet not found.</div>;

  function handleRequestClick() {
    if (!user) {
      navigate("/login");
      return;
    }
    setShowForm(true);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitError(null);
    try {
      await createConsultation(id!, preferredTime);
      setSubmitted(true);
      setShowForm(false);
    } catch {
      setSubmitError("Failed to submit request — please try again");
    }
  }

  return (
    <div className="grid grid-cols-1 gap-10 py-10 md:grid-cols-2">
      <div className="aspect-[4/3] w-full overflow-hidden rounded-xl bg-muted">
        {pet.image_url && (
          <img
            src={pet.image_url}
            alt={pet.name}
            className="size-full object-cover"
          />
        )}
      </div>

      <div className="flex flex-col gap-4">
        <SpeciesBadge species={pet.species} />
        <h1 className="text-3xl font-bold">{pet.name}</h1>
        <p className="text-sm text-muted-foreground">{pet.breed}</p>
        <p className="leading-relaxed">{pet.description}</p>

        {submitted && (
          <div className="rounded-lg bg-accent px-4 py-3 text-sm text-accent-foreground">
            Request submitted — we&apos;ll be in touch.
          </div>
        )}

        {!submitted && !showForm && (
          <Button size="lg" className="mt-2 w-fit" onClick={handleRequestClick}>
            Request adoption consultation
          </Button>
        )}

        {showForm && (
          <form
            className="flex max-w-sm flex-col gap-3 pt-2"
            onSubmit={handleSubmit}
          >
            <p className="text-sm text-muted-foreground">
              We&apos;ll contact you at {user?.email}. Just pick a callback date:
            </p>
            <Input
              type="date"
              value={preferredTime}
              onChange={(e) => setPreferredTime(e.target.value)}
              required
            />
            <Button type="submit" className="w-fit">
              Submit
            </Button>
            {submitError && (
              <p className="text-sm text-destructive">{submitError}</p>
            )}
          </form>
        )}
      </div>
    </div>
  );
}

export default PetDetail;
