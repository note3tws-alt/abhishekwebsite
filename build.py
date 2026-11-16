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
for _p in POSTS:
    _others = [o for o in POSTS if o['id'] != _p['id']][:3]
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
  <article class="article">{_p['body']}
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
pages = ['home', 'about', 'services', 'clients', 'contact', 'kannur', 'kozhikode', 'blog'] + [p['id'] for p in POSTS]
FILE_NAMES = {'home': 'index', 'kannur': 'digital-marketing-kannur', 'kozhikode': 'digital-marketing-kozhikode', 'blog': 'blog', **{p['id']: p['slug'] for p in POSTS}}

def fill(s):
    for _ in range(2):
        for k, v in parts.items():
            s = s.replace('{{%s}}' % k, v)
    return icons(s)

import base64
LOGO_DIR = os.path.join(SRC, 'logos')
def logos(s, mode):
    def rep(m):
        slug = m.group(1); alt = slug.replace('-', ' ').title() + ' logo'
        if mode == 'spa':
            b = base64.b64encode(open(os.path.join(LOGO_DIR, slug + '.png'), 'rb').read()).decode()
            src = 'data:image/png;base64,' + b
        else:
            src = 'img/logos/%s.png' % slug
        return ('<img src="%s" alt="%s">' if mode == 'spa' else '<img src="%s" alt="%s" loading="lazy">') % (src, alt)
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
            src = 'img/' + f
        alt = '@TheWorldStories profile picture' if name.startswith('tws') else 'Abhishek Prakash, digital marketing specialist in Dubai'
        return '<img src="%s" alt="%s">' % (src, alt)
    return re.sub(r'\{\{photo:([\w-]+)\}\}', rep, s)

def links(s, mode):
    s = photos(logos(s, mode), mode)
    s = s.replace('{{waicon}}', '<img class="wa-ico" src="%s" alt="" width="18" height="18">' % (WA_SPA if mode == 'spa' else 'img/brand/wa-glyph-white.svg'))
    def rep(m):
        p = m.group(1)
        if mode == 'spa':
            return f'href="#{p}"'
        return 'href="%s"' % (FILE_NAMES.get(p, p) + '.html')
    return re.sub(r'href="@(\w+)"', rep, s)

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">'
DESC = 'Abhishek Prakash, Dubai-based Digital Marketing Specialist with 7+ years across India and the UAE: Meta Ads, performance marketing, content strategy and lead generation.'
os.makedirs(OUT, exist_ok=True)

# ---- artifact: one file, hash-routed pages ----
TITLES = {'thanks': 'Thank you | Abhishek Prakash', 'notfound': 'Page not found | Abhishek Prakash',
  'home': 'Abhishek Prakash | Digital Marketing Specialist in Dubai, UAE',
  'about': 'About Abhishek Prakash | Digital Marketing Strategist in Dubai',
  'services': 'Meta Ads & Digital Marketing Services in Dubai | Abhishek',
  'clients': 'Clients | Digital Marketing Expert in Dubai',
  'kannur': 'Digital Marketing Strategist in Kannur | Abhishek Prakash',
  'kozhikode': 'Digital Marketing Strategist in Kozhikode, Calicut | Abhishek',
  'blog': 'Digital Marketing Blog | Abhishek Prakash',
  'contact': 'Hire a Digital Marketing Expert in Dubai | Abhishek Prakash'}
DESCS = {
  'home': 'Dubai-based digital marketing specialist and Meta Ads expert with 7+ years across India and the UAE. Performance marketing, SMM, content and lead generation.',
  'about': 'Abhishek Prakash built a 3.2M-follower travel page and now leads performance marketing and content for brands in Dubai, the UAE and India.',
  'services': 'Digital marketing services in Dubai: Meta Ads, social media marketing (SMM), content and video, influencer marketing, lead generation, Google Ads and SEO.',
  'clients': 'Brands grown by Dubai digital marketer Abhishek Prakash: Zee Real Estate, Modus D3, Ethra, Unicorn Bakes, WrapShap, The District and more.',
  'kannur': 'Digital marketing strategist for businesses in Kannur, Kerala: Meta Ads, social media marketing, SEO and lead generation. Brands grown in Payyanur since 2020.',
  'kozhikode': 'Digital marketing strategist for Kozhikode (Calicut) businesses: Meta Ads, social media, content, SEO and lead generation, with 7+ years across Kerala and UAE.',
  'contact': 'Hire a freelance digital marketing expert in Dubai for Meta Ads, social media marketing, content and lead generation. Replies within 24 hours.',
}
DESCS['blog'] = 'Practical digital marketing guides on Meta Ads, SEO, social media and local marketing for businesses in Dubai, Kannur, Kozhikode and across Kerala.'
for _p in POSTS:
    TITLES[_p['id']] = _p['seo_title']
    DESCS[_p['id']] = _p['desc']

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
  "url": "https://abhishekreally.com/", "image": "https://abhishekreally.com/img/abhishek-suit.jpg", "email": "mailto:abhisheksayyy@gmail.com", "telephone": "+971588615423",
  "address": {"@type": "PostalAddress", "addressLocality": "Dubai", "addressCountry": "AE"},
  "sameAs": ["https://www.linkedin.com/in/prakashabhishek", "https://www.instagram.com/abhishekdigitaluae/"],
  "knowsAbout": ["Digital Marketing", "Performance Marketing", "Meta Ads", "Facebook Ads", "Instagram Ads", "Social Media Marketing", "Content Strategy", "Lead Generation", "Influencer Marketing", "Brand Positioning", "Video Content Direction", "Google Ads", "SEO", "Real Estate Marketing"]}
def _ld(*nodes):
    return '<script type="application/ld+json">' + _json.dumps({"@context": "https://schema.org", "@graph": list(nodes)}, ensure_ascii=False) + '</script>'
FAQNODE = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in _faq]}
SERVICES = ["Meta Ads & Performance Marketing", "Content Strategy & Video Production", "Social Media & Influencer Marketing", "Lead Generation & Brand Growth", "Google Ads, SEO & WordPress"]
SERVNODE = {"@type": "ItemList", "name": "Digital marketing services in Dubai", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": n, "serviceType": n, "provider": {"@id": "https://abhishekreally.com/#person"}, "areaServed": [{"@type": "City", "name": "Dubai"}, {"@type": "Country", "name": "United Arab Emirates"}, {"@type": "Country", "name": "India"}]}} for i, n in enumerate(SERVICES)]}
LD = {
  'home': _ld({"@type": "WebSite", "@id": "https://abhishekreally.com/#website", "url": "https://abhishekreally.com/", "name": "Abhishek Prakash", "inLanguage": "en"}, PERSON, FAQNODE),
  'about': _ld({"@type": "ProfilePage", "url": "https://abhishekreally.com/about", "mainEntity": {"@id": "https://abhishekreally.com/#person"}}, PERSON),
  'services': _ld(PERSON, SERVNODE, FAQNODE),
  'contact': _ld({"@type": "ContactPage", "url": "https://abhishekreally.com/contact"}, PERSON, FAQNODE),
  'clients': _ld(PERSON),
  'kannur': None,
}

_kp = grab('PAGE', 'kannur')
_kfaq = [(_html.unescape(re.sub('<[^>]+>', '', q)).strip(), _html.unescape(re.sub('<[^>]+>', '', a)).strip()) for q, a in re.findall(r'<summary><span class="q">Q\d+</span>(.*?)<span class="pm"></span></summary><div class="ans">(.*?)</div>', _kp, re.S)]
LD['kannur'] = _ld(
  {"@type": "Service", "name": "Digital marketing in Kannur", "serviceType": "Digital Marketing", "provider": {"@id": "https://abhishekreally.com/#person"},
   "areaServed": [{"@type": "City", "name": n} for n in ["Kannur", "Payyanur", "Thalassery", "Taliparamba", "Kozhikode"]] + [{"@type": "State", "name": "Kerala"}],
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
  "blogPost": [{"@type": "BlogPosting", "headline": p['title'], "url": "https://abhishekreally.com/" + p['slug']} for p in POSTS]}, PERSON)
for _p in POSTS:
    _u = "https://abhishekreally.com/" + _p['slug']
    LD[_p['id']] = _ld({"@type": "BlogPosting", "headline": _p['title'], "description": _p['desc'], "datePublished": DATE, "dateModified": DATE,
        "author": {"@id": "https://abhishekreally.com/#person"}, "publisher": {"@id": "https://abhishekreally.com/#person"},
        "mainEntityOfPage": _u, "url": _u, "image": "https://abhishekreally.com/img/abhishek-suit.jpg", "articleSection": _p['category'], "inLanguage": "en"},
      {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://abhishekreally.com/"}, {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://abhishekreally.com/blog"}, {"@type": "ListItem", "position": 3, "name": _p['title'], "item": _u}]},
      PERSON)
FAVICON = '<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="site.webmanifest"><meta name="theme-color" content="#121211">'
SITE = 'https://abhishekreally.com'
FILES = {'home': 'index', 'kannur': 'digital-marketing-kannur', 'kozhikode': 'digital-marketing-kozhikode', 'thanks': 'thanks', 'notfound': '404'}
for p in pages + ['thanks', 'notfound']:
    fname = FILES.get(p, FILE_NAMES.get(p, p))
    canon = SITE + '/' + ('' if fname == 'index' else fname)
    og = f'<link rel="canonical" href="{canon}"><meta property="og:type" content="website"><meta property="og:title" content="{TITLES[p]}"><meta property="og:description" content="{DESCS.get(p, DESC)}"><meta property="og:locale" content="en_AE"><meta property="og:site_name" content="Abhishek Prakash"><meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/img/abhishek-suit.jpg"><meta name="twitter:card" content="summary_large_image">'
    if p in ('thanks', 'notfound'):
        og = '<meta name="robots" content="noindex">'
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLES[p]}</title>
<script>document.documentElement.classList.add('rv-js')</script>
<meta name="description" content="{DESCS.get(p, DESC)}">
{FONT}
{FAVICON}
{og}
{LD.get(p, "")}
<link rel="stylesheet" href="styles.css">
</head>
<body data-current="{p}">
{links(fill(header), 'mpa')}
<main class="wrap"><div class="frame">
{links(fill(grab("PAGE", p)), 'mpa').replace('<form class="form" id="contact-form" novalidate>', FORM_NETLIFY)}
{links(fill(footer), 'mpa').replace('</div></div>', '</div></main>', 1)}
<script src="main.js"></script>
</body>
</html>
'''
    if p in ('notfound',):
        for _f in set(FILE_NAMES.values()) | set(pages):
            html = html.replace(f'href="{_f}.html"', f'href="/{_f}.html"')
        html = html.replace('href="/index.html"', 'href="/"').replace('href="styles.css"', 'href="/styles.css"').replace('src="main.js"', 'src="/main.js"').replace('href="favicon.svg"', 'href="/favicon.svg"').replace('src="img/', 'src="/img/').replace('href="favicon-32.png"', 'href="/favicon-32.png"').replace('href="apple-touch-icon.png"', 'href="/apple-touch-icon.png"').replace('href="site.webmanifest"', 'href="/site.webmanifest"')
    open(os.path.join(H, fname + '.html'), 'w', encoding='utf-8').write(html)
for f in ['favicon-32.png', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png']:
    shutil.copy(os.path.join(SRC, 'brand', f), os.path.join(H, f))
os.makedirs(os.path.join(H, 'img', 'brand'), exist_ok=True)
for f in ['mark.svg', 'mark-lime.svg', 'logo-mark-1024.png', 'wa-glyph-white.svg', 'wa-glyph-green.svg']:
    shutil.copy(os.path.join(SRC, 'brand', f), os.path.join(H, 'img', 'brand', f))
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
open(os.path.join(H, 'robots.txt'), 'w', encoding='utf-8').write('User-agent: *\nAllow: /\nSitemap: https://abhishekreally.com/sitemap.xml\n')
open(os.path.join(H, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}/{u}</loc><lastmod>2026-11-09</lastmod></url>' for u in ['', 'about', 'services', 'clients', 'contact', 'digital-marketing-kannur', 'digital-marketing-kozhikode', 'blog'] + [p['slug'] for p in POSTS]) + '</urlset>\n')
z = os.path.join(OUT, 'abhishek-really-netlify.zip')
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, _, files in os.walk(H):
        for f in sorted(files):
            full = os.path.join(root, f)
            zf.write(full, os.path.relpath(full, H))
print('ok', os.path.getsize(os.path.join(OUT, 'abhishek-really.html')))
