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

# 2. Dead Bug — allongé dos au sol, bras/jambe opposés en l'air
diagrams["ex-deadbug"] = wrap(
    ground(100),
    line(30,100,80,100, GOLD, 8),       # dos au sol (torse)
    head(22,100),
    line(80,100,100,80, FLAME, 6),      # jambe levée
    line(45,100,30,60, FLAME, 6),       # bras levé opposé
    line(45,100,60,100),                # autre jambe pliée posée
    line(60,100,60,88),
    line(65,100,90,95),                 # autre bras posé
)

# 3. Pallof Press — debout, bras poussés devant, élastique de côté
diagrams["ex-pallof"] = wrap(
    ground(108),
    line(60,42,60,78),                  # torse
    head(60,32),
    line(60,78,50,106),                 # jambe
    line(60,78,70,106),                 # jambe
    line(60,50,95,50, FLAME, 6),        # bras tendus devant
    line(20,50,60,50, MUTED, 3),        # élastique
)

# 4. Rotation élastique golfique (chop)
diagrams["ex-bandrotation"] = wrap(
    ground(108),
    line(60,44,60,78),
    head(60,34),
    line(60,78,48,106),
    line(60,78,74,106),
    line(60,55,92,38, FLAME, 6),        # bras tendus tournés vers un côté
    arc(60,55,26,180,260),
    line(18,90,40,55, MUTED, 3),        # élastique ancré au sol
)

# 5. Fente avec rotation thoracique
diagrams["ex-lungerotation"] = wrap(
    ground(108),
    line(55,45,58,72),                  # torse
    head(53,35),
    line(58,72,40,108),                 # jambe avant (fente)
    line(58,72,80,95),
    line(80,95,88,108),                 # jambe arrière
    line(58,55,78,42, FLAME, 6),        # bras/rotation vers l'avant
    arc(58,55,20,300,20),
)

# 6. World's Greatest Stretch — grand fendu + ouverture bras
diagrams["ex-worldsgreateststretch"] = wrap(
    ground(108),
    line(35,108,70,80),                 # jambe avant fendue
    line(70,80,95,108),                 # jambe arrière tendue
    line(70,80,66,52),                  # torse
    head(64,42),
    line(70,60,45,72, MUTED, 4),        # main au sol
    line(66,55,95,30, FLAME, 6),        # bras ouvert vers le ciel
    arc(66,55,28,270,330),
)

# 7. Ouverture de livre (T-spine) — allongé sur le côté, genoux pliés, un bras qui s'ouvre
diagrams["ex-openbook"] = wrap(
    line(40,55,75,55, GOLD, 7),         # torse allongé sur le côté
    head(85,55),
    polyline([(40,55),(60,68),(58,88)], GOLD, 6),  # hanche -> genou -> pied (jambes pliées)
    line(75,55,75,80, MUTED, 4),        # bras du dessous, posé au sol
    line(75,55,100,25, FLAME, 6),       # bras du dessus qui s'ouvre
    arc(75,55,30,270,320),
)

# 8. Étirement hanche 90/90
diagrams["ex-90-90"] = wrap(
    ground(108),
    line(40,108,65,95),                 # jambe avant pliée 90°
    line(65,95,90,108),
    line(40,108,25,90),                 # jambe côté pliée 90°
    line(65,95,60,65),                  # torse penché sur jambe avant
    head(53,55, 8),
    line(60,72,42,85, FLAME, 5),        # bras vers jambe avant
)

# 9. Pont fessier — chaîne continue épaule/sol -> hanche levée -> genou -> pied/sol
diagrams["ex-glutebridge"] = wrap(
    ground(104),
    head(12,100),
    line(20,100,35,100),                # épaule au sol
    polyline([(35,100),(58,78),(85,88),(85,104)], FLAME, 6),  # hanche levée -> genou -> pied
)

# 10. Squat gobelet (haltères)
diagrams["ex-gobletsquat"] = wrap(
    ground(108),
    line(60,45,60,75),                  # torse droit
    head(60,35),
    line(60,75,42,108),                 # cuisse pliée
    line(42,108,42,90),
    line(60,75,78,108),
    line(78,108,78,90),
    line(50,58,70,58, FLAME, 8),        # haltère tenu devant la poitrine
)

# 11. Rowing élastique
diagrams["ex-rowelastique"] = wrap(
    ground(108),
    line(55,50,68,85),                  # torse penché en hinge
    head(50,42),
    line(68,85,55,108),
    line(68,85,85,108),
    line(60,58,30,58, MUTED, 3),        # élastique ancré devant
    line(60,58,90,66, FLAME, 6),        # coude tiré en arrière
)

# 12. Gainage latéral
diagrams["ex-sideplank"] = wrap(
    line(20,80,90,55, GOLD, 7),         # corps aligné en diagonale
    head(98,50),
    line(45,72,45,50, FLAME, 6),        # bras d'appui + hanche levée
    line(45,72,45,95),                  # avant-bras au sol
    line(60,66,60,95),                  # jambes empilées
    ground(100,15,70),
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

# 14. Rotation externe épaule (élastique)
diagrams["ex-shoulderband"] = wrap(
    ground(108),
    line(60,44,60,80),
    head(60,34),
    line(60,80,48,108),
    line(60,80,72,108),
    line(60,55,80,55, MUTED, 3),        # coude fixe
    line(80,55,80,35, FLAME, 6),        # avant-bras en rotation
    arc(80,55,20,270,340),
)

# 15. Vélo elliptique — fractionné
diagrams["ex-elliptique-fractionne"] = wrap(
    ground(108),
    line(60,48,63,78),                  # torse penché en avant
    head(56,38),
    line(63,78,45,60, FLAME, 5),        # bras arrière
    line(63,78,85,95, FLAME, 5),        # bras avant
    line(63,78,50,108),                 # jambe arrière
    line(63,78,90,100),                 # jambe avant
    line(30,110,100,110, MUTED, 4),     # base de l'appareil
)

# 16. Étirement complet (retour au calme, assis, buste vers l'avant)
diagrams["ex-catcow-mat-souplesse"] = wrap(
    ground(108),
    line(35,108,80,108, GOLD, 6),       # jambes tendues au sol
    line(38,105,60,68, FLAME, 6),       # torse penché vers l'avant
    head(65,60),
    line(60,68,40,85, MUTED, 4),        # bras tendus vers les pieds
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
