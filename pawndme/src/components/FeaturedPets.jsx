import { Load, useApi } from "./PageControls";
import { PetGrid } from "../pages/Pets";

export default function FeaturedPets({ account }) {
  const state = useApi("/animals/", account.token);
  return (
    <section className="featured section" id="pets">
      <div className="container">
        <h2 className="section-title">Featured Friends</h2>
        <div className="section-link">
          <a href="#/pets" className="outline-btn">View all pets →</a>
        </div>
        <Load state={state}>{({ results }) => (
          <PetGrid pets={results.filter((pet) => pet.status === "available").slice(0, 4)} account={account}
            empty="No pets are currently available for adoption." />
        )}</Load>
      </div>
    </section>
  );
}
