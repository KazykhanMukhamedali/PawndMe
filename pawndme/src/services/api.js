const base = (import.meta.env.VITE_API_URL || "/api").replace(/\/$/, "");

export async function api(path, { token, body, method = "GET", signal } = {}) {
  const headers = {};
  if (token) headers.Authorization = `Token ${token}`;
  if (body && !(body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(body);
  }
  const response = await fetch(base + path, { method, headers, body, signal });
  if (response.status === 204) return null;
  const data = await response.json().catch(() => null);
  if (!response.ok || data === null) {
    const message = data && Object.entries(data).map(([field, value]) =>
      field === "detail" ? value : `${field.replaceAll("_", " ")}: ${value}`
    ).join(" · ");
    throw Object.assign(new Error(message || "Could not reach the PawndMe API."), {
      status: response.status,
    });
  }
  return data;
}
