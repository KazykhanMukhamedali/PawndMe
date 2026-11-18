import { useState } from "react";
import PetCard from "../components/PetCard";
import { ActionForm, Field, Load, any, personalities, sizes, types, useApi } from "../components/PageControls";
import { api } from "../services/api";

const ages = [["up_to_1", "Up to 1 year"], ["1_3", "2–3 years"], ["4_7", "4–7 years"], ["8_plus", "8+ years"]];
const pageSize = 12;

export function PetGrid({ pets, account, empty = "No pets found.", onRemoved }) {
  if (!pets.length) return <p className="empty-state">{empty}</p>;
  return (
    <div className="pets-grid">
      {pets.map((pet) => <PetCard key={pet.id} pet={pet} account={account} onRemoved={onRemoved} />)}
    </div>
  );
}

export function Catalog({ query, account }) {
  const params = new URLSearchParams(query);
  const page = Math.max(1, Number(params.get("page")) || 1);
  params.delete("page");
  const state = useApi(`/animals/?${params}`, account.token);
  const locations = useApi("/animals/locations/");
  const cityOptions = new Set(locations.data ?? []);
  if (params.get("location")) cityOptions.add(params.get("location"));

  function filter(data) {
    const next = new URLSearchParams();
    for (const [name, value] of data) {
      if (value.trim()) next.set(name, value.trim());
    }
    location.hash = `/pets${next.size ? `?${next}` : ""}`;
  }

  return (
    <>
      <div className="catalog-banner">
        <div className="container">
          <h1>Find Your Perfect <span>Companion</span></h1>
          <p>Meet the pets waiting for a place to call home.</p>
        </div>
      </div>
      <section className="container browse-page">
        <ActionForm key={params.toString()} onAction={filter} className="filter-form">
          <Field label="Search by name" name="search" type="search" placeholder="Enter a pet’s name" defaultValue={params.get("search") ?? ""} />
          <div className="filter-row">
            <Field label="Animal" name="type" options={any("All animals", types)} defaultValue={params.get("type") ?? ""} />
            <Field label="Size" name="size" options={any("Any size", sizes)} defaultValue={params.get("size") ?? ""} />
            <Field label="Age" name="age_group" options={any("Any age", ages)} defaultValue={params.get("age_group") ?? ""} />
            <Field label="Personality" name="personality" options={any("Any personality", personalities)} defaultValue={params.get("personality") ?? ""} />
            <Field label="Location" name="location" options={any("Any location", [...cityOptions].map((city) => [city, city]))} defaultValue={params.get("location") ?? ""} />
            <button className="primary-btn">Search</button>
            <a href="#/pets">Clear</a>
          </div>
        </ActionForm>
        <Load state={state}>{({ results }) => {
          const pages = Math.max(1, Math.ceil(results.length / pageSize));
          const current = Math.min(Math.floor(page), pages);
          const pageLink = (number) => {
            const next = new URLSearchParams(params);
            next.set("page", number);
            return `#/pets?${next}`;
          };
          return (
            <>
              <p className="results-count">{results.length} {results.length === 1 ? "pet" : "pets"} found</p>
              <PetGrid pets={results.slice((current - 1) * pageSize, current * pageSize)} account={account} />
              {pages > 1 && <nav className="pagination" aria-label="Catalog pages">
                {current > 1 && <a href={pageLink(current - 1)}>Previous</a>}
                <span>Page {current} of {pages}</span>
                {current < pages && <a href={pageLink(current + 1)}>Next</a>}
              </nav>}
            </>
          );
        }}</Load>
      </section>
    </>
  );
}

export function Favorites({ account }) {
  const [revision, setRevision] = useState(0);
  const adopter = account.user?.account_type === "adopter";
  const state = useApi(adopter ? "/favorites/" : null, account.token, revision);

  return (
    <section className="container inner-page">
      <h1>Your Favorite Paws</h1>
      {adopter ? <Load state={state}>{({ results }) =>
        <PetGrid pets={results} account={account} empty="You haven’t saved any pets yet." onRemoved={() => setRevision((value) => value + 1)} />
      }</Load> : account.user ? <p>Favorites are available to adopters.</p> :
        <p><a href={account.loginLink}>Log in</a> to see your favorite pets.</p>}
    </section>
  );
}

export function PetProfile({ id, account }) {
  const state = useApi(`/animals/${id}/`, account.token);
  const [sent, setSent] = useState(false);

  return (
    <section className="container inner-page">
      <a href="#/pets">← Explore Pets</a>
      <Load state={state}>{(pet) => (
        <div className="profile-layout">
          <div className="pet-gallery">
            {pet.photos.length ? pet.photos.map((photo, index) => (
              <img key={photo} src={photo} alt={`${pet.name}, photo ${index + 1}`} />
            )) : <div className="photo-placeholder">No photo available</div>}
          </div>
          <div>
            <p className="eyebrow">{pet.status_label}</p>
            <h1>{pet.name}</h1>
            <p className="pet-facts">{pet.type} · {pet.age ? `${pet.age} yr` : "Under 1 yr"} · {pet.size}{pet.personality && ` · ${pet.personality}`}</p>
            <p>{pet.shelter.name} · {pet.location}</p>
            {pet.description && <><h2>About {pet.name}</h2><p>{pet.description}</p></>}
            {pet.health_info && <><h2>Health information</h2><p>{pet.health_info}</p></>}
            {(sent || pet.has_applied) ? <p role="status">Your adoption application has been sent.</p> :
              pet.status === "available" && (account.user?.account_type === "adopter" ? (
                <>
                  <h2>Apply to adopt {pet.name}</h2>
                  <ActionForm onAction={async (data) => {
                    await api(`/animals/${id}/apply/`, { token: account.token, method: "POST", body: Object.fromEntries(data) });
                    setSent(true);
                  }}>
                    <Field label="Full name" name="full_name" required maxLength={100} />
                    <Field label="Phone number" name="phone" type="tel" required maxLength={30} />
                    <Field label="Email" name="email" type="email" defaultValue={account.user.email} required />
                    <Field label="Tell us about your home and experience with pets" name="message" multiline required maxLength={500} />
                    <button className="primary-btn">Send application</button>
                  </ActionForm>
                </>
              ) : !account.user && <p><a href={account.loginLink}>Log in</a> to apply for adoption.</p>)}
          </div>
        </div>
      )}</Load>
    </section>
  );
}
