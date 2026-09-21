/* ==========================================================================
   EnForme! — storage.js
   Couche de persistance locale (localStorage). Pas de serveur : toutes les
   données restent sur l'appareil. L'export/import JSON sert de sauvegarde
   et de portabilité entre appareils.
   ========================================================================== */

const STORAGE_KEYS = {
  profile: "enforme:profile",
  history: "enforme:history",
  ongoing: "enforme:ongoing-session",
};

const DEFAULT_PROFILE = {
  age: null,
  sexe: "",
  niveauForme: "intermediaire",
  blessures: "",
  frequenceHebdo: 3,
  materielDispo: ["tapis", "elastique", "halteres", "velo"],
  objectifs: {
    golf: 70,
    souplesse: 45,
    force: 40,
    voile: 20,
    kite: 15,
    ski: 15,
  },
};

const Store = {
  getProfile() {
    const raw = localStorage.getItem(STORAGE_KEYS.profile);
    if (!raw) return { ...DEFAULT_PROFILE };
    try {
      return { ...DEFAULT_PROFILE, ...JSON.parse(raw) };
    } catch {
      return { ...DEFAULT_PROFILE };
    }
  },

  saveProfile(profile) {
    localStorage.setItem(STORAGE_KEYS.profile, JSON.stringify(profile));
  },

  getHistory() {
    const raw = localStorage.getItem(STORAGE_KEYS.history);
    if (!raw) return [];
    try {
      return JSON.parse(raw);
    } catch {
      return [];
    }
  },

  addHistoryEntry(entry) {
    const history = Store.getHistory();
    history.unshift(entry);
    localStorage.setItem(STORAGE_KEYS.history, JSON.stringify(history));
  },

  clearHistory() {
    localStorage.removeItem(STORAGE_KEYS.history);
  },

  getOngoingSession() {
    const raw = localStorage.getItem(STORAGE_KEYS.ongoing);
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  },

  saveOngoingSession(session) {
    localStorage.setItem(STORAGE_KEYS.ongoing, JSON.stringify(session));
  },

  clearOngoingSession() {
    localStorage.removeItem(STORAGE_KEYS.ongoing);
  },

  /** Regroupe tout l'état applicatif pour export. */
  exportAll() {
    return {
      exportedAt: new Date().toISOString(),
      app: "EnForme!",
      schemaVersion: 1,
      profile: Store.getProfile(),
      history: Store.getHistory(),
      ongoingSession: Store.getOngoingSession(),
    };
  },

  /** Remplace l'état applicatif à partir d'un export JSON validé. */
  importAll(data) {
    if (!data || typeof data !== "object") {
      throw new Error("Fichier invalide : structure JSON inattendue.");
    }
    if (data.profile) Store.saveProfile(data.profile);
    if (Array.isArray(data.history)) {
      localStorage.setItem(STORAGE_KEYS.history, JSON.stringify(data.history));
    }
    if (data.ongoingSession) {
      Store.saveOngoingSession(data.ongoingSession);
    } else {
      Store.clearOngoingSession();
    }
  },

  wipeAll() {
    Object.values(STORAGE_KEYS).forEach((k) => localStorage.removeItem(k));
  },
};
