/* StaffPilot public website — small progressive-enhancement script.
   No external dependencies. Forms validate client-side and store
   submissions locally (localStorage) until the API exists (Phase 15). */
(function () {
  "use strict";

  /* Mobile nav toggle */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  var cta = document.querySelector(".header-cta");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      if (cta) cta.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* Footer year */
  var year = document.getElementById("footer-year");
  if (year) year.textContent = String(new Date().getFullYear());

  /* Pricing calculator (pricing page) */
  var workersInput = document.getElementById("calc-workers");
  if (workersInput) {
    var out = {
      starter: document.getElementById("calc-starter"),
      growth: document.getElementById("calc-growth"),
      scale: document.getElementById("calc-scale"),
      count: document.getElementById("calc-count")
    };
    var fmt = function (n) { return "$" + n.toLocaleString("en-US"); };
    var update = function () {
      var w = Math.max(1, Math.min(500, parseInt(workersInput.value, 10) || 45));
      if (out.count) out.count.textContent = String(w);
      if (out.starter) out.starter.textContent = fmt(49 + 4 * w) + "/mo";
      if (out.growth) out.growth.textContent = fmt(99 + 6 * w) + "/mo";
      if (out.scale) out.scale.textContent = fmt(199 + 8 * w) + "/mo";
    };
    workersInput.addEventListener("input", update);
    update();
  }

  /* Generic client-side form handling: validate, show errors, show
     on-screen confirmation, store locally. Never pretends to submit
     to a backend. */
  function setupForm(formId, confirmId, summaryId, storageKey) {
    var form = document.getElementById(formId);
    if (!form) return;
    var confirm = document.getElementById(confirmId);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var valid = true;
      var firstBad = null;
      var required = form.querySelectorAll("[data-required]");
      required.forEach(function (field) {
        var err = document.getElementById(field.id + "-error");
        var value = (field.value || "").trim();
        var bad = false;
        if (!value) bad = true;
        if (field.type === "email" && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) bad = true;
        if (field.id === "demo-workers" && value && (isNaN(Number(value)) || Number(value) < 1)) bad = true;
        field.setAttribute("aria-invalid", bad ? "true" : "false");
        if (err) err.classList.toggle("visible", bad);
        if (bad) { valid = false; if (!firstBad) firstBad = field; }
      });
      if (!valid) { if (firstBad) firstBad.focus(); return; }
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = String(v); });
      data.submittedAt = new Date().toISOString();
      try {
        var existing = JSON.parse(localStorage.getItem(storageKey) || "[]");
        existing.push(data);
        localStorage.setItem(storageKey, JSON.stringify(existing));
      } catch (err) { /* local storage unavailable; confirmation still shows */ }
      if (summaryId) {
        var summary = document.getElementById(summaryId);
        if (summary) {
          var name = data.name || data["full-name"] || "";
          summary.textContent = name
            ? "Thanks, " + name + ". Your request was recorded locally in this browser."
            : "Thanks. Your request was recorded locally in this browser.";
        }
      }
      if (confirm) { confirm.classList.add("visible"); confirm.setAttribute("tabindex", "-1"); confirm.focus(); }
      form.reset();
    });
  }

  setupForm("demo-form", "demo-confirmation", "demo-summary", "staffpilot-demo-requests");
  setupForm("contact-form", "contact-confirmation", "contact-summary", "staffpilot-contact-messages");
})();
