import os

ROOT = r"C:\Users\raeda\Downloads\PM_Final_StudyBook"
SLIDES = os.path.join(ROOT, "slides")


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


order = [
    "sections/section_playbook.html",
    "sections/section_wk6.html",
    "sections/section_wk7.html",
    "sections/section_pricing.html",
    "sections/section_funnel.html",
    "sections/section_gamification.html",
]

parts = [read("front.html")]
for o in order:
    parts.append(read(o))
    if o == "sections/section_playbook.html":
        # Assemble the step-by-step Excel walkthroughs right after the playbook.
        wt = [
            '<section>',
            '<div class="eyebrow">Start here for the spreadsheets</div>',
            '<h2 id="excel-walkthroughs">Excel Labs: solve each one step by step '
            '<span class="badge new">from a blank sheet</span></h2>',
            '<div class="callout">These are the three graded Excel files, each solved from the very '
            'first click. If the spreadsheets scare you, start here. Every walkthrough opens with what '
            'you are handed (the blank sheet), turns the goal into a plain number, then numbers every '
            'move from Step 1 to the answer. The deeper concept teaching lives in the Pricing, Base '
            'Exclusion Funnel, and Design-Your-Own-Products sections; this is the do-it-now recipe.</div>',
            read("sections/wt_pricing.html"),
            read("sections/wt_design.html"),
            read("sections/wt_funnel.html"),
            '</section>',
        ]
        parts.append("\n".join(wt))

decks = [
    ("excel", "Excel Labs: the actual worksheets", "fuel"),
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
     '<div class="callout">Every page of every deck and reading, plus the Excel worksheets, rendered for quick visual revision. Click any image to open it full size in a new tab.</div>']
total = 0
for slug, title, badge in decks:
    d = os.path.join(SLIDES, slug)
    if not os.path.isdir(d):
        continue
    imgs = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    total += len(imgs)
    label = "IN SCOPE" if badge == "in" else ("WORKSHEETS" if slug == "excel" else "REFERENCE")
    noun = "worksheets" if slug == "excel" else "slides"
    g.append(f'<div class="gallery-deck"><h3>{title} <span class="badge {badge}">{label}</span> '
             f'<span class="deck-count">{len(imgs)} {noun}</span></h3>'
             f'<div class="gallery-grid">')
    for im in imgs:
        rel = f"slides/{slug}/{im}"
        base = im[:-4]
        if base.startswith("slide_"):
            try:
                cap = "Slide " + str(int(base.split("_")[1]))
            except ValueError:
                cap = base
        else:
            cap = base.replace("_", " ").replace("-", " ").title()
        g.append(f'<a href="{rel}" target="_blank"><img loading="lazy" src="{rel}" '
                 f'alt="{title} {cap}"><div class="cap">{cap}</div></a>')
    g.append('</div></div>')
g.append('</section>')
parts.append("\n".join(g))

parts.append(read("back.html"))

out = os.path.join(ROOT, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(parts))

print(f"Built index.html: {os.path.getsize(out):,} bytes, {total} images in gallery")
