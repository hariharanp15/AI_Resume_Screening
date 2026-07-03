const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export function getToken() {
  return localStorage.getItem("token");
}

export function setSession(session) {
  localStorage.setItem("token", session.access_token);
  localStorage.setItem("role", session.role);
  localStorage.setItem("name", session.full_name);
}

export function clearSession() {
  localStorage.clear();
}

export async function api(path, options = {}) {
  const headers = new Headers(options.headers || {});
  if (!(options.body instanceof FormData)) headers.set("Content-Type", "application/json");
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || "Request failed");
  }
  if (response.status === 204) return null;
  return response.json();
}
