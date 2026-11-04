import { useEffect, useState } from "react";
import PetCard from "./PetCard";
import { getFeaturedPets } from "../services/pets";

export default function FeaturedPets() {
  const [pets, setPets] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadPets() {
      try {
        const data = await getFeaturedPets();
        setPets(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadPets();
  }, []);

  function toggleFavorite(id) {
    setFavorites((previous) =>
      previous.includes(id)
        ? previous.filter((item) => item !== id)
        : [...previous, id]
    );
  }

  return (
    <section className="featured section" id="pets">
      <div className="container">
        <h2 className="section-title">Featured Friends</h2>

        <div className="section-link">
          <a href="#all-pets" className="outline-btn">
            View all pets →
          </a>
        </div>

        {loading && <p>Loading pets...</p>}
        {error && <p role="alert">{error}</p>}

        {!loading && !error && (
          <div className="pets-grid">
            {pets.map((pet) => (
              <PetCard
                key={pet.id}
                pet={pet}
                isFavorite={favorites.includes(pet.id)}
                onToggleFavorite={toggleFavorite}
              />
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
