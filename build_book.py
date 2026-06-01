import os

ROOT = r"C:\Users\raeda\Downloads\PM_Final_StudyBook"
SLIDES = os.path.join(ROOT, "slides")


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


order = [
    "sections/section_wk6.html",
    "sections/section_wk7.html",
    "sections/section_pricing.html",
    "sections/section_funnel.html",
    "sections/section_gamification.html",
]

parts = [read("front.html")]
for o in order:
    parts.append(read(o))

decks = [
    ("week6_ai_growth", "Week 6: AI &amp; Growth Engineering", "in"),
    ("week7_digital_products", "Week 7: Digital Products", "in"),
    ("pricing_strategies", "Reading: Nine Pricing Strategies", "in"),
    ("product_metrics", "Reading: Product Metrics", "in"),
    ("next_best_action", "Reading: Next Best Action (Telco Case)", "in"),
    ("gamification", "Case: Gamification (FLYG)", "in"),
    ("sample_project", "Sample Project: Wage Boost (direction only)", "fuel"),
]

g = ['<section id="gallery">',
     '<h2>Slide gallery <span class="badge new">all decks, scope-tagged</span></h2>',
     '<div class="callout">Every page of every deck and reading, rendered for quick visual revision. Click any slide to open it full size in a new tab.</div>']
total = 0
for slug, title, badge in decks:
    d = os.path.join(SLIDES, slug)
    if not os.path.isdir(d):
        continue
    imgs = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    total += len(imgs)
    label = "IN SCOPE" if badge == "in" else "REFERENCE"
    g.append(f'<div class="gallery-deck"><h3>{title} <span class="badge {badge}">{label}</span> '
             f'<span style="font-family:Inter;font-size:12px;color:var(--ink-mute);font-weight:600">{len(imgs)} slides</span></h3>'
             f'<div class="gallery-grid">')
    for im in imgs:
        rel = f"slides/{slug}/{im}"
        n = im.replace("slide_", "").replace(".png", "")
        try:
            num = str(int(n))
        except ValueError:
            num = n
        g.append(f'<a href="{rel}" target="_blank"><img loading="lazy" src="{rel}" '
                 f'alt="{title} slide {num}"><div class="cap">Slide {num}</div></a>')
    g.append('</div></div>')
g.append('</section>')
parts.append("\n".join(g))

parts.append(read("back.html"))

out = os.path.join(ROOT, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(parts))

print(f"Built index.html: {os.path.getsize(out):,} bytes, {total} slides in gallery")
