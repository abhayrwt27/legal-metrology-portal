import { getUser, isLoggedIn } from "./auth.js";

export function route(pathname = window.location.pathname) {
  if (pathname.startsWith("/public/verify/")) return { page: "public-verify" };
  if (pathname === "/login") return { page: "login" };
  if (pathname === "/register") return { page: "register" };
  if (pathname.startsWith("/portal")) {
    if (!isLoggedIn()) return { page: "login" };
    return { page: "dashboard", user: getUser() };
  }
  return { page: "home" };
}

export function navigate(path) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}
