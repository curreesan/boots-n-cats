import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { usePet } from "../hooks/usePet";
import { useAuth } from "../context/useAuth";
import { createConsultation } from "../api/consultations";
import SpeciesBadge from "../components/SpeciesBadge";
import "../styles/PetDetail.css";

function PetDetail() {
  const { id } = useParams<{ id: string }>();
  const { pet, loading, error } = usePet(id!);
  const { user } = useAuth();
  const navigate = useNavigate();

  const [showForm, setShowForm] = useState(false);
  const [contact, setContact] = useState("");
  const [preferredTime, setPreferredTime] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  if (loading) return <div className="pet-detail__status">Loading...</div>;
  if (error || !pet)
    return <div className="pet-detail__status">Pet not found.</div>;

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
      await createConsultation(id!, contact, preferredTime);
      setSubmitted(true);
      setShowForm(false);
    } catch {
      setSubmitError("Failed to submit request — please try again");
    }
  }

  return (
    <div className="pet-detail">
      <SpeciesBadge species={pet.species} />
      <h1 className="pet-detail__name">{pet.name}</h1>
      <div className="pet-detail__meta">{pet.breed}</div>
      <p className="pet-detail__description">{pet.description}</p>

      {submitted && (
        <div className="pet-detail__notice pet-detail__notice--success">
          Request submitted — we'll be in touch.
        </div>
      )}

      {!submitted && !showForm && (
        <button className="pet-detail__button" onClick={handleRequestClick}>
          Request adoption consultation
        </button>
      )}

      {showForm && (
        <form className="pet-detail__form" onSubmit={handleSubmit}>
          <input
            type="text"
            value={contact}
            onChange={(e) => setContact(e.target.value)}
            placeholder="Phone or email"
            required
          />
          <input
            type="text"
            value={preferredTime}
            onChange={(e) => setPreferredTime(e.target.value)}
            placeholder="Preferred time to call"
            required
          />
          <button type="submit" className="pet-detail__button">
            Submit
          </button>
          {submitError && (
            <div className="pet-detail__notice pet-detail__notice--error">
              {submitError}
            </div>
          )}
        </form>
      )}
    </div>
  );
}

export default PetDetail;
