(() => {
  "use strict";

  const main = document.querySelector("#vigilApp main");
  if (!main || document.getElementById("vigilUiuxStyles")) return;

  const style = document.createElement("style");
  style.id = "vigilUiuxStyles";
  style.textContent = `
    :root {
      --bg:#f3f7fa;
      --panel:#ffffff;
      --ink:#142b3a;
      --muted:#718493;
      --line:#e1eaf0;
      --blue:#087f83;
      --blue-light:#e6f6f4;
      --teal:#0e9f91;
      --shadow:0 12px 34px rgba(17,48,65,.055);
    }
    body { background:var(--bg); color:var(--ink); }
    .sidebar {
      background:#102b3a;
      border-right:0;
      color:#e8f3f6;
      padding:26px 17px;
      gap:27px;
    }
    .brand h2 { color:#fff; }
    .brand p { color:#9ebbc5; }
    .logo {
      background:linear-gradient(145deg,#16b6a6,#087f83);
      box-shadow:0 7px 20px rgba(14,159,145,.2);
    }
    .nav-label { color:#8caab6; }
    .nav button {
      color:#bfd0d8;
      transition:background .18s ease,color .18s ease,transform .18s ease;
    }
    .nav button:hover { background:#1a3b4a; color:#fff; }
    .nav button.active {
      background:#dff5f1;
      color:#087f83;
      font-weight:700;
    }
    .side-note { background:#193b49; border-color:#2b5260; }
    .side-note strong { color:#fff; }
    .side-note p { color:#b5cbd3; }
    main { padding:30px clamp(16px,3vw,42px) 38px; }
    .topbar { margin-bottom:27px; }
    .eyebrow { color:#087f83; }
    h1 { letter-spacing:-1.1px; }
    .hero {
      background:linear-gradient(115deg,#123b4b,#087f83 72%,#13a995);
      box-shadow:0 16px 36px rgba(8,127,131,.13);
      border-radius:22px;
      padding:30px;
    }
    .card {
      border-color:#e2ebef;
      border-radius:18px;
      box-shadow:0 7px 24px rgba(17,48,65,.035);
      padding:22px;
    }
    .stat-icon { background:#e4f6f3; color:#087f83; }
    .primary {
      background:#087f83;
      border-radius:11px;
      transition:filter .15s ease,transform .15s ease;
    }
    .primary:hover { filter:brightness(.94); }
    .primary:active { transform:translateY(1px); }
    .local-pill { border-radius:12px; }
    .vigil-page { min-width:0; animation:vigilFadeIn .22s ease; }
    .vigil-page[hidden] { display:none !important; }
    .vigil-page-heading { margin:0 0 22px; }
    .vigil-page-heading h2 { margin:0 0 5px; font-size:21px; letter-spacing:-.5px; }
    .vigil-page-heading p { margin:0; color:var(--muted); }
    .vigil-page-grid { display:grid; grid-template-columns:minmax(0,1fr); gap:18px; }
    .vigil-page .card { width:100%; }
    .vigil-page .content-grid { grid-template-columns:minmax(0,1fr); }
    .vigil-form-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:17px; }
    .vigil-field { display:flex; flex-direction:column; gap:7px; min-width:0; }
    .vigil-field label { font-size:12px; font-weight:700; color:#526a79; }
    .vigil-field input,.vigil-field select,.vigil-field textarea {
      width:100%; min-width:0; border:1px solid #dce7ed; border-radius:10px;
      padding:11px 12px; color:#142b3a; background:#fff; font:inherit;
    }
    .vigil-field input:focus,.vigil-field select:focus,.vigil-field textarea:focus {
      outline:3px solid rgba(8,127,131,.12); border-color:#087f83;
    }
    .vigil-field textarea { min-height:86px; resize:vertical; }
    .vigil-form-actions { display:flex; align-items:center; flex-wrap:wrap; gap:12px; margin-top:20px; }
    .vigil-muted { color:var(--muted); font-size:12px; }
    .vigil-settings-row {
      display:flex; align-items:center; justify-content:space-between;
      flex-wrap:wrap; gap:16px; padding:17px 0; border-bottom:1px solid var(--line);
    }
    .vigil-settings-row:last-child { border-bottom:0; }
    .vigil-settings-row strong { display:block; margin-bottom:4px; }
    .vigil-settings-row p { margin:0; color:var(--muted); font-size:12px; }
    #reportHistory { margin-top:0 !important; padding-top:0 !important; border-top:0 !important; }
    .safety { border-radius:14px; }
    @keyframes vigilFadeIn { from { opacity:.65; transform:translateY(3px); } to { opacity:1; transform:translateY(0); } }
    @media(max-width:900px) {
      .sidebar { background:#102b3a; }
      .nav { gap:5px; }
      .nav button { flex-shrink:0; }
    }
    @media(max-width:560px) {
      .vigil-form-grid { grid-template-columns:1fr; }
      .hero { padding:22px; }
      .card { padding:17px; }
      .vigil-page-heading h2 { font-size:19px; }
    }
  `;
  document.head.appendChild(style);

  const nav = main.parentElement.querySelector(".nav");
  if (!nav) return;

  const extraNav = [
    ["history", "◷", "Report History"],
    ["profile", "◎", "My Profile"],
    ["settings", "⚙", "Settings & Security"]
  ];

  for (const [target, icon, label] of extraNav) {
    if (nav.querySelector(`[data-target="${target}"]`)) continue;
    const button = document.createElement("button");
    button.type = "button";
    button.dataset.target = target;
    const glyph = document.createElement("span");
    glyph.className = "ico";
    glyph.setAttribute("aria-hidden", "true");
    glyph.textContent = icon;
    button.append(glyph, document.createTextNode(label));
    nav.appendChild(button);
  }

  const topbar = main.querySelector(".topbar");
  const hero = main.querySelector(".hero");
  const stats = main.querySelector(".stats");
  const sectionTitles = [...main.querySelectorAll(":scope > .section-title")];
  const contentGrid = main.querySelector(".content-grid");
  const assistant = document.getElementById("assistant");
  const reports = document.getElementById("reports");
  const reportHistory = document.getElementById("reportHistory");

  if (!topbar || !hero || !stats || !contentGrid || !assistant || !reports) {
    console.error("Vigil UI upgrade stopped: expected dashboard elements were not found.");
    return;
  }

  function makePage(id, title, description) {
    const page = document.createElement("section");
    page.className = "vigil-page";
    page.id = id;
    page.dataset.pageTitle = title;
    page.dataset.pageDescription = description;
    page.setAttribute("aria-label", title);
    const heading = document.createElement("div");
    heading.className = "vigil-page-heading";
    const h2 = document.createElement("h2");
    h2.textContent = title;
    const p = document.createElement("p");
    p.textContent = description;
    heading.append(h2, p);
    page.appendChild(heading);
    return page;
  }

  const overviewPage = document.createElement("section");
  overviewPage.className = "vigil-page";
  overviewPage.id = "overview";
  overviewPage.dataset.pageTitle = "Health Overview";
  overviewPage.dataset.pageDescription = "Understand health information with a little more clarity.";

  const assistantPage = makePage(
    "assistantPage", "AI Health Assistant",
    "Ask health questions and explore medical information."
  );
  const reportsPage = makePage(
    "reportsPage", "Medical Reports",
    "Upload a report and review the extracted information."
  );
  const historyPage = makePage(
    "historyPage", "Report History",
    "Review your saved report activity."
  );
  const profilePage = makePage(
    "profilePage", "My Profile",
    "Manage your personal details and patient health information."
  );
  const settingsPage = makePage(
    "settingsPage", "Settings & Security",
    "Manage your account and review privacy guidance."
  );

  main.insertBefore(overviewPage, hero);
  overviewPage.append(hero);
  if (sectionTitles[0]) overviewPage.append(sectionTitles[0]);
  overviewPage.append(stats);

  assistantPage.appendChild(assistant);
  reportsPage.appendChild(reports);

  contentGrid.remove();
  if (sectionTitles[1]) sectionTitles[1].remove();

  if (reportHistory) {
    const historyCard = document.createElement("article");
    historyCard.className = "card";
    historyCard.appendChild(reportHistory);
    historyPage.appendChild(historyCard);
  } else {
    const message = document.createElement("p");
    message.className = "vigil-muted";
    message.textContent = "Report history is not available in the current markup.";
    historyPage.appendChild(message);
  }

  const profileCard = document.createElement("article");
  profileCard.className = "card";
  profileCard.innerHTML = `
  
<div class="vigil-patient-id" style="margin-bottom: 20px; padding: 14px; border: 1px solid #d8e2ee; border-radius: 10px;">
  <div style="font-size: 13px; color: #64748b;">Vigil Patient ID</div>
  <strong id="vigilPatientId" style="display: block; margin-top: 5px;">Loading…</strong>
  <div style="font-size: 12px; color: #64748b; margin-top: 5px;">Your account-linked reference ID</div>
</div>
   
    <form id="vigilProfileForm">
      <div class="vigil-form-grid">
        <div class="vigil-field">
          <label for="vigilProfileName">Full name</label>
          <input id="vigilProfileName" name="full_name" maxlength="120" autocomplete="name">
        </div>
        <div class="vigil-field">
          <label for="vigilProfileDob">Date of birth</label>
          <input id="vigilProfileDob" name="date_of_birth" type="date">
        </div>
        <div class="vigil-field">
          <label for="vigilProfileSex">Sex</label>
          <select id="vigilProfileSex" name="sex">
            <option value="">Not specified</option>
            <option>Female</option><option>Male</option>
            <option>Other</option><option>Prefer not to say</option>
          </select>
        </div>
        <div class="vigil-field">
          <label for="vigilProfileBlood">Blood group</label>
          <select id="vigilProfileBlood" name="blood_group">
            <option value="">Not specified</option>
            <option>A+</option><option>A-</option><option>B+</option><option>B-</option>
            <option>AB+</option><option>AB-</option><option>O+</option><option>O-</option>
          </select>
        </div>
        <div class="vigil-field">
          <label for="vigilProfileHeight">Height (cm)</label>
          <input id="vigilProfileHeight" name="height_cm" type="number" min="30" max="300" step="0.1">
        </div>
        <div class="vigil-field">
          <label for="vigilProfileWeight">Weight (kg)</label>
          <input id="vigilProfileWeight" name="weight_kg" type="number" min="1" max="700" step="0.1">
        </div>
        <div class="vigil-field">
          <label for="vigilProfileAllergies">Allergies</label>
          <textarea id="vigilProfileAllergies" name="allergies" maxlength="2000"></textarea>
        </div>
        <div class="vigil-field">
          <label for="vigilProfileConditions">Existing conditions</label>
          <textarea id="vigilProfileConditions" name="existing_conditions" maxlength="2000"></textarea>
        </div>
        <div class="vigil-field">
          <label for="vigilProfileMeds">Current medications</label>
          <textarea id="vigilProfileMeds" name="current_medications" maxlength="2000"></textarea>
        </div>
      </div>
      <div class="vigil-form-actions">
        <button class="primary" type="submit" id="vigilProfileSave">Save profile</button>
        <span class="vigil-muted" id="vigilProfileStatus" role="status" aria-live="polite">Sign in to load or save your profile.</span>
      </div>
    </form>`;
  profilePage.appendChild(profileCard);

  const settingsCard = document.createElement("article");
  settingsCard.className = "card";
  settingsCard.innerHTML = `
    <div class="vigil-settings-row">
      <div><strong>Account session</strong><p>Sign out using the account controls at the top of the dashboard.</p></div>
      <span class="vigil-muted">Supabase authentication</span>
    </div>
    <div class="vigil-settings-row">
      <div><strong>Health information privacy</strong><p>Use only information you are comfortable storing in this prototype.</p></div>
      <span class="vigil-muted">Privacy guidance</span>
    </div>
    <div class="vigil-settings-row">
      <div><strong>Medical safety</strong><p>Vigil provides informational assistance and does not replace a qualified clinician.</p></div>
      <span class="vigil-muted">Always verify important advice</span>
    </div>
    <p class="vigil-muted">Notification and password-management options will be added only when their backend support is verified.</p>`;
  settingsPage.appendChild(settingsCard);

  main.insertBefore(assistantPage, main.querySelector(".safety"));
  main.insertBefore(reportsPage, main.querySelector(".safety"));
  main.insertBefore(historyPage, main.querySelector(".safety"));
  main.insertBefore(profilePage, main.querySelector(".safety"));
  main.insertBefore(settingsPage, main.querySelector(".safety"));

  const pages = {
    overview: overviewPage,
    assistant: assistantPage,
    reports: reportsPage,
    history: historyPage,
    profile: profilePage,
    settings: settingsPage
  };

  const heading = topbar.querySelector("h1");
  const subtitle = topbar.querySelector(".subtitle");
  let profileLoaded = false;

  function setStatus(message) {
    const el = document.getElementById("vigilProfileStatus");
    if (el) el.textContent = message;
  }

  function setPatientId(userId) {
    const el = document.getElementById("vigilPatientId");
    if (!el) return;

    if (!userId || typeof userId !== "string") {
      el.textContent = "Unavailable";
      return;
    }

    const compactId = userId.replace(/-/g, "").toUpperCase();
    el.textContent = "VIG-" + compactId.slice(0, 12);
  }

  function fillProfile(profile) {
    const fields = {
      full_name: "vigilProfileName",
      date_of_birth: "vigilProfileDob",
      sex: "vigilProfileSex",
      blood_group: "vigilProfileBlood",
      height_cm: "vigilProfileHeight",
      weight_kg: "vigilProfileWeight",
      allergies: "vigilProfileAllergies",
      existing_conditions: "vigilProfileConditions",
      current_medications: "vigilProfileMeds"
    };
    for (const [key, id] of Object.entries(fields)) {
      const el = document.getElementById(id);
      if (el) el.value = profile && profile[key] != null ? profile[key] : "";
    }
  }

  async function loadProfile() {
    if (typeof vigilSupabase === "undefined" || !vigilSupabase) {
      setStatus("Authentication is not ready. Please sign in again.");
      return;
    }
    try {
      const { data, error } = await vigilSupabase.auth.getSession();
      if (error || !data.session) {
        setStatus("Sign in to load your profile.");
        return;
      }
      const response = await fetch("/profile", {
        headers: { Authorization: "Bearer " + data.session.access_token }
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Could not load profile.");
      const profile = payload.profile || payload.patient_profile || payload;
      setPatientId(payload.account?.user_id || data.session.user.id);
      if (profile && typeof profile === "object") fillProfile(profile);
      profileLoaded = true;
      setStatus("Profile loaded. Review your details and save any changes.");
    } catch (error) {
      setStatus(error.message || "Could not load profile.");
    }
  }

  async function saveProfile(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const button = document.getElementById("vigilProfileSave");
    if (typeof vigilSupabase === "undefined" || !vigilSupabase) {
      setStatus("Authentication is not ready. Please sign in again.");
      return;
    }
    const { data, error } = await vigilSupabase.auth.getSession();
    if (error || !data.session) {
      setStatus("Sign in before saving your profile.");
      return;
    }

    const value = name => form.elements.namedItem(name).value;
    const numberOrNull = name => value(name).trim() === "" ? null : Number(value(name));
    const body = {
      full_name: value("full_name").trim(),
      date_of_birth: value("date_of_birth") || null,
      sex: value("sex"),
      height_cm: numberOrNull("height_cm"),
      weight_kg: numberOrNull("weight_kg"),
      blood_group: value("blood_group"),
      allergies: value("allergies").trim(),
      existing_conditions: value("existing_conditions").trim(),
      current_medications: value("current_medications").trim()
    };

    button.disabled = true;
    setStatus("Saving your profile…");
    try {
      const response = await fetch("/profile", {
        method: "POST",
        headers: {
          Authorization: "Bearer " + data.session.access_token,
          "Content-Type": "application/json",
          Accept: "application/json"
        },
        body: JSON.stringify(body)
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Could not save profile.");
      fillProfile(payload.profile || body);
      setPatientId(data.session.user.id);
      profileLoaded = true;
      setStatus("Profile saved successfully.");
    } catch (error) {
      setStatus(error.message || "Could not save profile.");
    } finally {
      button.disabled = false;
    }
  }

  document.getElementById("vigilProfileForm").addEventListener("submit", saveProfile);

  function showPage(target) {
    const page = pages[target] || overviewPage;
    for (const [key, element] of Object.entries(pages)) {
      element.hidden = element !== page;
      if (element === page) element.removeAttribute("aria-hidden");
      else element.setAttribute("aria-hidden", "true");
    }
    nav.querySelectorAll("button[data-target]").forEach(button => {
      const active = button.dataset.target === target;
      button.classList.toggle("active", active);
      button.setAttribute("aria-current", active ? "page" : "false");
    });
    if (heading) heading.textContent = page.dataset.pageTitle || "Vigil Healthcare AI";
    if (subtitle) subtitle.textContent = page.dataset.pageDescription || "";
    if (target === "profile" && !profileLoaded) void loadProfile();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  nav.querySelectorAll("button[data-target]").forEach(button => {
    button.addEventListener("click", event => {
      event.preventDefault();
      showPage(button.dataset.target);
    });
  });

  window.vigilRefreshOverviewStats = async function () {
    const overview = document.getElementById("overview");
    if (!overview) return;

    const reportValue = overview.querySelector(".stats .card:nth-child(2) .stat-value");
    const reportHelp = overview.querySelector(".stats .card:nth-child(2) .stat-help");

    if (!reportValue || !reportHelp) return;

    let activity = document.getElementById("vigilRecentActivity");

    if (!activity) {
      activity = document.createElement("section");
      activity.id = "vigilRecentActivity";
      activity.className = "card";
      activity.style.marginTop = "18px";

      const heading = document.createElement("h2");
      heading.className = "panel-title";
      heading.textContent = "Recent report activity";

      const description = document.createElement("p");
      description.className = "panel-subtitle";
      description.textContent = "Your latest saved medical reports.";

      const status = document.createElement("p");
      status.id = "vigilRecentActivityStatus";
      status.className = "vigil-muted";
      status.textContent = "Loading saved reports...";

      const list = document.createElement("div");
      list.id = "vigilRecentActivityList";

      activity.append(heading, description, status, list);
      overview.querySelector(".stats").insertAdjacentElement("afterend", activity);
    }

    const status = document.getElementById("vigilRecentActivityStatus");
    const list = document.getElementById("vigilRecentActivityList");

    reportValue.textContent = "Loading...";
    reportHelp.textContent = "Checking your saved reports...";
    status.textContent = "Loading saved reports...";
    list.replaceChildren();

    try {
      if (typeof vigilAuthorizationHeaders !== "function") {
        throw new Error("Authentication helper is unavailable.");
      }

      const response = await fetch("/reports", {
        method: "GET",
        headers: await vigilAuthorizationHeaders()
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.error || "Could not load reports.");
      }

      const reports = Array.isArray(data.reports) ? data.reports : [];

      reportValue.textContent = reports.length + " saved";

      if (reports.length === 0) {
        reportHelp.textContent = "Upload a PDF to get started.";
        status.textContent = "No saved reports yet.";
        return;
      }

      const latest = reports[0];
      const latestName = latest.filename ||
        latest.file_name ||
        latest.original_filename ||
        "Medical report";

      reportHelp.textContent = "Latest: " + latestName;

      status.textContent =
        "Showing " + Math.min(reports.length, 3) +
        " of " + reports.length + " saved reports.";

      reports.slice(0, 3).forEach(function (report) {
        const item = document.createElement("article");
        item.style.padding = "12px 0";
        item.style.borderTop = "1px solid var(--border, #e5e7eb)";

        const name = document.createElement("strong");
        name.textContent = report.filename ||
          report.file_name ||
          report.original_filename ||
          "Medical report";

        const details = document.createElement("p");
        details.className = "vigil-muted";

        const uploaded = report.uploaded_at
          ? new Date(report.uploaded_at).toLocaleString()
          : "Date unavailable";

        details.textContent =
          "Uploaded: " + uploaded +
          " | Status: " + String(report.status || "Saved");

        item.append(name, details);
        list.appendChild(item);
      });
    } catch (error) {
      reportValue.textContent = "Unavailable";
      reportHelp.textContent = "Check your sign-in and reports API.";
      status.textContent = "Could not load reports: " + error.message;
    }
  };

  window.addEventListener("load", function () {
    void window.vigilRefreshOverviewStats();
  }, { once: true });
  showPage("overview");
  console.info("Vigil UI/UX navigation enhancement loaded.");
})();
