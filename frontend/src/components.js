import { navigate } from "./router.js";
import { getUser, logout } from "./auth.js";

export function icon(name, size = 17) {
  return `<i data-lucide="${name}" width="${size}" height="${size}"></i>`;
}

export function refreshIcons() {
  if (window.lucide) window.lucide.createIcons();
}

export function publicHeader() {
  return `
    <header class="public-header">
      <a class="brand" href="/" data-link>
        <span class="brand-mark">LM</span>
        <span>
          <strong>DIGITAL LEGAL METROLOGY PORTAL</strong>
          <small>Verification & lifecycle management</small>
        </span>
      </a>
      <nav class="public-nav">
        <a href="/" data-link>Home</a>
        <a href="/#services">Services</a>
        <a href="/public/verify/" data-link>Public Verification</a>
        <a href="/#about">About</a>
        <a class="btn btn-primary btn-small" href="/login" data-link>Sign In</a>
      </nav>
      <button class="mobile-menu" id="mobile-menu" aria-label="Open menu">${icon("menu")}</button>
    </header>
  `;
}

export function portalShell(content, active = "dashboard") {
  const user = getUser();
  const role = user?.role || "OWNER";
  const items = role === "OWNER"
    ? [["dashboard", "layout-dashboard", "Dashboard"], ["instruments", "scale", "My Instruments"], ["applications", "clipboard-list", "Applications"], ["certificates", "badge-check", "Certificates"], ["documents", "files", "Documents"]]
    : role === "GATC"
    ? [["dashboard", "layout-dashboard", "Dashboard"], ["applications", "clipboard-list", "Assigned Applications"], ["inspections", "clipboard-check", "Inspections"]]
    : [["dashboard", "layout-dashboard", "Dashboard"], ["applications", "clipboard-list", "Applications"], ["certificates", "badge-check", "Certificates"], ["expiry", "calendar-clock", "Expiry Monitoring"], ["search", "search", "Search"]];

  return `
    <div class="portal">
      <aside class="sidebar" id="sidebar">
        <div class="sidebar-brand">
          <span class="brand-mark">LM</span>
          <div><strong>LEGAL METROLOGY</strong><small>Digital Portal</small></div>
        </div>
        <div class="role-label">${role}</div>
        <nav class="side-nav">
          ${items.map(([key, ic, label]) => `<a class="${active === key ? "active" : ""}" href="/portal/${key}" data-link>${icon(ic)}<span>${label}</span></a>`).join("")}
        </nav>
        <div class="sidebar-bottom">
          <a href="/portal/profile" data-link>${icon("user-round")}<span>Profile</span></a>
          <button id="logout-btn">${icon("log-out")}<span>Logout</span></button>
        </div>
      </aside>
      <main class="portal-main">
        <header class="portal-topbar">
          <button class="sidebar-toggle" id="sidebar-toggle">${icon("menu")}</button>
          <div class="topbar-title">Digital Legal Metrology Portal</div>
          <div class="user-summary">
            <span class="user-name">${user?.first_name || user?.username || "User"}</span>
            <span class="user-role">${role}</span>
          </div>
        </header>
        <section class="page-content">${content}</section>
      </main>
    </div>
  `;
}

export function bindNavigation() {
  document.querySelectorAll("[data-link]").forEach((a) => {
    a.addEventListener("click", (e) => {
      const href = a.getAttribute("href");
      if (!href || href.startsWith("#")) return;
      e.preventDefault();
      navigate(href);
    });
  });
  document.getElementById("logout-btn")?.addEventListener("click", () => {
    logout();
    navigate("/");
  });
  document.getElementById("sidebar-toggle")?.addEventListener("click", () => {
    document.getElementById("sidebar")?.classList.toggle("open");
  });
  document.getElementById("mobile-menu")?.addEventListener("click", () => {
    document.querySelector(".public-nav")?.classList.toggle("open");
  });
}
