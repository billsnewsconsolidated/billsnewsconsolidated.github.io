#!/usr/bin/env python3
"""Bills News Consolidated — static article page builder.

Renders every article in articles.json to a static page at article/<slug>.html
so Facebook/X crawlers (which do not run JavaScript) get real Open Graph and
Twitter Card meta tags with the article's own share image and sharpened
shareTitle. The legacy JS viewer (article.html?slug=...) keeps working for old
links; new canonical URLs are:

    https://billsnewsconsolidated.com/article/<slug>.html

Usage:  python3 build-pages.py
Re-run after any edit to articles.json. Requires each article to carry:
image (16:9 hero), imageShare (1200x630), imageCredit, shareTitle.
"""
import json
import os
import sys
from html import escape

BASE = "https://billsnewsconsolidated.com"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "article")

DESKS = {
    "news":            {"label": "News",            "cardClass": "",          "kickerClass": ""},
    "film-room":       {"label": "Film Room",       "cardClass": "film",      "kickerClass": "film"},
    "culture-desk":    {"label": "Culture Desk",    "cardClass": "culture",   "kickerClass": "culture"},
    "the-tailgate":    {"label": "The Tailgate",    "cardClass": "comedy",    "kickerClass": "comedy"},
    "daily-links":     {"label": "Daily Links",     "cardClass": "",          "kickerClass": ""},
    "the-card":        {"label": "The Card",        "cardClass": "sponsored", "kickerClass": "partner"},
    "partner-content": {"label": "Partner Content", "cardClass": "sponsored", "kickerClass": "partner"},
}

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Bills News Consolidated</title>
<meta name="description" content="{excerpt}">
<link rel="canonical" href="{canonical}">
<!-- Open Graph / Twitter Card — baked in at build time so shares carry
     this article's own emotional headline + image (see build-pages.py). -->
<meta property="og:site_name" content="Bills News Consolidated">
<meta property="og:type" content="article">
<meta property="og:title" content="{share_title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:image" content="{share_image_abs}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{share_title}">
<meta name="twitter:description" content="{excerpt}">
<meta name="twitter:image" content="{share_image_abs}">
<link rel="alternate" type="application/rss+xml" title="Bills News Consolidated RSS" href="../feed.xml">
<link rel="icon" href="../favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="../favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="../favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
<link rel="stylesheet" href="../styles.css">
</head>
<body>

<header>
  <div class="topbar">
    <div>
      <div class="logo"><a href="../index.html">BILLS NEWS <span>CONSOLIDATED</span></a></div>
      <div class="tagline">Buffalo Bills news with personalities — every single day.</div>
    </div>
    <a class="newsbtn" href="../newsletter.html">📧 GET THE NEWSLETTER</a>
  </div>
  <nav><div class="navwrap">
    <a href="../index.html?desk=news">NEWS</a>
    <a href="../index.html?desk=film-room">FILM ROOM</a>
    <a href="../index.html?desk=culture-desk">CULTURE DESK</a>
    <a href="../index.html?desk=the-tailgate">THE TAILGATE</a>
    <a href="../index.html?desk=the-card">THE CARD</a>
    <a href="../index.html#videos">VIDEOS</a>
    <a href="../index.html?desk=daily-links">DAILY LINKS</a>
    <a href="../gear-guide.html">GEAR GUIDE</a>
    <a href="../team.html">ABOUT</a>
    <a href="../newsletter.html">NEWSLETTER</a>
  </div></nav>
</header>

<div class="wrap article-shell">
  <div class="adslot leaderboard" style="background:#00338d;border:1px solid #00338d"><a href="https://kalshi.com/r/BNC" target="_blank" rel="sponsored noopener" style="color:#fff;text-decoration:none;font-weight:800;letter-spacing:.02em">KALSHI — Get a FREE $55 when you trade $25 →</a><div style="color:#cfe0ff;font-size:12px;font-weight:600;margin-top:2px">Use code BNC · 18+ · Terms apply</div></div>

  <article class="article-body-card">
    <div class="kicker {kicker_class}">{desk_label}</div>
    <h1>{title}</h1>
    <p class="dek">{excerpt}</p>
    <div class="byline">By <b>{author_upper}</b> · {author_role} · {display_date}</div>
    {disclosure}
    <figure class="hero-fig">
      <img src="../{hero_image}" alt="{title}" width="1600" height="900">
      <figcaption class="img-credit">{image_credit}</figcaption>
    </figure>
    <div class="blitz-banner" style="background:#002266;border-left:5px solid #C60C30;color:#fff;padding:14px 18px;margin:0 0 22px;display:flex;flex-wrap:wrap;align-items:center;gap:8px 18px;font-family:Arial,Helvetica,sans-serif;">
      <div style="flex:1 1 260px;min-width:220px;">
        <div style="font-weight:bold;font-size:17px;letter-spacing:.3px;">Get The BNC Blitz — free</div>
        <div style="font-size:13.5px;color:#dbe4f5;margin-top:3px;line-height:1.45;">Bills news, one stat that matters, and one take. Every morning.</div>
      </div>
      <button type="button" onclick="ml('show', 'q2woz5', true)" style="background:#C60C30;color:#fff;border:0;font-family:Arial,Helvetica,sans-serif;font-weight:bold;font-size:14px;padding:11px 22px;border-radius:4px;cursor:pointer;">Join free</button>
    </div>
    <div class="article-text">
{body_html}
    </div>
  </article>

  <!-- In-article newsletter signup -->
  <div class="newsletter light">
    <h2>Enjoying BNC? Get The BNC Blitz free.</h2>
    <p>The day's Bills news, one stat that matters, and one take you'll argue about — in your inbox every morning. Subscribers also get the ticket &amp; merch giveaways.</p>
    <!-- MailerLite embedded form (BNC Blitz - Website) -->
    <div class="ml-embedded" data-form="TJG0Wm"></div>
    <div class="fineprint">One email each morning. No spam, unsubscribe anytime.</div>
  </div>

  <div class="adslot inarticle-ad" style="background:#00338d;border:1px solid #00338d"><a href="https://kalshi.com/r/BNC" target="_blank" rel="sponsored noopener" style="color:#fff;text-decoration:none;font-weight:800;letter-spacing:.02em">KALSHI — Get a FREE $55 when you trade $25 →</a><div style="color:#cfe0ff;font-size:12px;font-weight:600;margin-top:2px">Use code BNC · 18+ · Terms apply</div></div>

  <h2 class="section">Keep reading</h2><div class="rule"></div>
  <div class="grid related">
{related_html}
  </div>
</div>

<footer>
  <div class="wrap">
    <div>© 2026 Bills News Consolidated</div>
    <div><a href="../index.html">Home</a> · <a href="../gear-guide.html">Gear Guide</a> · <a href="../team.html">About</a> · <a href="../newsletter.html">Newsletter</a> · <a href="../feed.xml">RSS</a></div>
  </div>
  <div class="disclaimer">Bills News Consolidated is an independent fan publication and is not affiliated with the Buffalo Bills or the NFL. All team names and marks are property of their respective owners. <a href="/privacy.html">Privacy Policy</a></div>
</footer>

<script src="../article-gate.js" defer></script>
<!-- MailerLite Universal -->
<script>
    (function(w,d,e,u,f,l,n){{w[f]=w[f]||function(){{(w[f].q=w[f].q||[]).push(arguments);}},l=d.createElement(e),l.async=1,l.src=u,n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);}})
    (window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');
    ml('account', '2756523');
</script>
<!-- End MailerLite Universal -->
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "80f37a665b0d47e1b69bcba986157385"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
"""

CARD = """    <a class="card{card_class}" href="{slug}.html">
      <img class="thumb" src="../{thumb}" alt="" loading="lazy">
      <div class="kicker {kicker_class}">{desk_label}</div>
      <h3>{title}</h3>{disclosure}
      <p>{excerpt}</p>
      <div class="byline">By <b>{author_upper}</b> · {display_date}</div>
    </a>"""


GATE_CTA = """        <div class="gate-cta" id="gateCta">
          <div class="gate-title">You're almost done — finish Bills stories like this in your inbox</div>
          <p>The BNC Blitz is free: the day's Bills news, one stat that matters, and one take, every morning. Join to keep reading — and never miss the end of a story again.</p>
          <button type="button" class="gate-join" onclick="bncJoin()">Join free</button>
          <button type="button" class="gate-skip" onclick="bncKeepReading()">Keep reading — no thanks</button>
        </div>"""


def desk_of(a):
    return DESKS.get(a.get("desk"), DESKS["news"])


def render_article(a, articles):
    d = desk_of(a)
    canonical = f"{BASE}/article/{a['slug']}.html"
    disclosure = ""
    if a.get("sponsored"):
        disclosure = (
            '<div class="disclosure"><b>Partner Content — Paid Promotion</b>'
            "This article is a paid promotion sponsored by a Bills News Consolidated "
            "advertiser. Sponsored columns are produced separately from our news coverage.</div>"
        )
    # Soft gate (2026-11-02): on articles with 6+ paragraphs, the tail from
    # ~65% on renders faded behind a Blitz signup card (see article-gate.js).
    # The text stays in the HTML — soft gate only, shares/SEO unaffected.
    para_html = [f"      <p>{escape(p)}</p>" for p in (a.get("body") or [])]
    n_paras = len(para_html)
    gate_at = max(3, int(n_paras * 0.65)) if n_paras >= 6 else None
    paras = []
    for i, ph in enumerate(para_html):
        if gate_at is not None and i == gate_at:
            paras.append('      <div class="gate-wrap">')
            paras.append('        <div class="gate-tail" id="gateTail">')
        paras.append(ph)
        if i == 1:
            paras.append('      <div class="adslot inarticle-ad" style="background:#00338d;border:1px solid #00338d"><a href="https://kalshi.com/r/BNC" target="_blank" rel="sponsored noopener" style="color:#fff;text-decoration:none;font-weight:800;letter-spacing:.02em">KALSHI — Get a FREE $55 when you trade $25 →</a><div style="color:#cfe0ff;font-size:12px;font-weight:600;margin-top:2px">Use code BNC · 18+ · Terms apply</div></div>')
        if gate_at is not None and i == n_paras - 1:
            paras.append('        </div>')
            paras.append(GATE_CTA)
            paras.append('      </div>')
    # Related: same desk first, then the rest, newest-first order preserved from sort below.
    rel = [x for x in articles if x["slug"] != a["slug"] and x["desk"] == a["desk"]]
    rel += [x for x in articles if x["slug"] != a["slug"] and x["desk"] != a["desk"]]
    cards = []
    for r in rel[:3]:
        rd = desk_of(r)
        cards.append(CARD.format(
            card_class=(" " + rd["cardClass"]) if rd["cardClass"] else "",
            slug=r["slug"],
            thumb=r.get("imageShare", ""),
            kicker_class=rd["kickerClass"],
            desk_label=escape(rd["label"]),
            title=escape(r["title"]),
            disclosure=('<p><i>This article is a paid promotion.</i></p>' if r.get("sponsored") else ""),
            excerpt=escape(r["excerpt"]),
            author_upper=escape(str(r["author"]).upper()),
            display_date=escape(r.get("displayDate", "")),
        ))
    return PAGE.format(
        title=escape(a["title"]),
        excerpt=escape(a["excerpt"]),
        canonical=canonical,
        share_title=escape(a["shareTitle"]),
        share_image_abs=f"{BASE}/{a['imageShare']}",
        kicker_class=d["kickerClass"],
        desk_label=escape(d["label"]),
        author_upper=escape(str(a["author"]).upper()),
        author_role=escape(a.get("authorRole", "")),
        display_date=escape(a.get("displayDate", "")),
        disclosure=disclosure,
        hero_image=a["image"],
        image_credit=escape(a["imageCredit"]),
        body_html="\n".join(paras),
        related_html="\n".join(cards),
    )


BASE = "https://billsnewsconsolidated.com"


def write_feed(articles):
    """Regenerate feed.xml from articles.json — the feed is built, never hand-edited."""
    from datetime import datetime
    from email.utils import format_datetime
    items = []
    for a in articles:
        d = datetime.strptime(a["date"], "%Y-%m-%d").replace(hour=12, tzinfo=None)
        pub = format_datetime(d)
        desc = a["excerpt"]
        if a.get("sponsored"):
            desc = "[Partner Content — paid promotion] " + desc
        url = f"{BASE}/article/{a['slug']}.html"
        items.append(
            "    <item>\n"
            f"      <title>{escape(a['title'])}</title>\n"
            f"      <link>{url}</link>\n"
            f"      <guid isPermaLink=\"true\">{url}</guid>\n"
            f"      <pubDate>{pub}</pubDate>\n"
            f"      <category>{escape(a['desk'])}</category>\n"
            f"      <description>{escape(desc)}</description>\n"
            "    </item>"
        )
    now = format_datetime(datetime.now())
    feed = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>Bills News Consolidated</title>\n"
        f"    <link>{BASE}/</link>\n"
        f'    <atom:link href="{BASE}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        "    <description>Buffalo Bills news with personalities — daily articles on news, film, culture, comedy and The Card, plus The BNC Blitz newsletter.</description>\n"
        "    <language>en-us</language>\n"
        f"    <lastBuildDate>{now}</lastBuildDate>\n\n"
        + "\n\n".join(items)
        + "\n  </channel>\n</rss>\n"
    )
    with open(os.path.join(HERE, "feed.xml"), "w") as f:
        f.write(feed)
    print(f"feed.xml rebuilt with {len(items)} items.")


def main():
    with open(os.path.join(HERE, "articles.json")) as f:
        data = json.load(f)
    articles = data["articles"] if isinstance(data, dict) else data
    articles = sorted(articles, key=lambda a: a["date"], reverse=True)
    missing = [a["slug"] for a in articles
               if not all(a.get(k) for k in ("image", "imageShare", "imageCredit", "shareTitle"))]
    if missing:
        sys.exit(f"articles.json entries missing image fields: {missing}")
    write_feed(articles)
    os.makedirs(OUT_DIR, exist_ok=True)
    for a in articles:
        out = os.path.join(OUT_DIR, a["slug"] + ".html")
        with open(out, "w") as f:
            f.write(render_article(a, articles))
        print("built", os.path.relpath(out, HERE))
    print(f"{len(articles)} static article pages built.")


if __name__ == "__main__":
    main()
