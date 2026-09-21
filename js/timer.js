/* ==========================================================================
   EnForme! — timer.js
   Moteur de minuteur générique pour les exercices chronométrés.
   Trois types de configuration (voir data/exercises.json → champ "timer") :
   - "attente"    : maintiens répétés (ex. gainage), avec repos entre chaque,
                    alternance de côté optionnelle.
   - "intervalle" : échauffement + blocs effort/repos (ex. fractionné vélo).
   - "duree"      : simple compte à rebours sans phases (ex. étirements).
   ========================================================================== */

const ExerciseTimer = {
  phases: [],
  phaseIndex: 0,
  secondsLeft: 0,
  running: false,
  intervalHandle: null,
  onTick: null,
  onPhaseChange: null,
  onComplete: null,
  audioCtx: null,

  /** Construit la liste de phases à partir d'une config "timer" d'exercice. */
  buildPhases(cfg) {
    const phases = [];
    if (cfg.type === "attente") {
      for (let i = 0; i < cfg.rounds; i++) {
        const side = cfg.alterne ? (i % 2 === 0 ? "Gauche" : "Droite") : null;
        phases.push({
          kind: "travail",
          seconds: cfg.workSec,
          label: side ? `Maintien — ${side}` : "Maintien",
        });
        if (cfg.restSec && i < cfg.rounds - 1) {
          phases.push({ kind: "repos", seconds: cfg.restSec, label: "Repos" });
        }
      }
    } else if (cfg.type === "intervalle") {
      if (cfg.warmupSec) {
        phases.push({ kind: "echauffement", seconds: cfg.warmupSec, label: "Échauffement" });
      }
      for (let i = 0; i < cfg.rounds; i++) {
        phases.push({ kind: "travail", seconds: cfg.workSec, label: `Effort ${i + 1}/${cfg.rounds}` });
        if (i < cfg.rounds - 1) {
          phases.push({ kind: "repos", seconds: cfg.restSec, label: "Récupération" });
        }
      }
    } else if (cfg.type === "duree") {
      phases.push({ kind: "travail", seconds: cfg.totalSec, label: "En cours" });
    }
    return phases;
  },

  load(cfg, callbacks = {}) {
    this.stop();
    this.phases = this.buildPhases(cfg);
    this.phaseIndex = 0;
    this.secondsLeft = this.phases.length ? this.phases[0].seconds : 0;
    this.onTick = callbacks.onTick || (() => {});
    this.onPhaseChange = callbacks.onPhaseChange || (() => {});
    this.onComplete = callbacks.onComplete || (() => {});
    this.onPhaseChange(this.currentPhase(), this.phaseIndex, this.phases.length);
    this.onTick(this.secondsLeft, this.currentPhase());
  },

  currentPhase() {
    return this.phases[this.phaseIndex] || null;
  },

  start() {
    if (this.running || !this.phases.length) return;
    this.running = true;
    this.intervalHandle = setInterval(() => this.tick(), 1000);
  },

  pause() {
    this.running = false;
    clearInterval(this.intervalHandle);
  },

  reset() {
    this.pause();
    this.phaseIndex = 0;
    this.secondsLeft = this.phases.length ? this.phases[0].seconds : 0;
    this.onPhaseChange(this.currentPhase(), this.phaseIndex, this.phases.length);
    this.onTick(this.secondsLeft, this.currentPhase());
  },

  stop() {
    this.pause();
    this.phases = [];
    this.phaseIndex = 0;
    this.secondsLeft = 0;
  },

  skipPhase() {
    this.advancePhase();
  },

  tick() {
    this.secondsLeft -= 1;
    if (this.secondsLeft <= 3 && this.secondsLeft > 0) {
      this.beep(440);
      this.vibrate(80);
    }
    if (this.secondsLeft <= 0) {
      this.beep(660, 180);
      this.vibrate([80, 40, 80]);
      this.advancePhase();
      return;
    }
    this.onTick(this.secondsLeft, this.currentPhase());
  },

  advancePhase() {
    this.phaseIndex += 1;
    if (this.phaseIndex >= this.phases.length) {
      this.pause();
      this.onComplete();
      return;
    }
    this.secondsLeft = this.phases[this.phaseIndex].seconds;
    this.onPhaseChange(this.currentPhase(), this.phaseIndex, this.phases.length);
    this.onTick(this.secondsLeft, this.currentPhase());
  },

  /** Bip sonore léger via Web Audio (aucun fichier audio requis, fonctionne hors-ligne). */
  beep(freq, durationMs = 100) {
    try {
      if (!this.audioCtx) {
        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      const ctx = this.audioCtx;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.frequency.value = freq;
      osc.type = "sine";
      gain.gain.setValueAtTime(0.15, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + durationMs / 1000);
      osc.connect(gain).connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + durationMs / 1000);
    } catch {
      /* silencieux si l'audio n'est pas disponible (ex. avant interaction utilisateur) */
    }
  },

  vibrate(pattern) {
    if (navigator.vibrate) navigator.vibrate(pattern);
  },

  formatTime(sec) {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${String(s).padStart(2, "0")}`;
  },
};
