import { useState } from "react";
import { ActionForm, Field, Load, any, personalities, sizes, statuses, types, useApi } from "../components/PageControls";
import { api } from "../services/api";

export function Account({ account, logout }) {
  const [revision, setRevision] = useState(0);
  const staff = account.user?.account_type === "shelter_staff";
  const animals = useApi(staff ? "/my-animals/" : null, account.token, revision);
  const applications = useApi(staff ? "/applications/" : null, account.token, revision);
  if (!account.user) return <section className="container inner-page"><h1>My Account</h1><a href={account.loginLink}>Log in</a></section>;

  return (
    <section className="container inner-page">
      <h1>My Account</h1>
      <p>{account.user.email} · {account.user.account_type_label}</p>
      <ActionForm onAction={logout}><button className="outline-btn">Log out</button></ActionForm>
      {staff && <>
        <div className="section-bar">
          <h2>{account.user.shelter?.name || "Shelter"} · Animals</h2>
          <a href="#/account/animals/new" className="primary-btn">Add animal</a>
        </div>
        <Load state={animals}>{({ results }) => results.length ? (
          <ul className="account-list">{results.map((animal) => (
            <li key={animal.id}>
              <div>
                <a href={`#/pets/${animal.id}`}>{animal.name}</a>
                <p>{animal.status_label} · <a href={`#/account/animals/${animal.id}`}>Edit profile</a></p>
              </div>
              <ActionForm onAction={async (data) => {
                await api(`/animals/${animal.id}/status/`, { token: account.token, method: "PATCH", body: Object.fromEntries(data) });
                setRevision((current) => current + 1);
              }}>
                <Field label="Status" name="status" options={statuses} defaultValue={animal.status} />
                <button className="outline-btn">Update status</button>
              </ActionForm>
            </li>
          ))}</ul>
        ) : <p>No animals in your shelter yet.</p>}</Load>
        <h2>Adoption applications</h2>
        <Load state={applications}>{({ results }) => results.length ? (
          <ul className="account-list">{results.map((application) => (
            <li key={application.id}>
              <div>
                <h3><a href={`#/pets/${application.animal.id}`}>{application.animal.name}</a> · {application.full_name}</h3>
                <p>{application.email} · {application.phone}</p>
                <p>{application.message}</p>
              </div>
            </li>
          ))}</ul>
        ) : <p>No applications yet.</p>}</Load>
      </>}
    </section>
  );
}

export function AnimalEditor({ id, account }) {
  const staff = account.user?.account_type === "shelter_staff";
  const state = useApi(staff && id ? `/animals/${id}/` : null, account.token);
  return (
    <section className="container inner-page">
      <a href="#/account">← My Account</a>
      <h1>{id ? "Edit animal profile" : "Add animal"}</h1>
      {staff ? id ? <Load state={state}>{(animal) =>
        animal.shelter.id === account.user.shelter?.id ? <AnimalForm animal={animal} token={account.token} /> :
          <p>You can only edit animals from your shelter.</p>
      }</Load> : <AnimalForm token={account.token} /> :
        <p>{account.user ? "This page is for shelter staff." : <a href={account.loginLink}>Log in as shelter staff</a>}</p>}
    </section>
  );
}

function AnimalForm({ animal, token }) {
  async function save(data) {
    const photos = data.getAll("photos").filter((photo) => photo.size > 0);
    data.delete("photos");
    for (const photo of photos) data.append("photos", photo);
    await api(animal ? `/animals/${animal.id}/` : "/animals/", {
      token, method: animal ? "PATCH" : "POST", body: data,
    });
    location.hash = "/account";
  }

  return (
    <>
      <ActionForm onAction={save}>
        <Field label="Name" name="name" defaultValue={animal?.name} required maxLength={50} />
        <Field label="Type" name="type" options={types} defaultValue={animal?.type} />
        <Field label="Age in years (0 if under 1)" name="age" type="number" min={0} max={32767} defaultValue={animal?.age} required />
        <Field label="Size" name="size" options={sizes} defaultValue={animal?.size} />
        <Field label="Location" name="location" defaultValue={animal?.location} required maxLength={100} />
        <Field label="Personality" name="personality" options={any("Select personality", personalities)} defaultValue={animal?.personality} />
        <Field label="Health information" name="health_info" defaultValue={animal?.health_info} multiline />
        <Field label="Description" name="description" defaultValue={animal?.description} multiline maxLength={1000} />
        <Field label={animal ? "Replace photos (up to 5 JPG or PNG files)" : "Photos (1–5 JPG or PNG files)"}
          name="photos" type="file" accept="image/jpeg,image/png" multiple required={!animal} />
        <button className="primary-btn">Save profile</button>
      </ActionForm>
      {animal && <ActionForm onAction={async () => {
        if (!window.confirm(`Delete ${animal.name}’s profile and its adoption applications?`)) return;
        await api(`/animals/${animal.id}/`, { token, method: "DELETE" });
        location.hash = "/account";
      }}><button className="outline-btn danger-btn">Delete profile</button></ActionForm>}
    </>
  );
}
