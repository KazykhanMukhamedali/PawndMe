import { useState } from "react";
import { ArrowRight } from "lucide-react";
import { api } from "../services/api";
import Paw from "./Paw";

export default function PetCard({ pet, account, onRemoved }) {
  const [favorite, setFavorite] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const isFavorite = favorite ?? pet.is_favorite;

  async function toggleFavorite() {
    if (!account.user) {
      location.hash = account.loginLink.slice(1);
      return;
    }
    setBusy(true);
    setError("");
    try {
      await api(`/favorites/${pet.id}/`, {
        token: account.token, method: isFavorite ? "DELETE" : "POST",
      });
      setFavorite(!isFavorite);
      if (isFavorite) onRemoved?.();
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <article className="pet-card">
      <div className="pet-image">
        {pet.photos[0] ? <img src={pet.photos[0]} alt={pet.name} loading="lazy" /> :
          <div className="photo-placeholder">No photo available</div>}

        <span
          className={`pet-status ${pet.status}`}
        >
          {pet.status_label}
        </span>

        {account.user?.account_type !== "shelter_staff" && <button
          type="button"
          className={`favorite-btn ${isFavorite ? "active" : ""}`}
          aria-label={
            isFavorite
              ? `Remove ${pet.name} from favorites`
              : `Add ${pet.name} to favorites`
          }
          aria-pressed={isFavorite}
          onClick={toggleFavorite}
          disabled={busy}
        >
          {isFavorite ? "♥" : "♡"}
        </button>}
      </div>

      <div className="pet-info">
        <div className="pet-heading">
          <div>
            <h3>{pet.name}</h3>
            <p className="pet-facts">{pet.type}</p>
          </div>
          <Paw className={`paw-icon paw-${pet.type}`} />
        </div>

        <div className="pet-details pet-facts">
          <span>{pet.age ? `${pet.age} yr` : "Under 1 yr"}</span>
          {pet.personality && <span>{pet.personality}</span>}
          <span>{pet.size}</span>
        </div>

        <div className="pet-footer">
          <span>⌖ {pet.location}</span>
          <a href={`#/pets/${pet.id}`}>
            View Profile <ArrowRight size={14} aria-hidden="true" />
          </a>
        </div>
        {error && <p className="form-error" role="alert">{error}</p>}
      </div>
    </article>
  );
}
