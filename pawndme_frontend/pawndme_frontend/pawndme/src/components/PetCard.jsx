export default function PetCard({
  pet,
  isFavorite,
  onToggleFavorite,
}) {
  return (
    <article className="pet-card">
      <div className="pet-image">
        <img src={pet.image} alt={pet.name} />

        <span
          className={`pet-status ${pet.status.toLowerCase()}`}
        >
          {pet.status}
        </span>

        <button
          type="button"
          className={`favorite-btn ${isFavorite ? "active" : ""}`}
          aria-label={
            isFavorite
              ? `Remove ${pet.name} from favorites`
              : `Add ${pet.name} to favorites`
          }
          aria-pressed={isFavorite}
          onClick={() => onToggleFavorite(pet.id)}
        >
          {isFavorite ? "♥" : "♡"}
        </button>
      </div>

      <div className="pet-info">
        <div className="pet-heading">
          <div>
            <h3>{pet.name}</h3>
            <p>{pet.breed}</p>
          </div>
          <span className="paw-icon">🐾</span>
        </div>

        <div className="pet-details">
          <span>{pet.age}</span>
          <span>{pet.gender}</span>
          <span>{pet.size}</span>
        </div>

        <div className="pet-footer">
          <span>⌖ {pet.location}</span>
          <a href={`#pet-${pet.id}`}>
            View Profile →
          </a>
        </div>
      </div>
    </article>
  );
}
