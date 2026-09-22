import json, math

GOLD = "#F6B93B"
FLAME = "#F2622E"
CREAM = "#FBF4EA"
MUTED = "#6b5940"

def line(x1,y1,x2,y2,color=GOLD,w=6):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'

def polyline(pts,color=GOLD,w=6):
    d = " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    return f'<polyline points="{d}" stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'

def label(x,y,text,color="#C9B8A6"):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="13" font-family="sans-serif" fill="{color}">{text}</text>'

def step_arrow(x1,y,x2,color="#C9B8A6"):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2-6}" y2="{y}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>'
            f'<polygon points="{x2-10},{y-7} {x2},{y} {x2-10},{y+7}" fill="{color}"/>')

def wrap_two(*parts):
    """Variante large pour les pictogrammes à deux poses (Départ -> Fin)."""
    return f'<svg viewBox="0 0 260 130" xmlns="http://www.w3.org/2000/svg" fill="none">{"".join(parts)}</svg>'

def head(cx,cy,r=9):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{CREAM}" stroke="{FLAME}" stroke-width="3"/>'

def ground(y=106,x1=8,x2=112):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{MUTED}" stroke-width="3" stroke-linecap="round" stroke-dasharray="1 7"/>'

def dot(x,y,r=4,color=FLAME):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}"/>'

def arc(cx,cy,r,a1,a2,color=FLAME,w=3,dash="4 4"):
    sx,sy = cx+r*math.cos(math.radians(a1)), cy+r*math.sin(math.radians(a1))
    ex,ey = cx+r*math.cos(math.radians(a2)), cy+r*math.sin(math.radians(a2))
    large = 1 if abs(a2-a1) > 180 else 0
    return f'<path d="M{sx:.1f},{sy:.1f} A{r},{r} 0 {large} 1 {ex:.1f},{ey:.1f}" stroke="{color}" stroke-width="{w}" fill="none" stroke-dasharray="{dash}" stroke-linecap="round"/>'

def wrap(*parts):
    return f'<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" fill="none">{"".join(parts)}</svg>'

diagrams = {}

# 1. Bird Dog — pictogramme deux poses : Départ (quadrupédie neutre) -> Fin (extension opposée)
diagrams["ex-birddog"] = wrap_two(
    ground(100,5,105), ground(100,155,255),
    step_arrow(112,55,148),
    # Départ (tout en or : posture neutre, symétrique, dos plat)
    line(70,45,35,60, GOLD, 6),
    head(78,32, 9),
    line(70,45,70,88, GOLD, 6),
    line(35,60,35,96, GOLD, 6),
    label(55,120,"Départ"),
    # Fin (bras + jambe opposés tendus en flamme, jambe d'appui restée au sol)
    line(220,45,188,60, GOLD, 6),
    head(228,32, 9),
    line(188,60,188,96, GOLD, 6),
    line(220,45,250,25, FLAME, 6),
    line(188,60,152,53, FLAME, 6),
    label(205,120,"Fin"),
)

# 2. Dead Bug — Départ (bras/genou pliés vers le plafond) -> Fin (bras/jambe opposés tendus)
diagrams["ex-deadbug"] = wrap_two(
    line(15,95,55,95, GOLD, 8), head(9,95,9),
    line(35,95,30,62, GOLD, 6),         # bras plié vers le plafond
    line(55,95,68,70, GOLD, 6), line(68,70,90,68, GOLD, 5),  # genou plié (tabletop)
    label(55,120,"Départ"),
    line(165,95,205,95, GOLD, 8), head(159,95,9),
    line(180,95,150,60, FLAME, 6),      # bras tendu
    line(205,95,240,80, FLAME, 6),      # jambe tendue (opposée)
    label(205,120,"Fin"),
)

# 3. Pallof Press — Départ (mains ramenées au sternon) -> Fin (bras poussés devant, flamme)
diagrams["ex-pallof"] = wrap_two(
    ground(106,5,105), ground(106,155,255),
    step_arrow(112,55,148),
    line(60,42,60,78, GOLD, 6), head(60,32,9),
    line(60,78,50,106, GOLD, 6), line(60,78,70,106, GOLD, 6),
    line(60,58,50,58, GOLD, 5),         # mains au sternon
    line(20,58,50,58, MUTED, 3),        # élastique détendu
    label(55,122,"Départ"),
    line(210,42,210,78, GOLD, 6), head(210,32,9),
    line(210,78,200,106, GOLD, 6), line(210,78,220,106, GOLD, 6),
    line(210,58,245,58, FLAME, 6),      # bras poussés devant
    line(170,58,210,58, MUTED, 3),      # élastique tendu
    label(205,122,"Fin"),
)

# 4. Rotation élastique golfique (chop) — Départ (bras bas d'un côté) -> Fin (bras hauts, tournés)
diagrams["ex-bandrotation"] = wrap_two(
    ground(106,5,105), ground(106,155,255),
    step_arrow(112,55,148),
    line(60,44,60,78, GOLD, 6), head(60,34,9),
    line(60,78,48,106, GOLD, 6), line(60,78,74,106, GOLD, 6),
    line(60,70,42,80, GOLD, 5),         # bras/élastique tenus bas
    line(15,95,42,80, MUTED, 3),
    label(55,122,"Départ"),
    line(210,44,210,78, GOLD, 6), head(210,34,9),
    line(210,78,198,106, GOLD, 6), line(210,78,222,106, GOLD, 6),
    line(210,55,242,38, FLAME, 6),      # bras tournés et levés
    arc(210,55,24,300,20),
    line(165,95,192,80, MUTED, 3),
    label(205,122,"Fin"),
)

# 5. Fente avec rotation thoracique — Départ (mains jointes, face avant) -> Fin (buste tourné, flamme)
diagrams["ex-lungerotation"] = wrap_two(
    ground(108,5,105), ground(108,155,255),
    step_arrow(112,55,148),
    line(55,45,58,72, GOLD, 6), head(53,35,9),
    line(58,72,40,108, GOLD, 6),
    line(58,72,80,95, GOLD, 5), line(80,95,88,108, GOLD, 5),
    dot(58,50,4,GOLD),                  # mains jointes devant
    label(55,122,"Départ"),
    line(205,45,208,72, GOLD, 6), head(203,35,9),
    line(208,72,190,108, GOLD, 6),
    line(208,72,230,95, GOLD, 5), line(230,95,238,108, GOLD, 5),
    line(208,55,235,40, FLAME, 6),      # buste/bras tournés
    arc(208,55,20,300,20),
    label(205,122,"Fin"),
)

# 6. World's Greatest Stretch — Départ (main au sol) -> Fin (bras ouvert vers le ciel, flamme)
diagrams["ex-worldsgreateststretch"] = wrap_two(
    ground(108,5,105), ground(108,155,255),
    step_arrow(112,55,148),
    line(35,108,70,80, GOLD, 6), line(70,80,95,108, GOLD, 6),
    line(70,80,66,52, GOLD, 6), head(64,42,9),
    line(70,60,50,72, GOLD, 4),         # main au sol
    label(55,122,"Départ"),
    line(185,108,220,80, GOLD, 6), line(220,80,245,108, GOLD, 6),
    line(220,80,216,52, GOLD, 6), head(214,42,9),
    line(216,55,245,28, FLAME, 6),      # bras ouvert vers le ciel
    arc(216,55,26,270,330),
    label(205,122,"Fin"),
)

# 7. Ouverture de livre (T-spine) — Départ (bras joints devant) -> Fin (bras du dessus ouvert, flamme)
diagrams["ex-openbook"] = wrap_two(
    line(15,55,50,55, GOLD, 7), head(60,55,9),
    polyline([(15,55),(35,68),(33,88)], GOLD, 6),
    line(50,55,68,60, GOLD, 5),         # bras joints devant, fermé
    label(35,110,"Départ"),
    line(165,55,200,55, GOLD, 7), head(210,55,9),
    polyline([(165,55),(185,68),(183,88)], GOLD, 6),
    line(200,55,200,80, GOLD, 4),       # bras du dessous, au sol
    line(200,55,235,25, FLAME, 6),      # bras du dessus qui s'ouvre
    arc(200,55,28,280,330),
    label(195,110,"Fin"),
)

# 8. Étirement hanche 90/90 — Départ (buste droit) -> Fin (penché sur la jambe avant, flamme)
diagrams["ex-90-90"] = wrap_two(
    ground(108,5,105), ground(108,155,255),
    step_arrow(112,55,148),
    line(40,108,65,95, GOLD, 6), line(65,95,90,108, GOLD, 6),
    line(40,108,25,90, GOLD, 5),
    line(60,65,63,90, GOLD, 6), head(58,55,8),
    label(55,122,"Départ"),
    line(190,108,215,95, GOLD, 6), line(215,95,240,108, GOLD, 6),
    line(190,108,175,90, GOLD, 5),
    line(213,72,220,95, FLAME, 6), head(206,63,8),  # buste penché sur la jambe avant
    label(205,122,"Fin"),
)

# 9. Pont fessier — Départ (bassin au sol) -> Fin (hanches levées, flamme)
diagrams["ex-glutebridge"] = wrap_two(
    ground(104,5,105), ground(104,155,255),
    step_arrow(112,55,148),
    head(12,100,9),
    line(20,100,60,100, GOLD, 6),       # à plat, bassin au sol
    line(60,100,60,80, GOLD, 5),
    label(55,122,"Départ"),
    head(162,100,9),
    line(170,100,193,78, FLAME, 6),     # hanche levée
    polyline([(193,78),(220,88),(220,104)], FLAME, 6),
    label(205,122,"Fin"),
)

# 10. Squat gobelet (haltères) — Départ (debout) -> Fin (position basse, flamme)
diagrams["ex-gobletsquat"] = wrap_two(
    ground(108,5,105), ground(108,155,255),
    step_arrow(112,55,148),
    line(60,42,60,72, GOLD, 6), head(60,32,9),
    line(60,72,48,108, GOLD, 6), line(60,72,72,108, GOLD, 6),
    line(50,55,70,55, GOLD, 7),         # haltère tenu haut
    label(55,122,"Départ"),
    line(210,58,210,80, FLAME, 6), head(210,48,9),
    line(210,80,192,108, FLAME, 6), line(192,108,192,92, FLAME, 5),
    line(210,80,228,108, FLAME, 6), line(228,108,228,92, FLAME, 5),
    line(200,65,220,65, GOLD, 7),       # haltère, position basse
    label(205,122,"Fin"),
)

# 11. Rowing élastique — Départ (bras tendus devant) -> Fin (coudes tirés en arrière, flamme)
diagrams["ex-rowelastique"] = wrap_two(
    ground(108,5,105), ground(108,155,255),
    step_arrow(112,55,148),
    line(55,50,68,85, GOLD, 6), head(50,42,9),
    line(68,85,55,108, GOLD, 6), line(68,85,85,108, GOLD, 6),
    line(30,58,60,58, MUTED, 3),
    line(60,58,32,58, GOLD, 5),         # bras tendus devant
    label(55,122,"Départ"),
    line(205,50,218,85, GOLD, 6), head(200,42,9),
    line(218,85,205,108, GOLD, 6), line(218,85,235,108, GOLD, 6),
    line(180,58,210,58, MUTED, 3),
    line(210,58,240,66, FLAME, 6),      # coude tiré en arrière
    label(205,122,"Fin"),
)

# 12. Gainage latéral — Côté gauche -> Côté droit (miroir, l'exercice alterne les côtés)
diagrams["ex-sideplank"] = wrap_two(
    ground(100,10,70), ground(100,190,250),
    step_arrow(112,55,148),
    line(20,80,90,55, GOLD, 7), head(98,50,9),
    line(45,72,45,50, GOLD, 6), line(45,72,45,95, GOLD, 5),
    line(60,66,60,95, GOLD, 5),
    label(55,116,"Côté gauche"),
    line(240,80,170,55, GOLD, 7), head(162,50,9),
    line(215,72,215,50, GOLD, 6), line(215,72,215,95, GOLD, 5),
    line(200,66,200,95, GOLD, 5),
    label(205,116,"Côté droit"),
)

# 13. Chat-Vache — pictogramme deux poses : Chat (dos rond, tête basse) -> Vache (dos creux, tête haute)
diagrams["ex-catcow"] = wrap_two(
    ground(100,5,105), ground(100,155,255),
    step_arrow(112,55,148),
    # Chat : dos arrondi vers le haut, tête rentrée basse
    f'<path d="M70,55 Q52,36 35,60" stroke="{GOLD}" stroke-width="7" fill="none" stroke-linecap="round"/>',
    head(80,70, 9),
    line(70,55,70,90, GOLD, 6),
    line(35,60,35,92, GOLD, 6),
    label(55,120,"Chat"),
    # Vache : dos creusé vers le bas, tête relevée
    f'<path d="M220,55 Q202,74 185,60" stroke="{GOLD}" stroke-width="7" fill="none" stroke-linecap="round"/>',
    head(230,38, 9),
    line(220,55,220,90, GOLD, 6),
    line(185,60,185,92, GOLD, 6),
    label(205,120,"Vache"),
)

# 14. Rotation externe épaule (élastique) — Départ (avant-bras vers l'intérieur) -> Fin (rotation externe, flamme)
diagrams["ex-shoulderband"] = wrap_two(
    ground(108,5,105), ground(108,155,255),
    step_arrow(112,55,148),
    line(60,44,60,80, GOLD, 6), head(60,34,9),
    line(60,80,48,108, GOLD, 6), line(60,80,72,108, GOLD, 6),
    line(60,55,80,55, MUTED, 3),        # coude fixe
    line(80,55,80,75, GOLD, 5),         # avant-bras vers l'intérieur
    label(55,122,"Départ"),
    line(210,44,210,80, GOLD, 6), head(210,34,9),
    line(210,80,198,108, GOLD, 6), line(210,80,222,108, GOLD, 6),
    line(210,55,230,55, MUTED, 3),      # coude fixe
    line(230,55,230,32, FLAME, 6),      # avant-bras en rotation externe
    arc(230,55,20,270,340),
    label(205,122,"Fin"),
)

# 15. Vélo elliptique — Échauffement (posture neutre) -> Effort (plus incliné, plus dynamique, flamme)
diagrams["ex-elliptique-fractionne"] = wrap_two(
    line(30,108,100,108, MUTED, 4),
    line(165,108,235,108, MUTED, 4),
    step_arrow(112,55,148),
    line(60,48,63,78, GOLD, 5), head(56,38,9),
    line(63,78,50,62, GOLD, 4), line(63,78,80,90, GOLD, 4),
    line(63,78,52,104, GOLD, 5), line(63,78,88,98, GOLD, 5),
    label(55,122,"Échauffement"),
    line(213,45,220,72, FLAME, 5), head(206,35,9),
    line(220,72,200,50, FLAME, 5), line(220,72,242,90, FLAME, 5),
    line(220,72,205,104, FLAME, 5), line(220,72,245,96, FLAME, 5),
    label(205,122,"Effort"),
)

# 16. Étirement complet (retour au calme) — Départ (assis buste droit) -> Fin (penché vers les pieds, flamme)
diagrams["ex-catcow-mat-souplesse"] = wrap_two(
    ground(108,5,105), ground(108,155,255),
    step_arrow(112,55,148),
    line(35,108,80,108, GOLD, 6),       # jambes tendues au sol
    line(45,105,50,65, GOLD, 6), head(48,58,9),
    label(55,122,"Départ"),
    line(185,108,230,108, GOLD, 6),
    line(190,105,168,85, FLAME, 6), head(163,80,9),
    line(168,85,148,100, FLAME, 5),     # bras tendus vers les pieds
    label(205,122,"Fin"),
)

with open("js/diagrams.js", "w", encoding="utf-8") as f:
    f.write("/* ==========================================================================\n")
    f.write("   EnForme! — diagrams.js\n")
    f.write("   Pictogrammes SVG par exercice (clé = id d'exercice dans exercises.json).\n")
    f.write("   Style stick-figure minimaliste : trait or (posture), trait flamme (le\n")
    f.write("   segment du corps qui bouge / travaille), pointillés = trajectoire ou élastique.\n")
    f.write("   ========================================================================== */\n\n")
    f.write("window.EXERCISE_DIAGRAMS = ")
    f.write(json.dumps(diagrams, ensure_ascii=False, indent=2))
    f.write(";\n")

print("Généré", len(diagrams), "pictogrammes ->", list(diagrams.keys()))
