import re, os, shutil, zipfile
SRC = os.path.join(os.path.dirname(__file__), 'src')
OUT = os.path.join(os.path.dirname(__file__), 'out')
raw = open(os.path.join(SRC, 'pages.html'), encoding='utf-8').read()
css = open(os.path.join(SRC, 'styles.css'), encoding='utf-8').read()
js = open(os.path.join(SRC, 'main.js'), encoding='utf-8').read() + '\n' + open(os.path.join(SRC, 'chat.js'), encoding='utf-8').read()

import sys as _sys
_sys.path.insert(0, SRC)
from posts import POSTS, DATE, DATE_LABEL
def _card(p):
    return (f'<a class="post-card" href="@{p["id"]}"><span class="pc-cat">{p["category"]}</span>'
            f'<h3>{p["title"]}</h3><p>{p["excerpt"]}</p><span class="pc-meta">{p["read"]} · Read article {{{{i:arrow}}}}</span></a>')
_blog_cards = ''.join(_card(p) for p in POSTS)
_gen = f"""
<!--PAGE:blog-->
<section class="block page-hero">
  <div class="left">
    <div class="crumbs"><a href="@home">Home</a><span>/</span><span>Blog</span></div>
    <span class="pill">Blog</span>
    <h1>Digital marketing insights <span class="ghost">from Dubai and Kerala.</span></h1>
  </div>
  <div class="right"><p>Practical guides on Meta Ads, SEO, social media and local marketing for businesses in Dubai, Kannur, Kozhikode and across Kerala.</p></div>
</section>
<section class="block" style="border-top:0"><div class="post-grid">{_blog_cards}</div></section>
<!--/PAGE-->
"""
# Contextual internal links at the end of each article (helps the location and service pages rank)
RELATED = {
  'kochi': ['kannur', 'kozhikode', 'google-business-profile'],
  'malappuram': ['kozhikode', 'kannur', 'services'],
  'thrissur': ['kannur', 'kozhikode', 'services'],
  'google-first-page': ['google-business-profile', 'kannur', 'services'],
  'meta-ads-dubai-real-estate': ['services', 'clients', 'about'],
  'google-business-profile': ['payyanur', 'kannur', 'google-first-page'],
}
REL_LABEL = {'payyanur': 'Digital marketer in Payyanur', 'kannur': 'Digital marketing specialist in Kannur', 'kozhikode': 'Digital marketing strategist in Kozhikode (Calicut)',
             'services': 'Digital marketing services in Dubai: Meta Ads, content and lead generation', 'clients': 'Brands I’ve helped grow in the UAE and India',
             'about': 'About Abhishek Prakash', **{p['id']: p['title'] for p in POSTS}}
def _related(pid):
    ids = RELATED.get(pid, [])
    if not ids: return ''
    return '<h2>Related reading</h2><ul>' + ''.join(f'<li><a href="@{i}">{REL_LABEL[i]}</a></li>' for i in ids) + '</ul>'
for _p in POSTS:
    _i = POSTS.index(_p); _others = [POSTS[(_i + k) % len(POSTS)] for k in (1, 2, 3)]  # rotate so every article gets inbound links
    _gen += f"""
<!--PAGE:{_p['id']}-->
<section class="block page-hero">
  <div class="left">
    <div class="crumbs"><a href="@home">Home</a><span>/</span><a href="@blog">Blog</a><span>/</span><span>{_p['category']}</span></div>
    <span class="pill">{_p['category']}</span>
    <h1>{_p['h1']}</h1>
  </div>
  <div class="right">
    <div class="byline"><span class="me-pic sm">{{{{photo:abhishek-headshot}}}}</span><div><b>Abhishek Prakash</b><span>{DATE_LABEL} · {_p['read']}</span></div></div>
    <p>{_p['excerpt']}</p>
  </div>
</section>
<section class="block" style="border-top:0">
  <article class="article">{_p['body']}{_related(_p['id'])}
    <div class="post-cta"><div><b>Want help with your marketing?</b><span>I reply within 24 hours, 7 days a week.</span></div><a class="btn btn-hot" href="@contact">Contact Me {{{{i:arrow}}}}</a></div>
  </article>
</section>
<div class="gap"></div>
<section class="block">
  <div class="split-head"><h2>More articles <span class="ghost">you might like.</span></h2><p class="muted"><a class="v link" href="@blog">See all articles</a></p></div>
  <div class="post-grid">{''.join(_card(o) for o in _others)}</div>
</section>
<!--/PAGE-->
"""
# ---- service pages and case studies (data in src/landing.py) ----
from landing import SERVICE_PAGES, CASE_STUDIES, ROAS_NOTE, KANNUR_PAGES
SERVICE_PAGES = SERVICE_PAGES + KANNUR_PAGES
SVC_BY = {s['id']: s for s in SERVICE_PAGES}
CS_BY = {c['id']: c for c in CASE_STUDIES}
def _faq_html(items):
    return ('<div class="faq" style="border-top:0;padding-top:0"><div class="faq-list" style="margin-top:0">' +
            ''.join(f'<details{" open" if i == 0 else ""}><summary><span class="q">Q{i+1}</span>{q}<span class="pm"></span></summary><div class="ans">{a}</div></details>'
                    for i, (q, a) in enumerate(items)) + '</div></div>')
def _cs_card(c):
    return (f'<a class="post-card" href="@{c["id"]}"><span class="pc-cat">{c["years"]} · {c["where"]}</span>'
            f'<h3>{c["name"]}</h3><p>{c["excerpt"]}</p><span class="pc-meta">{c["role"]} · Read case study {{{{i:arrow}}}}</span></a>')
for _s in SERVICE_PAGES:
    _cells = ''.join(f'<div class="xcell">{{{{i:{ic}}}}}<h3>{h}</h3><p>{d}</p></div>' for ic, h, d in _s['incl'])
    _steps = ''.join(f'<div class="step"><span class="n">{i+1}</span><h3>{h}</h3><p>{d}</p></div>' for i, (h, d) in enumerate(_s['steps']))
    _for = ''.join(f'<li>{x}</li>' for x in _s['for'])
    _roas = f'<div class="also">{{{{i:chart}}}}<span><b>About the ROAS figure:</b> {ROAS_NOTE}</span></div>' if _s['roas'] else ''
    _rel = ' · '.join(f'<a class="v link" href="@{r}">{SVC_BY[r]["name"]}</a>' for r in _s['related'])
    _kn = _s.get('kannur')
    _crumb_mid = '<a href="@kannur">Kannur</a>' if _kn else '<a href="@services">Services</a>'
    _areas = ('<span class="pill plain">All of Kannur district</span><a class="pill plain" href="@payyanur">Payyanur</a><a class="pill plain" href="@kozhikode">Kozhikode</a><a class="pill plain" href="@kerala">Anywhere in Kerala</a>'
              if _kn else '<span class="pill plain">Dubai &amp; the UAE</span><a class="pill plain" href="@kerala">Anywhere in Kerala</a><a class="pill plain" href="@freelance-dubai">Freelance &amp; project work</a>')
    _local = (f'''<section class="block">
  <div class="split-head"><h2>{_s['local_h']}</h2><p class="muted"><a class="v link" href="@kannur">Digital marketing in Kannur</a></p></div>
  <div class="kintro" style="max-width:820px">{''.join(f'<p>{x}</p>' for x in _s['local'])}</div>
</section>

<div class="gap"></div>
''' if _kn else '')
    _gen += f"""
<!--PAGE:{_s['id']}-->
<section class="block page-hero">
  <div class="left">
    <div class="crumbs"><a href="@home">Home</a><span>/</span>{_crumb_mid}<span>/</span><span>{_s['crumb']}</span></div>
    <span class="pill">{_s['pill']}</span>
    <h1>{_s['h1']}</h1>
  </div>
  <div class="right">
    <p>{_s['lead']}</p>
    <div class="btn-row"><a class="btn btn-hot" href="@contact">Discuss your project</a><a class="btn btn-line" href="@case-studies">See case studies</a></div>
  </div>
</section>
{{{{stats}}}}

<div class="gap"></div>

{_local}<section class="block">
  <div class="split-head"><h2>{_s['incl_h']}</h2><p class="muted">{_s['incl_p']}</p></div>
  <div class="xgrid x3">{_cells}</div>
  <div class="areas"><span class="label">Available for</span>{_areas}</div>
</section>

<div class="gap"></div>

<section class="block">
  <div class="split-head"><h2>Who it’s for <span class="ghost">and how we’ll work.</span></h2><p class="muted">Clear steps, honest communication and results you can measure.</p></div>
  <div class="svc-detail" style="border-top:1px solid var(--line)"><span class="n">Fit</span><div><h3>A good fit if you are</h3><p>Not sure it fits? Send a message and I’ll tell you honestly.</p></div><div><ul class="checks">{_for}</ul></div></div>
  <div class="steps">{_steps}</div>
</section>

<div class="gap"></div>

<section class="block">
  <div class="split-head"><h2>Proof, <span class="ghost">from real work.</span></h2><p class="muted"><a class="v link" href="@case-studies">All case studies</a></p></div>
  <div class="post-grid">{''.join(_cs_card(CS_BY[c]) for c in _s['proof'])}</div>
  {_roas}
</section>

<div class="gap"></div>

<section class="block">
  <div class="split-head"><h2>{_s['name']}: <span class="ghost">common questions.</span></h2><p class="muted">I respond within 24 hours, 7 days a week.</p></div>
  {_faq_html(_s['faq'])}
  <div class="also">{{{{i:sliders}}}}<span><b>Related services:</b> {_rel}</span></div>
</section>
<!--/PAGE-->
"""
_cs_grid = ''.join(_cs_card(c) for c in CASE_STUDIES)
_gen += f"""
<!--PAGE:case-studies-->
<section class="block page-hero">
  <div class="left">
    <div class="crumbs"><a href="@home">Home</a><span>/</span><span>Case studies</span></div>
    <span class="pill">Work · Case studies</span>
    <h1>Case studies <span class="ghost">from Dubai, Kerala and beyond.</span></h1>
  </div>
  <div class="right">
    <p>What I did, what changed and what I learned, for each stage of my career. Each case study says clearly what was my own work and what was a team effort.</p>
    <div class="btn-row"><a class="btn btn-hot" href="@contact">Start a project</a><a class="btn btn-line" href="@clients">All clients</a></div>
  </div>
</section>
<section class="block" style="border-top:0"><div class="post-grid">{_cs_grid}</div>
  <div class="also">{{{{i:check}}}}<span><b>How these are written:</b> no invented numbers. Where a business’s figures aren’t published, the case study says so instead of guessing.</span></div>
</section>
<!--/PAGE-->
"""
for _c in CASE_STUDIES:
    _i = CASE_STUDIES.index(_c); _others = [CASE_STUDIES[(_i + k) % len(CASE_STUDIES)] for k in (1, 2, 3)]
    _gen += f"""
<!--PAGE:{_c['id']}-->
<section class="block page-hero">
  <div class="left">
    <div class="crumbs"><a href="@home">Home</a><span>/</span><a href="@case-studies">Case studies</a><span>/</span><span>{_c['crumb']}</span></div>
    <span class="pill">Case study · {_c['years']}</span>
    <h1>{_c['h1']}</h1>
  </div>
  <div class="right"><p>{_c['lead']}</p></div>
</section>
<section class="block" style="border-top:0">
  <div class="xgrid cs-facts">
    <div class="xcell">{{{{i:team}}}}<h3>Role</h3><p>{_c['role']}</p></div>
    <div class="xcell">{{{{i:cal}}}}<h3>When</h3><p>{_c['years']}</p></div>
    <div class="xcell">{{{{i:pin}}}}<h3>Where</h3><p>{_c['where']}</p></div>
    <div class="xcell">{{{{i:megaphone}}}}<h3>Channels</h3><p>{_c['channels']}</p></div>
  </div>
</section>
<div class="gap"></div>
<section class="block">
  <article class="article">{_c['body']}
    <div class="post-cta"><div><b>Want results like this for your brand?</b><span>I reply within 24 hours, 7 days a week.</span></div><a class="btn btn-hot" href="@contact">Contact Me {{{{i:arrow}}}}</a></div>
  </article>
</section>
<div class="gap"></div>
<section class="block">
  <div class="split-head"><h2>More case studies <span class="ghost">to read next.</span></h2><p class="muted"><a class="v link" href="@case-studies">All case studies</a></p></div>
  <div class="post-grid">{''.join(_cs_card(o) for o in _others)}</div>
</section>
<!--/PAGE-->
"""
_home_blog = ''.join(_card(p) for p in POSTS[:3])
raw = raw.replace('{{home-blog}}', _home_blog)
raw = raw.replace('\n<!--PAGE:thanks-->', _gen + '\n<!--PAGE:thanks-->', 1)

P = {
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
 'arrowur':'<path d="M7 17L17 7M9 7h8v8"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 'phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2"/>',
 'pin':'<path d="M12 21s-7-6.2-7-11a7 7 0 0114 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 'megaphone':'<path d="M3 11v2a1 1 0 001 1h2l5 4V6L6 10H4a1 1 0 00-1 1z"/><path d="M15 9a4 4 0 010 6M18 6a8 8 0 010 12"/>',
 'search':'<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
 'code':'<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
 'target':'<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>',
 'pen':'<path d="M4 20l4-1 11-11-3-3L5 16l-1 4z"/><path d="M14 6l3 3"/>',
 'cal':'<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>',
 'play':'<rect x="3" y="6" width="18" height="12" rx="3"/><path d="M10 9.5v5l4.5-2.5z"/>',
 'cake':'<path d="M4 20h16v-7a2 2 0 00-2-2H6a2 2 0 00-2 2v7z"/><path d="M4 15c2 1.5 4 1.5 6 0s4-1.5 6 0 3 1 4 0M12 11V7"/>',
 'cap':'<path d="M2 9l10-5 10 5-10 5-10-5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/>',
 'device':'<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/>',
 'building':'<path d="M4 21V5l8-2v18M12 9h8v12M8 8v.01M8 12v.01M8 16v.01M16 13v.01M16 17v.01M2 21h20"/>',
 'grid':'<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
 'globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18"/>',
 'bolt':'<path d="M13 3L5 14h6l-1 7 8-11h-6l1-7z"/>',
 'chart':'<path d="M5 20v-8M11 20V5M17 20v-5M3 20h18"/>',
 'video':'<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/>',
 'funnel':'<path d="M3 5h18l-7 8v6l-4 2v-8z"/>',
 'sliders':'<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
 'star':'<path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.6 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z"/>',
 'share':'<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 10.8l7.6-3.6M8.2 13.2l7.6 3.6"/>',
 'team':'<circle cx="12" cy="7" r="3"/><circle cx="5" cy="10" r="2"/><circle cx="19" cy="10" r="2"/><path d="M7 20a5 5 0 0110 0M2 19a3.5 3.5 0 015-3M22 19a3.5 3.5 0 00-5-3"/>',
 'check':'<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 'chat':'<path d="M4 5h16v11H9l-5 4z"/><path d="M8.5 10.5h.01M12 10.5h.01M15.5 10.5h.01"/>',
 'users':'<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0112 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2A5 5 0 0121 19"/>',
}
BRANDMARK = open(os.path.join(SRC, 'brand', 'inline.svg'), encoding='utf-8').read()
import base64 as _b64w
WA_SPA = 'data:image/svg+xml;base64,' + _b64w.b64encode(open(os.path.join(SRC, 'brand', 'wa-glyph-white.svg'), 'rb').read()).decode()
def icons(s):
    s = s.replace('{{brandmark}}', BRANDMARK)
    return re.sub(r'\{\{i:(\w+)\}\}', lambda m: f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{P[m.group(1)]}</svg>', s)

def grab(tag, name):
    m = re.search(rf'<!--{tag}:{name}-->(.*?)<!--/(?:PAGE|PART)-->', raw, re.S)
    return m.group(1)
header = re.search(r'<!--HEADER-->(.*?)<!--/HEADER-->', raw, re.S).group(1)
footer = re.search(r'<!--FOOTER-->(.*?)<!--/FOOTER-->', raw, re.S).group(1)
parts = {k: grab('PART', k) for k in re.findall(r'<!--PART:([\w-]+)-->', raw)}
pages = (['home', 'about', 'services'] + [s['id'] for s in SERVICE_PAGES] + ['case-studies'] + [c['id'] for c in CASE_STUDIES] +
         ['clients', 'contact', 'kerala', 'kannur', 'payyanur', 'kozhikode', 'freelance-dubai', 'blog'] + [p['id'] for p in POSTS])
FILE_NAMES = {'home': 'index', 'kerala': 'digital-marketing-expert-kerala', 'kannur': 'digital-marketing-kannur', 'payyanur': 'digital-marketing-payyanur', 'kozhikode': 'digital-marketing-kozhikode',
              'freelance-dubai': 'freelance-digital-marketer-dubai', 'blog': 'blog', **{p['id']: p['slug'] for p in POSTS},
              **{s['id']: s['slug'] for s in SERVICE_PAGES}, **{c['id']: c['slug'] for c in CASE_STUDIES}}
# Main-menu item highlighted on each page (sub-pages light up their section)
NAV_KEY = {**{s['id']: 'services' for s in SERVICE_PAGES}, 'case-studies': 'work', **{c['id']: 'work' for c in CASE_STUDIES}, **{p['id']: 'blog' for p in POSTS}}

def fill(s):
    for _ in range(2):
        for k, v in parts.items():
            s = s.replace('{{%s}}' % k, v)
    return icons(s)

import base64, struct
def imgsize(path):
    """(width, height) of a PNG, JPEG or WebP file, standard library only. Used for width/height attributes (prevents layout shift)."""
    d = open(path, 'rb').read()
    if d[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', d[16:24])
    if d[:4] == b'RIFF' and d[8:12] == b'WEBP':
        k = d[12:16]
        if k == b'VP8X':
            return 1 + int.from_bytes(d[24:27], 'little'), 1 + int.from_bytes(d[27:30], 'little')
        if k == b'VP8L':
            b = int.from_bytes(d[21:25], 'little'); return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
        return struct.unpack('<HH', d[26:30])[0] & 0x3FFF, struct.unpack('<HH', d[26:30])[1] & 0x3FFF
    i = 2
    while i < len(d):
        if d[i] != 0xFF: i += 1; continue
        mk = d[i + 1]; ln = struct.unpack('>H', d[i + 2:i + 4])[0]
        if mk in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack('>HH', d[i + 5:i + 9]); return w, h
        i += 2 + ln
    raise ValueError(path)

LOGO_DIR = os.path.join(SRC, 'logos')
LOGO_NAMES = {'saj-realty': 'SAJ Realty', 'wrapshap': 'WrapShap', 'ruyah-by-naas': 'Ruyah by Naas', 'k1-kitchen-gallery': 'K1 Kitchen Gallery',
              'land4sale-payyanur': 'Land4Sale Payyanur', 'modus-d3': 'Modus D3', 'the-district': 'The District', 'auto-jota': 'Auto Jota',
              'brandvo-digital': 'Brandvo Digital', 'zee-real-estate': 'Zee Real Estate', 'unicorn-bakes': 'Unicorn Bakes', 'ethra': 'Ethra'}
def logos(s, mode):
    def rep(m):
        slug = m.group(1); alt = LOGO_NAMES.get(slug, slug.replace('-', ' ').title()) + ' logo'
        f = os.path.join(LOGO_DIR, slug + '.png'); w, h = imgsize(f)
        if mode == 'spa':
            src = 'data:image/png;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
        else:
            src = '/img/logos/%s.png' % slug
        return '<img src="%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async">' % (src, alt, w, h)
    return re.sub(r'\{\{logo:([\w-]+)\}\}', rep, s)

PHOTO_DIR = os.path.join(SRC, 'photos')
MIME = {'.jpg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp'}
def photos(s, mode):
    def rep(m):
        name = m.group(1)
        f = next(x for x in os.listdir(PHOTO_DIR) if x.startswith(name + '.'))
        ext = os.path.splitext(f)[1]
        if mode == 'spa':
            src = 'data:%s;base64,%s' % (MIME[ext], base64.b64encode(open(os.path.join(PHOTO_DIR, f), 'rb').read()).decode())
        else:
            src = '/img/' + f
        alt = '@TheWorldStories profile picture' if name.startswith('tws') else 'Abhishek Prakash, digital marketing specialist in Dubai'
        w, h = imgsize(os.path.join(PHOTO_DIR, f))
        extra = ' fetchpriority="high"' if name == 'abhishek-suit' else ' decoding="async"'
        return '<img src="%s" alt="%s" width="%d" height="%d"%s>' % (src, alt, w, h, extra)
    return re.sub(r'\{\{photo:([\w-]+)\}\}', rep, s)

def url_for(p):
    """Clean, root-relative URL for a page id. Matches the canonical URLs and the sitemap (Netlify serves about.html at /about)."""
    f = FILE_NAMES.get(p, p)
    return '/' if f == 'index' else '/' + f

def links(s, mode):
    s = photos(logos(s, mode), mode)
    s = s.replace('{{waicon}}', '<img class="wa-ico" src="%s" alt="" width="18" height="18">' % (WA_SPA if mode == 'spa' else '/img/brand/wa-glyph-white.svg'))
    def rep(m):
        p = m.group(1)
        if p not in FILE_NAMES and p not in pages:
            raise SystemExit('Unknown page link @%s' % p)
        if mode == 'spa':
            return f'href="#{p}"'
        return 'href="%s"' % url_for(p)
    return re.sub(r'href="@([\w-]+)"', rep, s)

GA_ID = 'G-3WZ931YKTM'   # GA4 measurement ID (G-XXXXXXXXXX). Empty = no tracking tag.
GA_TAG = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}",{{"anonymize_ip":true}});</script>' if GA_ID else '')
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">'
DESC = 'Abhishek Prakash, Dubai-based digital marketing specialist with 7+ years across India and the UAE: Meta Ads, performance marketing and content.'
os.makedirs(OUT, exist_ok=True)

# ---- artifact: one file, hash-routed pages ----
TITLES = {'thanks': 'Thank you | Abhishek Prakash', 'notfound': 'Page not found | Abhishek Prakash',
  'home': 'Abhishek Prakash | Digital Marketing Specialist, Kerala & Dubai',
  'about': 'About Abhishek Prakash, Digital Marketing Strategist, Dubai',
  'services': 'Meta Ads & Digital Marketing Services in Dubai | Abhishek',
  'clients': 'Clients & Brands | Abhishek Prakash, Digital Marketer Dubai',
  'kannur': 'Digital Marketing Specialist in Kannur | Abhishek Prakash',
  'kozhikode': 'Digital Marketing Strategist in Kozhikode & Calicut',
  'blog': 'Digital Marketing Blog | Abhishek Prakash',
  'contact': 'Hire a Digital Marketing Expert in Dubai | Abhishek Prakash'}
DESCS = {
  'home': 'Abhishek Prakash, digital marketing specialist for Kerala and Dubai businesses: Meta Ads, social media, SEO, content and lead generation. 7+ years, India & UAE.',
  'about': 'Abhishek Prakash built a 3.2M-follower travel page and now leads performance marketing and content for brands in Dubai, the UAE and India.',
  'services': 'Digital marketing services in Dubai: Meta Ads, social media marketing (SMM), content and video, influencer marketing, lead generation, Google Ads and SEO.',
  'clients': 'Brands grown by Dubai digital marketer Abhishek Prakash: Zee Real Estate, Modus D3, Ethra, Unicorn Bakes, WrapShap, The District and more.',
  'kannur': 'Digital marketing specialist for Kannur businesses: Meta Ads, social media, SEO and lead generation. Payyanur brands grown since 2020. Case studies and FAQs.',
  'kozhikode': 'Digital marketing strategist for Kozhikode (Calicut) businesses: Meta Ads, social media, content, SEO and lead generation, with 7+ years across Kerala and UAE.',
  'contact': 'Hire a freelance digital marketing expert in Dubai for Meta Ads, social media marketing, content and lead generation. Replies within 24 hours.',
}
DESCS['blog'] = 'Practical digital marketing guides on Meta Ads, SEO, social media and local marketing for businesses in Dubai, Kannur, Kozhikode and across Kerala.'
for _p in POSTS + SERVICE_PAGES + CASE_STUDIES:
    TITLES[_p['id']] = _p['seo_title']
    DESCS[_p['id']] = _p['desc']
TITLES['kerala'] = 'Digital Marketing Expert in Kerala | Abhishek Prakash'
DESCS['kerala'] = 'Digital marketing anywhere in Kerala: Meta Ads, social media, content and lead generation, from a strategist with Kannur roots and Dubai experience.'
TITLES['freelance-dubai'] = 'Freelance Digital Marketer in Dubai | Abhishek Prakash'
DESCS['freelance-dubai'] = 'Freelance digital marketer in Dubai for Meta Ads, lead generation, social media and content: by project, monthly or as a consultant. 7+ years in UAE & India.'
TITLES['payyanur'] = 'Digital Marketer in Payyanur, Kannur | Abhishek Prakash'
DESCS['payyanur'] = 'Digital marketer for Payyanur businesses: Meta Ads, Instagram, content and lead generation. Worked with Unicorn Bakes, Brandvo Digital and Land4Sale Payyanur.'
TITLES['case-studies'] = 'Digital Marketing Case Studies | Abhishek Prakash'
DESCS['case-studies'] = 'Case studies from Abhishek Prakash: @TheWorldStories (3.2M followers), Unicorn Bakes, Fairmont and Zee Real Estate, with role and team work kept separate.'

body = ''.join(f'<div data-page="{p}" data-title="{TITLES.get(p, "Abhishek Prakash")}">{fill(grab("PAGE", p))}</div>' for p in pages)
import base64 as _b64
SPA_ICON = '<link rel="icon" href="data:image/svg+xml;base64,' + _b64.b64encode(open(os.path.join(SRC, 'brand', 'mark.svg'), 'rb').read()).decode() + '">'
spa = f'''<title>Abhishek Prakash</title>
<script>document.documentElement.classList.add('rv-js')</script>
{SPA_ICON}
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{DESC}">
{FONT}
<style>{css}</style>
{links(fill(header), 'spa')}
<div class="wrap"><div class="frame">
{links(body, 'spa')}
{links(fill(footer), 'spa')}
<script>document.body.setAttribute('data-mode','spa');</script>
<script>{js}</script>
'''
open(os.path.join(OUT, 'abhishek-really.html'), 'w', encoding='utf-8').write(spa)

# ---- hosted: real multi-page site ----
H = os.path.join(OUT, 'abhishek-really-site')
shutil.rmtree(H, ignore_errors=True); os.makedirs(H)
open(os.path.join(H, 'styles.css'), 'w', encoding='utf-8').write(css)
open(os.path.join(H, 'main.js'), 'w', encoding='utf-8').write(js)
os.makedirs(os.path.join(H, 'img', 'logos'))
for f in os.listdir(PHOTO_DIR):
    shutil.copy(os.path.join(PHOTO_DIR, f), os.path.join(H, 'img', f))
for f in os.listdir(LOGO_DIR):
    shutil.copy(os.path.join(LOGO_DIR, f), os.path.join(H, 'img', 'logos', f))

FORM_NETLIFY = '<form class="form" id="contact-form" name="contact" method="POST" action="/thanks.html" data-netlify="true" netlify-honeypot="bot-field" novalidate><input type="hidden" name="form-name" value="contact"><p hidden><label>Leave this empty: <input name="bot-field"></label></p>'

# ---- structured data (JSON-LD) for search engines ----
import json as _json, html as _html
_faq = re.findall(r'<summary><span class="q">Q\d+</span>(.*?)<span class="pm"></span></summary><div class="ans">(.*?)</div>', parts['faq'], re.S)
_faq = [(_html.unescape(re.sub('<[^>]+>', '', q)).strip(), _html.unescape(re.sub('<[^>]+>', '', a)).strip()) for q, a in _faq]
PERSON = {"@type": "Person", "@id": "https://abhishekreally.com/#person", "name": "Abhishek Prakash",
  "jobTitle": "Digital Marketing Specialist", "description": "Dubai-based digital marketing specialist, performance marketer and content strategist with 7+ years of experience across India and the UAE.",
  "url": "https://abhishekreally.com/", "image": {"@type": "ImageObject", "url": "https://abhishekreally.com/img/abhishek-suit.jpg", "width": 1000, "height": 900},
  "alumniOf": {"@type": "EducationalOrganization", "name": "Digital Academy 360"}, "nationality": {"@type": "Country", "name": "India"}, "email": "mailto:abhisheksayyy@gmail.com", "telephone": "+971588615423",
  "address": {"@type": "PostalAddress", "addressLocality": "Dubai", "addressCountry": "AE"},
  "sameAs": ["https://www.linkedin.com/in/prakashabhishek", "https://www.instagram.com/abhishekdigitaluae/", "https://g.page/r/Ccn8e79FhoryEBM"],
  "knowsAbout": ["Digital Marketing", "Performance Marketing", "Meta Ads", "Facebook Ads", "Instagram Ads", "Social Media Marketing", "Content Strategy", "Lead Generation", "Influencer Marketing", "Brand Positioning", "Video Content Direction", "Google Ads", "SEO", "Real Estate Marketing"]}
LLMS_INTRO = """# Abhishek Prakash

> Abhishek Prakash is a digital marketing specialist, performance marketer and content strategist with 7+ years of experience across India and the UAE. He is based in Dubai and works with businesses in Dubai, the UAE and across Kerala, India (including Payyanur, Kannur and Kozhikode). Website: https://abhishekreally.com

## Key facts

- Services: Meta Ads (Facebook and Instagram ads), performance marketing, Google Ads, SEO, social media marketing, content strategy and video scripts, lead generation, Google Business Profile and local SEO, marketing consulting.
- Results: an average 10-15X ROAS on Meta Ads across the brands he manages. 12+ brands grown across the UAE and India.
- Built @TheWorldStories, a travel page on Twitter he created in 2011 that grew to 3.2M+ followers and was the most-followed travel page on Twitter in 2016 (archived: https://web.archive.org/web/20170726141138/twitter.com/theworldstories).
- Experience: Unicorn Bakes, Payyanur (2020-2024, digital marketing and social media growth); Fairmont Project Management Services, Dubai (2025-2026, lead generation and performance advertising); Head of Marketing at Zee Real Estate and Modus D3, Dubai (Aug-Oct 2026).
- Clients include Zee Real Estate, Modus D3, Brandvo Digital, Ethra, SAJ Realty, Ruyah by Naas, Unicorn Bakes, K1 Kitchen Gallery, WrapShap, Auto Jota, The District and Land4Sale Payyanur.
- Education: Post Graduate Program in Digital Marketing, Digital Academy 360 (2023); Bachelor of Business Management (BBM), 2014-2017.
- Google Business Profile: Abhishek Prakash | Digital Marketer in Payyanur (Edat, Payyanur, Kerala 670327): https://g.page/r/Ccn8e79FhoryEBM
- Contact: abhisheksayyy@gmail.com, +971 58 861 5423 (phone and WhatsApp), https://abhishekreally.com/contact
- Profiles: https://www.linkedin.com/in/prakashabhishek, https://www.instagram.com/abhishekdigitaluae/
"""
SITE_UPDATED = '2026-11-19'   # bump when page content changes (sitemap lastmod, article dateModified)
WEBSITE = {"@type": "WebSite", "@id": "https://abhishekreally.com/#website", "url": "https://abhishekreally.com/", "name": "Abhishek Prakash",
  "alternateName": "abhishekreally.com", "inLanguage": "en", "publisher": {"@id": "https://abhishekreally.com/#person"}}
def _ld(*nodes):
    nodes = [n for n in nodes if n]
    if not any(n.get("@type") == "WebSite" for n in nodes):
        nodes.append(WEBSITE)
    return '<script type="application/ld+json">' + _json.dumps({"@context": "https://schema.org", "@graph": nodes}, ensure_ascii=False) + '</script>'
def _crumbs(*items):
    trail = [("Home", "https://abhishekreally.com/")] + list(items)
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(trail)]}
FAQNODE = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in _faq]}
SERVICES = ["Meta Ads & Performance Marketing", "Content Strategy & Video Production", "Social Media & Influencer Marketing", "Lead Generation & Brand Growth", "Google Ads, SEO & WordPress"]
SERVNODE = {"@type": "ItemList", "name": "Digital marketing services in Dubai", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": n, "serviceType": n, "provider": {"@id": "https://abhishekreally.com/#person"}, "areaServed": [{"@type": "City", "name": "Dubai"}, {"@type": "Country", "name": "United Arab Emirates"}, {"@type": "Country", "name": "India"}]}} for i, n in enumerate(SERVICES)]}
BUSINESS = {"@type": "ProfessionalService", "@id": "https://abhishekreally.com/#business", "name": "Abhishek Prakash | Digital Marketer in Payyanur",
  "description": "Freelance digital marketing: Meta Ads, Google Ads, SEO, social media, content strategy and lead generation for businesses in Kerala and Dubai.",
  "url": "https://abhishekreally.com/digital-marketing-payyanur", "telephone": "+971588615423", "email": "abhisheksayyy@gmail.com",
  "image": "https://abhishekreally.com/img/brand/logo-mark-1024.png", "logo": "https://abhishekreally.com/img/brand/logo-mark-1024.png",
  "address": {"@type": "PostalAddress", "streetAddress": "Edat", "addressLocality": "Payyanur", "addressRegion": "Kerala", "postalCode": "670327", "addressCountry": "IN"},
  "hasMap": "https://g.page/r/Ccn8e79FhoryEBM", "sameAs": ["https://g.page/r/Ccn8e79FhoryEBM"], "founder": {"@id": "https://abhishekreally.com/#person"},
  "areaServed": [{"@type": "City", "name": n} for n in ["Payyanur", "Kannur", "Kozhikode", "Kasaragod"]] + [{"@type": "State", "name": "Kerala"}, {"@type": "City", "name": "Dubai"}],
  "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "19:00"}]}
LD = {
  'home': _ld(WEBSITE, PERSON, BUSINESS, FAQNODE),
  'about': _ld({"@type": "ProfilePage", "url": "https://abhishekreally.com/about", "name": "About Abhishek Prakash", "mainEntity": {"@id": "https://abhishekreally.com/#person"}, "dateModified": SITE_UPDATED},
               PERSON, _crumbs(("About", "https://abhishekreally.com/about"))),
  'services': _ld(PERSON, SERVNODE, FAQNODE, _crumbs(("Services", "https://abhishekreally.com/services"))),
  'contact': _ld({"@type": "ContactPage", "url": "https://abhishekreally.com/contact", "name": "Contact Abhishek Prakash", "about": {"@id": "https://abhishekreally.com/#person"}},
                 PERSON, FAQNODE, _crumbs(("Contact", "https://abhishekreally.com/contact"))),
  'clients': _ld({"@type": "CollectionPage", "url": "https://abhishekreally.com/clients", "name": "Clients and brands", "about": {"@id": "https://abhishekreally.com/#person"}},
                 PERSON, _crumbs(("Clients", "https://abhishekreally.com/clients"))),
  'kannur': None,
}

_kp = grab('PAGE', 'kannur')
_kfaq = [(_html.unescape(re.sub('<[^>]+>', '', q)).strip(), _html.unescape(re.sub('<[^>]+>', '', a)).strip()) for q, a in re.findall(r'<summary><span class="q">Q\d+</span>(.*?)<span class="pm"></span></summary><div class="ans">(.*?)</div>', _kp, re.S)]
LD['kannur'] = _ld(
  {"@type": "Service", "name": "Digital marketing in Kannur", "serviceType": "Digital Marketing", "provider": {"@id": "https://abhishekreally.com/#person"},
   "areaServed": [{"@type": "City", "name": n} for n in ["Kannur", "Payyanur", "Kozhikode"]] + [{"@type": "State", "name": "Kerala"}],
   "description": DESCS['kannur']},
  {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://abhishekreally.com/"}, {"@type": "ListItem", "position": 2, "name": "Digital Marketing in Kannur", "item": "https://abhishekreally.com/digital-marketing-kannur"}]},
  PERSON,
  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in _kfaq]})
_zp = grab('PAGE', 'kozhikode')
_zfaq = [(_html.unescape(re.sub('<[^>]+>', '', q)).strip(), _html.unescape(re.sub('<[^>]+>', '', a)).strip()) for q, a in re.findall(r'<summary><span class="q">Q\d+</span>(.*?)<span class="pm"></span></summary><div class="ans">(.*?)</div>', _zp, re.S)]
LD['kozhikode'] = _ld(
  {"@type": "Service", "name": "Digital marketing in Kozhikode (Calicut)", "serviceType": "Digital Marketing", "provider": {"@id": "https://abhishekreally.com/#person"},
   "areaServed": [{"@type": "City", "name": "Kozhikode", "alternateName": "Calicut"}, {"@type": "State", "name": "Kerala"}], "description": DESCS['kozhikode']},
  {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://abhishekreally.com/"}, {"@type": "ListItem", "position": 2, "name": "Digital Marketing in Kozhikode", "item": "https://abhishekreally.com/digital-marketing-kozhikode"}]},
  PERSON,
  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in _zfaq]})
LD['blog'] = _ld({"@type": "Blog", "name": "Abhishek Prakash – Digital Marketing Blog", "url": "https://abhishekreally.com/blog", "author": {"@id": "https://abhishekreally.com/#person"},
  "blogPost": [{"@type": "BlogPosting", "headline": p['title'], "url": "https://abhishekreally.com/" + p['slug']} for p in POSTS]}, PERSON,
  _crumbs(("Blog", "https://abhishekreally.com/blog")))
for _p in POSTS:
    _u = "https://abhishekreally.com/" + _p['slug']
    LD[_p['id']] = _ld({"@type": "BlogPosting", "headline": _p['title'], "description": _p['desc'], "datePublished": DATE, "dateModified": SITE_UPDATED,
        "author": {"@type": "Person", "@id": "https://abhishekreally.com/#person", "name": "Abhishek Prakash", "url": "https://abhishekreally.com/about"}, "publisher": {"@id": "https://abhishekreally.com/#person"},
        "mainEntityOfPage": _u, "url": _u, "image": "https://abhishekreally.com/img/og-image.jpg", "articleSection": _p['category'], "inLanguage": "en"},
      {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://abhishekreally.com/"}, {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://abhishekreally.com/blog"}, {"@type": "ListItem", "position": 3, "name": _p['title'], "item": _u}]},
      PERSON)
SITE = 'https://abhishekreally.com'
# ---- structured data for service pages, case studies, Kerala and freelance pages ----
def _strip(x): return _html.unescape(re.sub('<[^>]+>', '', x)).strip()
def _faqnode(items): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": _strip(q), "acceptedAnswer": {"@type": "Answer", "text": _strip(a)}} for q, a in items]}
def _page_faq(pid): return re.findall(r'<summary><span class="q">Q\d+</span>(.*?)<span class="pm"></span></summary><div class="ans">(.*?)</div>', grab('PAGE', pid), re.S)
AREAS = [{"@type": "City", "name": "Dubai"}, {"@type": "Country", "name": "United Arab Emirates"}, {"@type": "State", "name": "Kerala"}]
for _s in SERVICE_PAGES:
    _u = SITE + '/' + _s['slug']
    LD[_s['id']] = _ld({"@type": "Service", "name": _s['name'], "serviceType": _s['name'], "url": _u, "description": _s['desc'],
                        "provider": {"@id": "https://abhishekreally.com/#person"},
                        "areaServed": [{"@type": "City", "name": "Kannur"}, {"@type": "City", "name": "Payyanur"}, {"@type": "State", "name": "Kerala"}] if _s.get('kannur') else AREAS},
                       PERSON, _faqnode(_s['faq']),
                       _crumbs(("Digital marketing in Kannur", SITE + "/digital-marketing-kannur"), (_s['crumb'], _u)) if _s.get('kannur') else _crumbs(("Services", SITE + "/services"), (_s['crumb'], _u)))
LD['case-studies'] = _ld({"@type": "CollectionPage", "url": SITE + "/case-studies", "name": "Case studies", "about": {"@id": "https://abhishekreally.com/#person"},
    "hasPart": [{"@type": "Article", "headline": _strip(c['h1']), "url": SITE + '/' + c['slug']} for c in CASE_STUDIES]}, PERSON, _crumbs(("Case studies", SITE + "/case-studies")))
for _c in CASE_STUDIES:
    _u = SITE + '/' + _c['slug']
    LD[_c['id']] = _ld({"@type": "Article", "headline": _strip(_c['h1']), "description": _c['desc'], "url": _u, "mainEntityOfPage": _u,
                        "author": {"@type": "Person", "@id": "https://abhishekreally.com/#person", "name": "Abhishek Prakash", "url": SITE + "/about"},
                        "publisher": {"@id": "https://abhishekreally.com/#person"}, "datePublished": SITE_UPDATED, "dateModified": SITE_UPDATED,
                        "image": SITE + "/img/og-image.jpg", "about": _c['name'], "inLanguage": "en"},
                       PERSON, _crumbs(("Case studies", SITE + "/case-studies"), (_c['crumb'], _u)))
LD['kerala'] = _ld({"@type": "Service", "name": "Digital marketing in Kerala", "serviceType": "Digital Marketing", "url": SITE + "/digital-marketing-expert-kerala",
    "provider": {"@id": "https://abhishekreally.com/#person"}, "areaServed": [{"@type": "State", "name": "Kerala"}] + [{"@type": "City", "name": n} for n in ["Kannur", "Kozhikode", "Kochi", "Thrissur", "Malappuram", "Thiruvananthapuram"]],
    "description": DESCS['kerala']}, PERSON, _faqnode(_page_faq('kerala')), _crumbs(("Digital marketing in Kerala", SITE + "/digital-marketing-expert-kerala")))
LD['payyanur'] = _ld({"@type": "Service", "name": "Digital marketing in Payyanur", "serviceType": "Digital Marketing", "url": SITE + "/digital-marketing-payyanur",
    "provider": {"@id": "https://abhishekreally.com/#person"}, "areaServed": [{"@type": "City", "name": n} for n in ["Payyanur", "Kannur", "Kasaragod"]] + [{"@type": "State", "name": "Kerala"}],
    "description": DESCS['payyanur']}, PERSON, BUSINESS, _faqnode(_page_faq('payyanur')), _crumbs(("Digital marketing in Kerala", SITE + "/digital-marketing-expert-kerala"), ("Payyanur", SITE + "/digital-marketing-payyanur")))
LD['freelance-dubai'] = _ld({"@type": "Service", "name": "Freelance digital marketing in Dubai", "serviceType": "Digital Marketing", "url": SITE + "/freelance-digital-marketer-dubai",
    "provider": {"@id": "https://abhishekreally.com/#person"}, "areaServed": [{"@type": "City", "name": "Dubai"}, {"@type": "Country", "name": "United Arab Emirates"}],
    "description": DESCS['freelance-dubai']}, PERSON, _faqnode(_page_faq('freelance-dubai')), _crumbs(("Freelance digital marketer in Dubai", SITE + "/freelance-digital-marketer-dubai")))
FAVICON = '<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon-96.png" sizes="96x96" type="image/png"><link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png"><link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest"><meta name="theme-color" content="#121211">'
FILES = {'thanks': 'thanks', 'notfound': '404'}
POST_IDS = {x['id'] for x in POSTS}
POST_CAT = {x['id']: x['category'] for x in POSTS}
for p in pages + ['thanks', 'notfound']:
    fname = FILES.get(p, FILE_NAMES.get(p, p))
    canon = SITE + '/' + ('' if fname == 'index' else fname)
    _t, _d = _html.escape(TITLES[p]), _html.escape(DESCS.get(p, DESC))
    is_post = p in POST_IDS
    og = (f'<link rel="canonical" href="{canon}"><meta name="robots" content="index, follow, max-image-preview:large">'
          f'<meta property="og:type" content="{"article" if is_post else ("profile" if p == "about" else "website")}">'
          f'<meta property="og:title" content="{_t}"><meta property="og:description" content="{_d}"><meta property="og:locale" content="en_AE">'
          f'<meta property="og:site_name" content="Abhishek Prakash"><meta property="og:url" content="{canon}">'
          f'<meta property="og:image" content="{SITE}/img/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
          f'<meta property="og:image:alt" content="Abhishek Prakash, digital marketing specialist in Dubai">'
          f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{_t}"><meta name="twitter:description" content="{_d}">'
          f'<meta name="twitter:image" content="{SITE}/img/og-image.jpg"><meta name="author" content="Abhishek Prakash">')
    if is_post:
        og += (f'<meta property="article:published_time" content="{DATE}"><meta property="article:modified_time" content="{SITE_UPDATED}">'
               f'<meta property="article:author" content="{SITE}/about"><meta property="article:section" content="{POST_CAT[p]}">')
    if p == 'about':
        og += '<meta property="profile:first_name" content="Abhishek"><meta property="profile:last_name" content="Prakash">'
    if p == 'home':
        og += '<link rel="preload" as="image" href="/img/abhishek-suit.jpg" fetchpriority="high">'
    if p in ('thanks', 'notfound'):
        og = '<meta name="robots" content="noindex">'
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLES[p]}</title>
<script>document.documentElement.classList.add('rv-js')</script>
{GA_TAG}
<meta name="description" content="{DESCS.get(p, DESC)}">
{FONT}
{FAVICON}
{og}
{LD.get(p, "")}
<link rel="stylesheet" href="/styles.css">
</head>
<body data-current="{NAV_KEY.get(p, p)}">
{links(fill(header), 'mpa')}
<main class="wrap"><div class="frame">
{links(fill(grab("PAGE", p)), 'mpa').replace('<form class="form" id="contact-form" novalidate>', FORM_NETLIFY)}
{links(fill(footer), 'mpa').replace('</div></div>', '</div></main>', 1)}
<script src="/main.js" defer></script>
</body>
</html>
'''
    os.makedirs(os.path.dirname(os.path.join(H, fname + '.html')), exist_ok=True)
    open(os.path.join(H, fname + '.html'), 'w', encoding='utf-8').write(html)
for f in ['favicon.ico', 'favicon-32.png', 'favicon-48.png', 'favicon-96.png', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png']:
    shutil.copy(os.path.join(SRC, 'brand', f), os.path.join(H, f))
os.makedirs(os.path.join(H, 'img', 'brand'), exist_ok=True)
for f in ['mark.svg', 'mark-lime.svg', 'logo-mark-1024.png', 'wa-glyph-white.svg', 'wa-glyph-green.svg']:
    shutil.copy(os.path.join(SRC, 'brand', f), os.path.join(H, 'img', 'brand', f))
shutil.copy(os.path.join(SRC, 'brand', 'og-image.jpg'), os.path.join(H, 'img', 'og-image.jpg'))
open(os.path.join(H, 'site.webmanifest'), 'w', encoding='utf-8').write('{"name":"Abhishek Prakash","short_name":"Abhishek","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}],"theme_color":"#121211","background_color":"#ffffff","display":"standalone","start_url":"/"}')
shutil.copy(os.path.join(SRC, 'brand', 'mark.svg'), os.path.join(H, 'favicon.svg'))
open(os.path.join(H, 'netlify.toml'), 'w', encoding='utf-8').write('''[build]
  publish = "."

# Old WordPress URLs keep working (and keep their search ranking)
[[redirects]]
  from = "/about/"
  to = "/about.html"
  status = 301
[[redirects]]
  from = "/services/"
  to = "/services.html"
  status = 301
# /services and /case-studies are pages AND folders (services.html + services/meta-ads.html).
# Force the bare paths to the hub pages so Netlify never looks for a folder index.
[[redirects]]
  from = "/services"
  to = "/services.html"
  status = 200
  force = true
[[redirects]]
  from = "/case-studies"
  to = "/case-studies.html"
  status = 200
  force = true
[[redirects]]
  from = "/work"
  to = "/case-studies"
  status = 301
[[redirects]]
  from = "/work.html"
  to = "/clients.html"
  status = 301
[[redirects]]
  from = "/contact/"
  to = "/contact.html"
  status = 301

[[headers]]
  for = "/img/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "SAMEORIGIN"
    Referrer-Policy = "strict-origin-when-cross-origin"
''')
AI_BOTS = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User',
           'Google-Extended', 'Applebot', 'Applebot-Extended', 'Bingbot', 'Amazonbot', 'meta-externalagent', 'DuckAssistBot', 'MistralAI-User', 'CCBot']
open(os.path.join(H, 'robots.txt'), 'w', encoding='utf-8').write(
    '# Search engines and AI assistants are welcome to crawl and cite this site.\nUser-agent: *\nAllow: /\n\n'
    + ''.join(f'User-agent: {b}\n' for b in AI_BOTS) + 'Allow: /\n\nSitemap: https://abhishekreally.com/sitemap.xml\n')
# llms.txt: plain-language summary for AI assistants (llmstxt.org format)
_llms_pages = '\n'.join(f'- [{_html.unescape(TITLES.get(u, u)).split(" | ")[0]}]({SITE}{url_for(u)}): {_html.unescape(DESCS.get(u, ""))}' for u in pages if u in DESCS)
open(os.path.join(H, 'llms.txt'), 'w', encoding='utf-8').write(LLMS_INTRO + '\n## Pages\n\n' + _llms_pages + '\n')
open(os.path.join(H, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}{url_for(u)}</loc><lastmod>{SITE_UPDATED}</lastmod></url>' for u in pages) + '</urlset>\n')
z = os.path.join(OUT, 'abhishek-really-netlify.zip')
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, _, files in os.walk(H):
        for f in sorted(files):
            full = os.path.join(root, f)
            zf.write(full, os.path.relpath(full, H))
print('ok', os.path.getsize(os.path.join(OUT, 'abhishek-really.html')))
