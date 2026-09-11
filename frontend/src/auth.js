import { api } from "./api.js";

export function getUser() {
  const value = localStorage.getItem("user");
  return value ? JSON.parse(value) : null;
}

export function isLoggedIn() {
  return Boolean(localStorage.getItem("access_token"));
}

export async function login(username, password) {
  const data = await api.post("/auth/login/", { username, password });
  localStorage.setItem("access_token", data.access);
  localStorage.setItem("refresh_token", data.refresh);
  localStorage.setItem("user", JSON.stringify(data.user));
  return data.user;
}

export async function register(payload) {
  return api.post("/auth/register/", payload);
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
}
