import "./style.css";
import { renderHome, renderLogin, renderRegister, renderPublicVerify, renderDashboard, renderInstruments, renderApplications, renderCertificates } from "./pages.js";
import { route } from "./router.js";

async function render() {
  const r = route();
  if (r.page === "home") return renderHome();
  if (r.page === "login") return renderLogin();
  if (r.page === "register") return renderRegister();
  if (r.page === "public-verify") return renderPublicVerify(window.location.pathname.split("/public/verify/")[1] || "");
  const section = window.location.pathname.split("/portal/")[1] || "dashboard";
  if (section === "dashboard") return renderDashboard();
  if (section === "instruments") return renderInstruments();
  if (section === "applications" || section === "inspections") return renderApplications();
  if (section === "certificates" || section === "expiry") return renderCertificates();
  return renderDashboard();
}

window.addEventListener("popstate", render);
render();
