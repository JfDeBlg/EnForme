/* ==========================================================================
   EnForme! — app.js
   Application principale : menu, navigation entre écrans, déroulé de séance.
   Aucune dépendance externe (V0). Données statiques chargées depuis /data.
   ========================================================================== */

const OBJECTIF_LABELS = {
  golf: "Puissance golf",
  souplesse: "Souplesse",
  force: "Force musculaire",
  voile: "Voile légère",
  kite: "Kitesurf",
  ski: "Ski",
  endurance: "Endurance",
};

const MATERIEL_LABELS = {
  tapis: "Tapis de sol",
  elastique: "Élastique",
  halteres: "Haltères 1 kg (x2)",
  velo: "Vélo elliptique",
};

const App = {
  exercisesById: {},
  programmes: [],
  profile: null,

  async init() {
    this.profile = Store.getProfile();
    await this.loadData();
    this.bindMenu();
    this.bindNav();
    this.renderReglages();
    this.renderNouvelEntrainement();
    this.renderReprendre();
    this.renderHistorique();
    this.renderStatistiques();
    this.goTo("accueil");
    this.registerServiceWorker();
  },

  async loadData() {
    const [exRes, progRes] = await Promise.all([
      fetch("data/exercises.json"),
      fetch("data/programmes.json"),
    ]);
    const exData = await exRes.json();
    const progData = await progRes.json();
    exData.exercises.forEach((ex) => (this.exercisesById[ex.id] = ex));
    this.programmes = progData.programmes;
  },

  registerServiceWorker() {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("sw.js").catch(() => {
        /* silencieux : l'app fonctionne aussi sans SW (juste sans offline complet) */
      });
    }
  },

  /* ---------------- Navigation ---------------- */

  bindMenu() {
    const burger = document.getElementById("burger");
    const overlay = document.getElementById("menu-overlay");
    const panel = document.getElementById("menu-panel");

    const open = () => {
      burger.setAttribute("aria-expanded", "true");
      overlay.classList.add("is-open");
      panel.classList.add("is-open");
    };
    const close = () => {
      burger.setAttribute("aria-expanded", "false");
      overlay.classList.remove("is-open");
      panel.classList.remove("is-open");
    };

    burger.addEventListener("click", () => {
      const isOpen = panel.classList.contains("is-open");
      isOpen ? close() : open();
    });
    overlay.addEventListener("click", close);

    document.querySelectorAll("[data-nav]").forEach((btn) => {
      btn.addEventListener("click", () => {
        close();
        this.goTo(btn.dataset.nav);
      });
    });
  },

  bindNav() {
    document.querySelectorAll("[data-goto]").forEach((btn) => {
      btn.addEventListener("click", () => this.goTo(btn.dataset.goto));
    });
  },

  goTo(viewId) {
    document.querySelectorAll(".view").forEach((v) => v.classList.remove("is-active"));
    const target = document.getElementById(`view-${viewId}`);
    if (target) target.classList.add("is-active");
    window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
    if (viewId === "reprendre") this.renderReprendre();
    if (viewId === "historique") this.renderHistorique();
    if (viewId === "statistiques") this.renderStatistiques();
  },

  toast(msg) {
    const el = document.getElementById("toast");
    el.textContent = msg;
    el.classList.add("is-visible");
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => el.classList.remove("is-visible"), 2400);
  },

  /* ---------------- Réglages ---------------- */

  renderReglages() {
    const p = this.profile;
    document.getElementById("f-age").value = p.age ?? "";
    document.getElementById("f-sexe").value = p.sexe ?? "";
    document.getElementById("f-niveau").value = p.niveauForme ?? "intermediaire";
    document.getElementById("f-blessures").value = p.blessures ?? "";
    document.getElementById("f-frequence").value = p.frequenceHebdo ?? 3;

    document.querySelectorAll("[data-materiel]").forEach((cb) => {
      cb.checked = p.materielDispo.includes(cb.dataset.materiel);
    });

    Object.keys(OBJECTIF_LABELS)
      .filter((k) => k !== "endurance")
      .forEach((key) => {
        const input = document.getElementById(`obj-${key}`);
        const out = document.getElementById(`obj-${key}-val`);
        if (!input) return;
        input.value = p.objectifs[key] ?? 0;
        out.textContent = `${input.value}%`;
        input.oninput = () => (out.textContent = `${input.value}%`);
      });

    document.getElementById("form-reglages").onsubmit = (e) => {
      e.preventDefault();
      this.saveReglagesFromForm();
    };
    document.getElementById("btn-export").onclick = () => this.exportData();
    document.getElementById("input-import").onchange = (e) => this.importData(e);
    document.getElementById("btn-reset").onclick = () => this.wipeData();
  },

  saveReglagesFromForm() {
    const materiel = Array.from(document.querySelectorAll("[data-materiel]:checked")).map(
      (cb) => cb.dataset.materiel
    );
    const objectifs = {};
    Object.keys(OBJECTIF_LABELS)
      .filter((k) => k !== "endurance")
      .forEach((key) => {
        const input = document.getElementById(`obj-${key}`);
        if (input) objectifs[key] = Number(input.value);
      });

    this.profile = {
      age: document.getElementById("f-age").value ? Number(document.getElementById("f-age").value) : null,
      sexe: document.getElementById("f-sexe").value,
      niveauForme: document.getElementById("f-niveau").value,
      blessures: document.getElementById("f-blessures").value,
      frequenceHebdo: Number(document.getElementById("f-frequence").value) || 3,
      materielDispo: materiel,
      objectifs,
    };
    Store.saveProfile(this.profile);
    this.toast("Profil enregistré");
    this.renderNouvelEntrainement();
  },

  exportData() {
    const data = Store.exportAll();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    const date = new Date().toISOString().slice(0, 10);
    a.href = url;
    a.download = `enforme-export-${date}.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    this.toast("Export téléchargé");
  },

  importData(evt) {
    const file = evt.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const data = JSON.parse(reader.result);
        const ok = confirm(
          "Importer ce fichier remplacera votre profil et votre historique actuels. Continuer ?"
        );
        if (!ok) return;
        Store.importAll(data);
        this.profile = Store.getProfile();
        this.renderReglages();
        this.renderHistorique();
        this.renderStatistiques();
        this.renderReprendre();
        this.toast("Import terminé");
      } catch (err) {
        alert("Fichier illisible : " + err.message);
      }
      evt.target.value = "";
    };
    reader.readAsText(file);
  },

  wipeData() {
    const ok = confirm("Effacer toutes les données locales (profil, historique) ? Cette action est irréversible.");
    if (!ok) return;
    Store.wipeAll();
    this.profile = Store.getProfile();
    this.renderReglages();
    this.renderHistorique();
    this.renderStatistiques();
    this.renderReprendre();
    this.toast("Données effacées");
  },

  /* ---------------- Nouvel entraînement ---------------- */

  renderNouvelEntrainement() {
    const wrap = document.getElementById("programmes-list");
    wrap.innerHTML = "";
    this.programmes.forEach((prog) => {
      const card = document.createElement("button");
      card.className = "action-btn";
      card.style.marginBottom = "10px";
      card.style.width = "100%";
      const label = OBJECTIF_LABELS[prog.objectifPrincipal] || prog.objectifPrincipal;
      card.innerHTML = `<strong>${prog.nom}</strong><span>${label} · ${prog.dureeMin} min · ${prog.exercices.length} exercices</span>`;
      card.addEventListener("click", () => this.startSession(prog));
      wrap.appendChild(card);
    });
  },

  startSession(programme) {
    const session = {
      programmeId: programme.id,
      programmeNom: programme.nom,
      startedAt: new Date().toISOString(),
      exerciceIndex: 0,
      exercices: programme.exercices,
    };
    Store.saveOngoingSession(session);
    this.runSession(session);
  },

  runSession(session) {
    this.currentSession = session;
    this.renderSeanceStep();
    this.goTo("seance");
  },

  renderSeanceStep() {
    const session = this.currentSession;
    const total = session.exercices.length;
    const idx = session.exerciceIndex;
    const exId = session.exercices[idx];
    const ex = this.exercisesById[exId];

    document.getElementById("seance-titre").textContent = session.programmeNom;
    document.getElementById("seance-progress").textContent = `Exercice ${idx + 1} / ${total}`;

    const materiel = ex.materiel.map((m) => MATERIEL_LABELS[m] || m).join(", ");
    const consignes = ex.consignes.map((c) => `<li>${c}</li>`).join("");
    const videoUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(ex.videoQuery)}`;

    document.getElementById("seance-content").innerHTML = `
      <div class="card card--flame">
        <h2>${ex.nom}</h2>
        <p>${ex.description}</p>
        <ul>${consignes}</ul>
        <p><strong>Format :</strong> ${ex.series}</p>
        <p><strong>Matériel :</strong> ${materiel || "aucun"}</p>
        <a class="btn btn--ghost" href="${videoUrl}" target="_blank" rel="noopener">▶ Voir une démonstration vidéo</a>
      </div>
    `;

    const btnNext = document.getElementById("btn-seance-next");
    btnNext.textContent = idx + 1 < total ? "Exercice suivant" : "Terminer la séance";
  },

  bindSeance() {
    document.getElementById("btn-seance-next").addEventListener("click", () => {
      const session = this.currentSession;
      if (session.exerciceIndex + 1 < session.exercices.length) {
        session.exerciceIndex += 1;
        Store.saveOngoingSession(session);
        this.renderSeanceStep();
      } else {
        this.finishSession();
      }
    });
    document.getElementById("btn-seance-quitter").addEventListener("click", () => {
      const ok = confirm("Quitter la séance ? Votre progression est sauvegardée, vous pourrez reprendre plus tard.");
      if (ok) this.goTo("accueil");
    });
  },

  finishSession() {
    const ressenti = prompt("Ressenti de la séance ? (1 = difficile, 5 = facile)", "3");
    const session = this.currentSession;
    Store.addHistoryEntry({
      date: new Date().toISOString(),
      programmeId: session.programmeId,
      programmeNom: session.programmeNom,
      nbExercices: session.exercices.length,
      ressenti: ressenti ? Number(ressenti) : null,
    });
    Store.clearOngoingSession();
    this.toast("Séance enregistrée — bravo !");
    this.renderHistorique();
    this.renderStatistiques();
    this.renderReprendre();
    this.goTo("accueil");
  },

  /* ---------------- Reprendre ---------------- */

  renderReprendre() {
    const wrap = document.getElementById("reprendre-content");
    const ongoing = Store.getOngoingSession();
    if (!ongoing) {
      wrap.innerHTML = `<div class="empty-state"><span class="ico">🌤️</span>Aucune séance en cours. Lancez un nouvel entraînement quand vous êtes prêt.</div>`;
      return;
    }
    const total = ongoing.exercices.length;
    wrap.innerHTML = `
      <div class="card">
        <h3>${ongoing.programmeNom}</h3>
        <p>Arrêtée à l'exercice ${ongoing.exerciceIndex + 1} / ${total}</p>
        <button class="btn btn--primary btn--block" id="btn-resume">Reprendre la séance</button>
      </div>
    `;
    document.getElementById("btn-resume").addEventListener("click", () => this.runSession(ongoing));
  },

  /* ---------------- Historique ---------------- */

  renderHistorique() {
    const wrap = document.getElementById("historique-content");
    const history = Store.getHistory();
    if (history.length === 0) {
      wrap.innerHTML = `<div class="empty-state"><span class="ico">📋</span>Aucune séance enregistrée pour l'instant.</div>`;
      return;
    }
    wrap.innerHTML = history
      .map((h) => {
        const d = new Date(h.date);
        const dateStr = d.toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" });
        return `<div class="card card--muted">
          <div class="section-title" style="margin:0 0 6px;">
            <strong>${h.programmeNom}</strong>
            <span style="color:var(--text-muted); font-size:0.85rem;">${dateStr}</span>
          </div>
          <p style="margin:0;">${h.nbExercices} exercices${h.ressenti ? ` · ressenti ${h.ressenti}/5` : ""}</p>
        </div>`;
      })
      .join("");
  },

  /* ---------------- Statistiques ---------------- */

  renderStatistiques() {
    const wrap = document.getElementById("stats-content");
    const history = Store.getHistory();
    if (history.length === 0) {
      wrap.innerHTML = `<div class="empty-state"><span class="ico">📊</span>Vos statistiques apparaîtront après votre première séance.</div>`;
      return;
    }
    const now = Date.now();
    const sevenDays = history.filter((h) => now - new Date(h.date).getTime() < 7 * 86400000).length;

    const counts = {};
    history.forEach((h) => {
      const prog = this.programmes.find((p) => p.id === h.programmeId);
      const key = prog ? prog.objectifPrincipal : "autre";
      counts[key] = (counts[key] || 0) + 1;
    });
    const max = Math.max(...Object.values(counts));

    const bars = Object.entries(counts)
      .map(([key, n]) => {
        const pct = Math.round((n / max) * 100);
        const label = OBJECTIF_LABELS[key] || key;
        return `<div class="range-item">
          <div class="range-head"><span>${label}</span><b>${n}</b></div>
          <div style="background:var(--surface-raised); border-radius:6px; height:10px; overflow:hidden;">
            <div style="width:${pct}%; background:var(--flame); height:100%;"></div>
          </div>
        </div>`;
      })
      .join("");

    wrap.innerHTML = `
      <div class="card-grid">
        <div class="card"><h3>Total</h3><h2>${history.length}</h2><p>séances enregistrées</p></div>
        <div class="card"><h3>7 derniers jours</h3><h2>${sevenDays}</h2><p>séances</p></div>
      </div>
      <div class="section-title"><h3>Répartition par objectif</h3></div>
      ${bars}
    `;
  },
};

document.addEventListener("DOMContentLoaded", () => {
  App.init();
  App.bindSeance();
});
