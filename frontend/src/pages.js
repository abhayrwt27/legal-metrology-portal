import { api } from "./api.js";
import { login, register } from "./auth.js";
import { navigate } from "./router.js";
import { bindNavigation, icon, portalShell, publicHeader, refreshIcons } from "./components.js";
import Chart from "chart.js/auto";
import { Html5Qrcode } from "html5-qrcode";

function statusClass(status) {
  return String(status || "").toLowerCase().replaceAll("_", "-");
}

function statCard(label, value, ic) {
  return `<div class="stat-card"><div class="stat-icon">${icon(ic)}</div><div><span>${label}</span><strong>${value ?? 0}</strong></div></div>`;
}

export function renderHome() {
  document.getElementById("app").innerHTML = `
    ${publicHeader()}
    <main>
      <section class="hero">
        <div class="hero-copy">
          <div class="eyebrow">GOVERNMENT DIGITAL SERVICE</div>
          <h1>Trusted verification for weighing and measuring instruments.</h1>
          <p>A unified digital platform for registration, field verification, certification, lifecycle tracking and public QR-based verification.</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="/public/verify/" data-link>Verify an Instrument ${icon("arrow-right")}</a>
            <a class="btn btn-outline" href="/login" data-link>Access Portal</a>
          </div>
        </div>
        <div class="hero-panel">
          <div class="document-frame">
            <div class="document-head"><span>Digital Legal Metrology Portal</span><span>VERIFICATION RECORD</span></div>
            <div class="document-line wide"></div><div class="document-line"></div>
            <div class="document-grid"><div><small>INSTRUMENT UID</small><strong>LM-INST-2026-000001</strong></div><div><small>STATUS</small><strong class="verified">VALID</strong></div></div>
            <div class="document-seal">VERIFIED</div>
          </div>
        </div>
      </section>

      <section class="section" id="services">
        <div class="section-heading"><span class="eyebrow">PLATFORM CAPABILITIES</span><h2>One lifecycle, one trusted record.</h2></div>
        <div class="feature-grid">
          <article><div class="feature-number">01</div><h3>Instrument Identity</h3><p>Every registered instrument receives a permanent unique identity that remains unchanged across renewals.</p></article>
          <article><div class="feature-number">02</div><h3>Inspection Workflow</h3><p>Route applications from owners to LMO review, GATC assignment and field inspection with controlled status transitions.</p></article>
          <article><div class="feature-number">03</div><h3>Digital Certificates</h3><p>Generate certificate records linked directly to the instrument and preserve certificate history.</p></article>
          <article><div class="feature-number">04</div><h3>Public Verification</h3><p>Allow citizens and businesses to verify an instrument using its UID or permanent QR code without signing in.</p></article>
        </div>
      </section>

      <section class="section process-section">
        <div class="section-heading"><span class="eyebrow">HOW IT WORKS</span><h2>From registration to verification.</h2></div>
        <div class="process-grid">
          <div><b>01</b><span>Register instrument</span></div><div><b>02</b><span>Submit application</span></div><div><b>03</b><span>Assign inspection</span></div><div><b>04</b><span>Record field result</span></div><div><b>05</b><span>Issue certificate</span></div><div><b>06</b><span>Public QR verification</span></div>
        </div>
      </section>

      <section class="section about" id="about">
        <div><span class="eyebrow">ABOUT THE PORTAL</span><h2>Designed for transparent, accountable Legal Metrology operations.</h2></div>
        <p>The platform connects stakeholders, instruments, inspections and certificates through a structured digital record. It is designed as a prototype architecture for government and enterprise workflows, with role-based access and public-safe verification.</p>
      </section>
    </main>
    <footer><div><strong>MAAPAK</strong><span>SIH prototype</span></div><span>Professional digital verification infrastructure</span></footer>
  `;
  bindNavigation(); refreshIcons();
}

export function renderLogin() {
  document.getElementById("app").innerHTML = `
    <div class="auth-page"><div class="auth-panel">
      <a class="brand auth-brand" href="/" data-link><span class="brand-mark">LM</span><span><strong>DIGITAL LEGAL METROLOGY</strong><small>Government portal</small></span></a>
      <div class="auth-copy"><span class="eyebrow">SECURE ACCESS</span><h1>Sign in to the portal</h1><p>Use your registered account to access role-specific services.</p></div>
      <form id="login-form" class="form">
        <label>Username<input name="username" required autocomplete="username"></label>
        <label>Password<input name="password" type="password" required autocomplete="current-password"></label>
        <div id="form-message" class="form-message"></div>
        <button class="btn btn-primary full" type="submit">Sign In ${icon("arrow-right")}</button>
      </form>
      <p class="auth-switch">New owner account? <a href="/register" data-link>Register here</a></p>
    </div></div>
  `;
  bindNavigation(); refreshIcons();
  document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = document.getElementById("form-message");
    message.textContent = "Signing in...";
    try {
      const data = new FormData(e.target);
      const user = await login(data.get("username"), data.get("password"));
      navigate("/portal/dashboard");
    } catch (err) {
      message.textContent = err.message;
      message.className = "form-message error";
    }
  });
}

export function renderRegister() {
  document.getElementById("app").innerHTML = `
    <div class="auth-page"><div class="auth-panel wide">
      <a class="brand auth-brand" href="/" data-link><span class="brand-mark">LM</span><span><strong>DIGITAL LEGAL METROLOGY</strong><small>Owner registration</small></span></a>
      <div class="auth-copy"><span class="eyebrow">OWNER REGISTRATION</span><h1>Create an owner account</h1><p>Owners can register instruments and submit verification applications.</p></div>
      <form id="register-form" class="form form-grid">
        <label>Username<input name="username" required></label>
        <label>Email<input name="email" type="email" required></label>
        <label>First name<input name="first_name" required></label>
        <label>Last name<input name="last_name" required></label>
        <label>Phone number<input name="phone_number"></label>
        <label>Organization name<input name="organization_name"></label>
        <label>Password<input name="password" type="password" minlength="8" required></label>
        <label>Confirm password<input name="password_confirm" type="password" minlength="8" required></label>
        <div id="form-message" class="form-message full"></div>
        <button class="btn btn-primary full" type="submit">Create Owner Account</button>
      </form>
      <p class="auth-switch">Already registered? <a href="/login" data-link>Sign in</a></p>
    </div></div>
  `;
  bindNavigation(); refreshIcons();
  document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = document.getElementById("form-message");
    try {
      const data = Object.fromEntries(new FormData(e.target));
      await register(data);
      message.textContent = "Registration successful. You can now sign in.";
      message.className = "form-message success";
      setTimeout(() => navigate("/login"), 700);
    } catch (err) {
      message.textContent = err.message;
      message.className = "form-message error";
    }
  });
}

async function renderDashboard() {
  let data = {};
  try { data = await api.get("/verification/dashboard/"); } catch (err) {}
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  let cards = "";
  if (user.role === "OWNER") {
    cards = statCard("Total instruments", data.total_instruments, "scale") + statCard("Active certificates", data.active_certificates, "badge-check") + statCard("Expiring certificates", data.expiring_certificates, "calendar-clock") + statCard("Pending applications", data.pending_applications, "clock-3");
  } else if (user.role === "GATC") {
    cards = statCard("Assigned applications", data.assigned_applications, "clipboard-list") + statCard("Pending inspections", data.pending_inspections, "clipboard-check") + statCard("Completed inspections", data.completed_inspections, "check-check") + statCard("Passed inspections", data.passed_inspections, "badge-check");
  } else {
    cards = statCard("Total applications", data.total_applications, "clipboard-list") + statCard("Submitted", data.submitted_applications, "inbox") + statCard("Assigned", data.assigned_applications, "user-check") + statCard("Approved", data.approved_applications, "badge-check") + statCard("Active certificates", data.active_certificates, "file-check-2") + statCard("Expiring", data.expiring_certificates, "calendar-clock");
  }
  const chart = user.role === "OWNER" ? `<div class="panel chart-panel"><div class="panel-heading"><div><span class="eyebrow">APPLICATIONS</span><h3>Status distribution</h3></div></div><canvas id="status-chart"></canvas></div>` : "";
  document.getElementById("app").innerHTML = portalShell(`
    <div class="page-heading"><div><span class="eyebrow">DASHBOARD</span><h1>Operational overview</h1><p>Monitor your Legal Metrology workflow from a single workspace.</p></div></div>
    <div class="stat-grid">${cards}</div>
    ${chart}
  `, "dashboard");
  bindNavigation(); refreshIcons();
  if (user.role === "OWNER" && data.applications_by_status) {
    const counts = {};
    data.applications_by_status.forEach(x => counts[x.status] = (counts[x.status] || 0) + 1);
    new Chart(document.getElementById("status-chart"), { type: "doughnut", data: { labels: Object.keys(counts), datasets: [{ data: Object.values(counts) }] }, options: { responsive: true, plugins: { legend: { position: "bottom" } } }});
  }
}

async function renderInstruments() {
  const instruments = await api.get("/instruments/");
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  document.getElementById("app").innerHTML = portalShell(`
    <div class="page-heading"><div><span class="eyebrow">INSTRUMENT REGISTER</span><h1>My Instruments</h1><p>Permanent instrument identities remain linked across certificate renewals.</p></div>${user.role === "OWNER" ? '<button class="btn btn-primary" id="show-instrument-form">Register instrument</button>' : ""}</div>
    <div id="instrument-form-wrap"></div>
    <div class="panel table-panel"><div class="table-wrap"><table><thead><tr><th>UID</th><th>Instrument</th><th>Manufacturer</th><th>Serial number</th><th>Location</th><th>QR</th></tr></thead><tbody>
    ${instruments.length ? instruments.map(i => `<tr><td><strong>${i.uid}</strong></td><td>${i.name}<small>${i.instrument_type.replaceAll("_"," ")}</small></td><td>${i.manufacturer}</td><td>${i.serial_number}</td><td>${i.location}</td><td>${i.qr_code_url ? `<a class="text-link" href="${i.qr_code_url}" target="_blank">View QR</a>` : "—"}</td></tr>`).join("") : '<tr><td colspan="6" class="empty">No instruments registered yet.</td></tr>'}
    </tbody></table></div></div>
  `, "instruments");
  bindNavigation(); refreshIcons();
  document.getElementById("show-instrument-form")?.addEventListener("click", () => {
    document.getElementById("instrument-form-wrap").innerHTML = `<div class="panel form-panel"><div class="panel-heading"><div><span class="eyebrow">NEW INSTRUMENT</span><h3>Register instrument</h3></div></div>
      <form id="instrument-form" class="form form-grid">
        <label>Instrument name<input name="name" required></label>
        <label>Instrument type<select name="instrument_type" required><option value="WEIGHING_SCALE">Weighing Scale</option><option value="ELECTRONIC_BALANCE">Electronic Balance</option><option value="PLATFORM_SCALE">Platform Scale</option><option value="FUEL_DISPENSER">Fuel Dispenser</option><option value="WATER_METER">Water Meter</option><option value="MEASURING_INSTRUMENT">Measuring Instrument</option><option value="OTHER">Other</option></select></label>
        <label>Manufacturer<input name="manufacturer" required></label><label>Model number<input name="model_number" required></label>
        <label>Serial number<input name="serial_number" required></label><label>Capacity / range<input name="capacity_range"></label>
        <label>Unit of measurement<input name="unit_of_measurement"></label><label>Installation date<input name="installation_date" type="date"></label>
        <label class="full">Location / address<input name="location" required></label>
        <div id="instrument-message" class="form-message full"></div><button class="btn btn-primary" type="submit">Register instrument</button>
      </form></div>`;
    document.getElementById("instrument-form").addEventListener("submit", async (e) => {
      e.preventDefault(); const msg = document.getElementById("instrument-message");
      try { await api.post("/instruments/", Object.fromEntries(new FormData(e.target))); msg.textContent = "Instrument registered and QR code generated."; msg.className="form-message success"; setTimeout(renderInstruments, 600); }
      catch(err){ msg.textContent=err.message; msg.className="form-message error"; }
    });
  });
}

async function renderApplications() {
  const apps = await api.get("/verification/applications/");
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const canCreate = user.role === "OWNER";
  const canManage = user.role === "LMO" || user.role === "ADMIN";
  document.getElementById("app").innerHTML = portalShell(`
    <div class="page-heading"><div><span class="eyebrow">WORKFLOW</span><h1>${user.role === "GATC" ? "Assigned Applications" : "Verification Applications"}</h1><p>Controlled lifecycle from submission through inspection and decision.</p></div>${canCreate ? '<button class="btn btn-primary" id="new-app">New application</button>' : ""}</div>
    <div id="app-form-wrap"></div>
    <div class="panel table-panel"><div class="table-wrap"><table><thead><tr><th>Application</th><th>Instrument</th><th>Type</th><th>Status</th><th>GATC</th><th>Action</th></tr></thead><tbody>
      ${apps.length ? apps.map(a => `<tr><td><strong>${a.application_id}</strong><small>${new Date(a.created_at).toLocaleDateString()}</small></td><td>${a.instrument_uid}<small>${a.instrument_name}</small></td><td>${a.application_type}</td><td><span class="status ${statusClass(a.status)}">${a.status.replaceAll("_"," ")}</span></td><td>${a.assigned_gatc_name || "Not assigned"}</td><td>${canManage && a.status==="SUBMITTED" ? `<button class="table-action assign" data-id="${a.application_id}">Assign</button>` : a.status==="ASSIGNED" && user.role==="GATC" ? `<button class="table-action inspect" data-id="${a.application_id}">Inspect</button>` : canManage && a.status==="INSPECTION_COMPLETED" ? `<button class="table-action decide" data-id="${a.application_id}">Review</button>` : "—"}</td></tr>`).join("") : '<tr><td colspan="6" class="empty">No applications found.</td></tr>'}
    </tbody></table></div></div>
  `, "applications");
  bindNavigation(); refreshIcons();

  document.getElementById("new-app")?.addEventListener("click", async () => {
    const instruments = await api.get("/instruments/");
    document.getElementById("app-form-wrap").innerHTML = `<div class="panel form-panel"><div class="panel-heading"><h3>Submit verification application</h3></div><form id="app-form" class="form form-grid"><label class="full">Instrument<select name="instrument" required>${instruments.map(i=>`<option value="${i.id}">${i.uid} — ${i.name}</option>`).join("")}</select></label><label>Application type<select name="application_type"><option value="INITIAL">Initial Verification</option><option value="REVERIFICATION">Re-verification</option><option value="RENEWAL">Renewal</option></select></label><div id="app-message" class="form-message"></div><button class="btn btn-primary" type="submit">Submit application</button></form></div>`;
    document.getElementById("app-form").addEventListener("submit", async (e)=>{e.preventDefault();const msg=document.getElementById("app-message");try{await api.post("/verification/applications/",Object.fromEntries(new FormData(e.target)));msg.textContent="Application submitted.";msg.className="form-message success";setTimeout(renderApplications,600)}catch(err){msg.textContent=err.message;msg.className="form-message error"}});
  });

  document.querySelectorAll(".assign").forEach(btn=>btn.addEventListener("click", async()=> {
    const gatcs=await api.get("/verification/gatc-users/"); const name=prompt("Enter GATC user ID:\n"+gatcs.map(g=>`${g.id} — ${g.name} (${g.username})`).join("\n"));
    if(name) { try { await api.post(`/verification/applications/${btn.dataset.id}/assign/`,{gatc_id:Number(name)}); renderApplications(); } catch(err){alert(err.message)} }
  }));
  document.querySelectorAll(".inspect").forEach(btn=>btn.addEventListener("click",()=> {
    document.getElementById("app-form-wrap").innerHTML=`<div class="panel form-panel"><div class="panel-heading"><h3>Record inspection</h3></div><form id="inspection-form" class="form form-grid"><label>Inspection date<input type="date" name="inspection_date" required></label><label>Inspection location<input name="inspection_location" required></label><label>Test result<input name="test_result" required></label><label>Result<select name="result"><option value="PASS">Pass</option><option value="FAIL">Fail</option></select></label><label class="full">Measurements / observations<textarea name="measurements" placeholder='{"observed_value": 100, "error": 0.1}'></textarea></label><label class="full">Remarks<textarea name="remarks"></textarea></label><button class="btn btn-primary" type="submit">Complete inspection</button><div id="inspection-message" class="form-message"></div></form></div>`;
    document.getElementById("inspection-form").addEventListener("submit",async(e)=>{e.preventDefault();const d=Object.fromEntries(new FormData(e.target));try{d.measurements=d.measurements?JSON.parse(d.measurements):{};await api.post(`/verification/applications/${btn.dataset.id}/inspection/`,d);renderApplications()}catch(err){document.getElementById("inspection-message").textContent=err.message;document.getElementById("inspection-message").className="form-message error"}});
  }));
  document.querySelectorAll(".decide").forEach(btn=>btn.addEventListener("click",async()=>{const choice=confirm("OK = Approve. Cancel = Reject.");try{if(choice) await api.post(`/verification/applications/${btn.dataset.id}/approve/`,{});else{const reason=prompt("Enter rejection reason:");if(!reason)return;await api.post(`/verification/applications/${btn.dataset.id}/reject/`,{reason})}renderApplications()}catch(err){alert(err.message)}}));
}

async function renderCertificates() {
  const certs = await api.get("/certificates/");
  document.getElementById("app").innerHTML = portalShell(`<div class="page-heading"><div><span class="eyebrow">CERTIFICATE REGISTER</span><h1>Certificates</h1><p>Certificate records remain linked to permanent instrument identities.</p></div></div><div class="panel table-panel"><div class="table-wrap"><table><thead><tr><th>Certificate</th><th>Instrument</th><th>Issue date</th><th>Expiry date</th><th>Status</th></tr></thead><tbody>${certs.length?certs.map(c=>`<tr><td><strong>${c.number}</strong></td><td>${c.instrument_uid}<small>${c.instrument_name}</small></td><td>${c.issue_date}</td><td>${c.expiry_date}</td><td><span class="status ${statusClass(c.status)}">${c.status}</span></td></tr>`).join(""):'<tr><td colspan="5" class="empty">No certificates found.</td></tr>'}</tbody></table></div></div>`,"certificates");
  bindNavigation();refreshIcons();
}

export async function renderPublicVerify(uid = "") {
  document.getElementById("app").innerHTML=`${publicHeader()}<main class="verify-page"><div class="verify-intro"><span class="eyebrow">PUBLIC VERIFICATION</span><h1>Verify a measuring instrument</h1><p>Enter a permanent instrument UID or scan its QR code. No login is required.</p></div><div class="verify-grid"><div class="panel form-panel"><h3>Search by UID</h3><form id="verify-form" class="form"><label>Instrument UID<input id="uid-input" value="${uid}" placeholder="LM-INST-2026-000001" required></label><button class="btn btn-primary" type="submit">Verify instrument</button></form><div class="scanner-box"><div id="qr-reader"></div><button class="btn btn-outline" id="start-scan">Open camera scanner</button></div></div><div id="verify-result"></div></div></main><footer><strong>DIGITAL LEGAL METROLOGY PORTAL</strong><span>Public verification service</span></footer>`;
  bindNavigation();refreshIcons();
  async function verify(value){const result=document.getElementById("verify-result");result.innerHTML=`<div class="panel loading-panel">Checking the instrument record...</div>`;try{const d=await api.get(`/public/verify/${encodeURIComponent(value)}/`);const c=d.current_certificate;result.innerHTML=`<div class="panel verification-result"><div class="result-top"><span class="eyebrow">VERIFICATION RESULT</span><span class="status ${d.verification_status.toLowerCase()}">${d.verification_status}</span></div><h2>${d.instrument.name}</h2><dl class="details"><div><dt>Instrument UID</dt><dd>${d.instrument.uid}</dd></div><div><dt>Type</dt><dd>${d.instrument.instrument_type}</dd></div><div><dt>Manufacturer</dt><dd>${d.instrument.manufacturer}</dd></div><div><dt>Model</dt><dd>${d.instrument.model_number}</dd></div><div><dt>Serial number</dt><dd>${d.instrument.serial_number}</dd></div><div><dt>Location</dt><dd>${d.instrument.location}</dd></div></dl>${c?`<div class="certificate-summary"><span>Current certificate</span><strong>${c.number}</strong><small>Valid from ${c.issue_date} to ${c.expiry_date}</small></div>`:`<div class="alert-box">No currently valid certificate was found for this instrument.</div>`}</div>`}catch(err){result.innerHTML=`<div class="panel error-panel"><h3>Instrument not found</h3><p>${err.message}</p></div>`}}
  if(uid) verify(uid);
  document.getElementById("verify-form").addEventListener("submit",e=>{e.preventDefault();verify(document.getElementById("uid-input").value.trim())});
  document.getElementById("start-scan").addEventListener("click",async()=>{const scanner=new Html5Qrcode("qr-reader");try{await scanner.start({facingMode:"environment"},{fps:10,qrbox:{width:220,height:220}},async(decoded)=>{await scanner.stop();const value=decoded.includes("/public/verify/")?decoded.split("/public/verify/")[1].split(/[?#]/)[0]:decoded;document.getElementById("uid-input").value=value;verify(value)},()=>{});}catch(err){document.getElementById("qr-reader").innerHTML=`<p class="scan-error">Camera access could not be started. Use UID search instead.</p>`}});
}
export { renderDashboard, renderInstruments, renderApplications, renderCertificates };
