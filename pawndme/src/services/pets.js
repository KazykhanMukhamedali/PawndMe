
import { pets } from "../data/pets";

const API_URL = import.meta.env.VITE_API_URL;
const USE_MOCKS = import.meta.env.VITE_USE_MOCKS !== "false";

export async function getFeaturedPets() {
  if (USE_MOCKS) {
    return pets;
  }

  const response = await fetch(`${API_URL}/pets/featured`);

  if (!response.ok) {
    throw new Error("Failed to fetch pets");
  }

  return response.json();
}
