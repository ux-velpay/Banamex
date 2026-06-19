#!/usr/bin/env python3
"""
Refactor Claude Design bundle into clean, self-contained HTML.
Input:  /Users/ivonnegonzalez/Desktop/Banamex/Banamex-velpay.html
Output: /Users/ivonnegonzalez/Desktop/Banamex/index.html
"""

import json
import re
import base64
import gzip
from collections import Counter

SRC = "/Users/ivonnegonzalez/Desktop/Banamex/Banamex-velpay.html"
DST = "/Users/ivonnegonzalez/Desktop/Banamex/index.html"

# ── 1. Load source ──────────────────────────────────────────────────────────
print("Reading source file…")
with open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

# ── 2. Extract manifest ─────────────────────────────────────────────────────
print("Extracting manifest…")
manifest_match = re.search(
    r'<script[^>]*type="__bundler/manifest"[^>]*>(.*?)</script>',
    content, re.DOTALL
)
if not manifest_match:
    raise ValueError("Could not find __bundler/manifest script tag")
manifest = json.loads(manifest_match.group(1))
print(f"  Found {len(manifest)} assets in manifest")

# ── 3. Extract template ─────────────────────────────────────────────────────
print("Extracting template…")
tmpl_match = re.search(
    r'<script[^>]*type="__bundler/template"[^>]*>(.*?)</script>',
    content, re.DOTALL
)
if not tmpl_match:
    raise ValueError("Could not find __bundler/template script tag")
template_raw = tmpl_match.group(1).strip()
# Template may be JSON-encoded string or raw HTML
try:
    template_html = json.loads(template_raw)
    if not isinstance(template_html, str):
        template_html = template_raw
except Exception:
    template_html = template_raw
print(f"  Template length: {len(template_html):,} chars")

# ── 4. Build data URI map ───────────────────────────────────────────────────
print("Building data URIs for all assets…")
data_uri_map = {}
font_entries = []   # (family, weight, style, data_uri, mime)
js_entries = []     # (uuid, data_text)
css_entries = []    # (uuid, css_text)

for uuid, entry in manifest.items():
    mime = entry.get("mime", "application/octet-stream")
    raw_b64 = entry.get("data", "")
    compressed = entry.get("compressed", False)

    raw = base64.b64decode(raw_b64)
    if compressed:
        raw = gzip.decompress(raw)

    # JS modules — keep as text, we'll inline them
    if mime in ("application/javascript", "text/javascript"):
        try:
            js_entries.append((uuid, raw.decode("utf-8")))
        except Exception:
            pass
        data_uri_map[uuid] = f"data:{mime};base64,{base64.b64encode(raw).decode()}"
        continue

    # CSS — keep as text
    if mime == "text/css":
        try:
            css_entries.append((uuid, raw.decode("utf-8")))
        except Exception:
            pass
        data_uri_map[uuid] = f"data:{mime};base64,{base64.b64encode(raw).decode()}"
        continue

    # Fonts
    if mime in ("font/woff2", "font/woff", "font/ttf", "font/otf",
                "application/font-woff2", "application/font-woff",
                "application/x-font-ttf"):
        data_uri = f"data:{mime};base64,{base64.b64encode(raw).decode()}"
        data_uri_map[uuid] = data_uri
        font_entries.append((uuid, data_uri, mime))
        continue

    # Everything else (images, svg, etc.)
    data_uri = f"data:{mime};base64,{base64.b64encode(raw).decode()}"
    data_uri_map[uuid] = data_uri

print(f"  {len(font_entries)} font assets, {len(js_entries)} JS assets, {len(css_entries)} CSS assets")

# ── 5. Replace UUID references in template HTML ────────────────────────────
print("Replacing UUID references in template HTML…")

html = template_html

# UUIDs look like 8-4-4-4-12 hex
UUID_RE = re.compile(
    r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
    re.IGNORECASE
)

replaced = 0
def replace_uuid(m):
    global replaced
    uid = m.group(0)
    if uid in data_uri_map:
        replaced += 1
        return data_uri_map[uid]
    return uid

html = UUID_RE.sub(replace_uuid, html)
print(f"  Replaced {replaced} UUID references")

# ── 6. Detect repeated inline-style patterns ────────────────────────────────
print("Analysing inline style patterns…")

# Collect all style= values
style_values = re.findall(r'style="([^"]*)"', html)

# Background colour patterns
bg_patterns = Counter()
for sv in style_values:
    m = re.search(r'background(?:-color)?:\s*([^;]+)', sv, re.IGNORECASE)
    if m:
        bg_patterns[m.group(1).strip()] += 1

print("  Top background values:")
for val, cnt in bg_patterns.most_common(15):
    print(f"    {cnt:3}x  {val!r}")

# ── 7. Build font-face CSS from manifest fonts ──────────────────────────────
# Try to infer font metadata from UUID usage context or just use generic names
# We'll look at what font names appear in the CSS or HTML
font_families_found = set(re.findall(r"font-family:\s*['\"]?([^;'\"]+)['\"]?", html))
print(f"  Font families in HTML: {font_families_found}")

# Build @font-face blocks
# We don't have name metadata per uuid in manifest, so we scan the CSS entries
fontface_css = ""
for uuid, css_text in css_entries:
    # Extract @font-face blocks from CSS
    faces = re.findall(r'@font-face\s*\{[^}]+\}', css_text, re.DOTALL)
    for face in faces:
        # Replace any uuid src references already done above via data_uri_map
        face_replaced = UUID_RE.sub(lambda m: data_uri_map.get(m.group(0), m.group(0)), face)
        fontface_css += face_replaced + "\n"

if not fontface_css and font_entries:
    # Fallback: generate generic @font-face for each font asset
    for i, (uuid, data_uri, mime) in enumerate(font_entries):
        ext = mime.split("/")[-1].replace("x-font-", "").replace("application/font-", "")
        fontface_css += f"""@font-face {{
  font-family: 'IBM Plex Sans';
  src: url('{data_uri}') format('{ext}');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}}\n"""

# ── 8. Design tokens ────────────────────────────────────────────────────────
DESIGN_TOKENS_CSS = """:root {
  /* Color primitives */
  --color-primary: #003746;
  --color-primary-mid: #177287;
  --color-accent: #A0D6E2;
  --color-accent-light: #CAE8EE;
  --color-white: #FFFFFF;
  --color-bg-page: #F9FAFB;
  --color-bg-surface: #F3F4F6;
  --color-text-secondary: #4B5563;
  --color-border: #E5E7EB;
  --color-border-strong: #D0D5DD;
  --color-gray-dark: #111827;
  --color-success: #00AF59;
  --color-success-dark: #027A48;
  --color-success-bright: #2DDC8E;
  --color-error: #F04438;
  --color-warning: #F7732A;
  --color-warning-light: #FBE7CB;

  /* Semantic aliases */
  --bg-surface: var(--color-bg-surface);
  --bg-page: var(--color-bg-page);
  --bg-card: var(--color-white);
  --text-primary: var(--color-primary);
  --text-secondary: var(--color-accent);
  --text-placeholder: var(--color-text-secondary);
  --border-default: var(--color-border);
  --border-strong: var(--color-border-strong);
  --action-primary: var(--color-primary);
  --action-primary-hover: var(--color-primary-mid);

  /* Spacing */
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;

  /* Border radius */
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-2xl: 20px;

  /* Shadows */
  --shadow-card: 0 0 0 1px rgba(0,0,0,0.04), 0 2px 8px rgba(0,0,0,0.04);
  --shadow-md: 0 2px 4px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.08);
  --shadow-lg: 0 16px 48px rgba(0,55,70,0.16);

  /* Typography */
  --font-base: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'IBM Plex Mono', ui-monospace, monospace;
}
"""

# ── 9. Utility / pattern classes ────────────────────────────────────────────
PATTERN_CSS = """
/* ── Slide base ── */
.slide {
  position: relative;
  width: 100%;
  overflow: hidden;
  box-sizing: border-box;
}
.slide--dark   { background-color: var(--color-primary); color: var(--color-white); }
.slide--light  { background-color: var(--color-bg-page); color: var(--color-primary); }
.slide--white  { background-color: var(--color-white);   color: var(--color-primary); }
.slide--teal   { background-color: var(--color-primary-mid); color: var(--color-white); }

/* ── Slide header block ── */
.slide-header { display: flex; flex-direction: column; gap: 8px; }
.slide-header__eyebrow {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  opacity: 0.6;
}
.slide-header__title {
  font-family: var(--font-base);
  font-weight: 700;
  line-height: 1.15;
}
.slide-header__description {
  font-family: var(--font-base);
  font-weight: 400;
  line-height: 1.5;
  opacity: 0.75;
}

/* ── Cards ── */
.card {
  border-radius: var(--radius-xl);
  border: 1px solid var(--color-border);
  background: var(--color-white);
  box-shadow: var(--shadow-card);
  padding: var(--space-6);
  box-sizing: border-box;
}
.card--dark {
  background: rgba(255,255,255,0.06);
  border-color: rgba(255,255,255,0.12);
  color: var(--color-white);
}
.card--accent {
  background: var(--color-accent-light);
  border-color: var(--color-accent);
}

/* ── Stat grid ── */
.stat-grid {
  display: grid;
  gap: var(--space-6);
}
.stat-grid--2 { grid-template-columns: repeat(2, 1fr); }
.stat-grid--3 { grid-template-columns: repeat(3, 1fr); }
.stat-grid--4 { grid-template-columns: repeat(4, 1fr); }
.stat-item__value {
  font-size: clamp(28px, 4vw, 48px);
  font-weight: 700;
  line-height: 1;
  color: var(--color-primary);
}
.stat-item__label {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}

/* ── Feature list ── */
.feature-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
.feature-list li { display: flex; align-items: flex-start; gap: 10px; font-size: 14px; line-height: 1.5; }
.feature-list li::before {
  content: '';
  flex-shrink: 0;
  width: 18px; height: 18px;
  margin-top: 2px;
  background-color: var(--color-success);
  border-radius: 50%;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' fill='none'%3E%3Cpath d='M2 6l3 3 5-5' stroke='white' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 10px;
}

/* ── Step cards ── */
.step-card { display: flex; align-items: flex-start; gap: 16px; }
.step-card__number {
  flex-shrink: 0;
  width: 36px; height: 36px;
  border-radius: 50%;
  background: var(--color-primary);
  color: var(--color-white);
  font-weight: 700;
  font-size: 15px;
  display: flex; align-items: center; justify-content: center;
}
.step-card__content { flex: 1; }

/* ── Section divider ── */
.section-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  text-align: center;
  gap: 16px;
}
.section-divider__number {
  font-size: clamp(64px, 12vw, 120px);
  font-weight: 800;
  line-height: 1;
  opacity: 0.08;
  color: currentColor;
  position: absolute;
}

/* ── Utility ── */
.text-white   { color: var(--color-white) !important; }
.text-primary { color: var(--color-primary) !important; }
.text-accent  { color: var(--color-accent) !important; }
.bg-dark      { background-color: var(--color-primary) !important; }
.bg-page      { background-color: var(--color-bg-page) !important; }
.font-base    { font-family: var(--font-base); }
.font-mono    { font-family: var(--font-mono); }
"""

# ── 10. Extract <head> content from template HTML ───────────────────────────
# The template might be a full HTML doc or a fragment
if re.search(r'<!DOCTYPE', html, re.IGNORECASE):
    # Full doc — parse and inject our additions into head
    head_match = re.search(r'(<head[^>]*>)(.*?)(</head>)', html, re.DOTALL | re.IGNORECASE)
    body_match = re.search(r'(<body[^>]*>)(.*?)(</body>)', html, re.DOTALL | re.IGNORECASE)
    if head_match and body_match:
        existing_head = head_match.group(2)
        body_open = body_match.group(1)
        body_content = body_match.group(2)
        body_close = body_match.group(3)

        # Remove existing <style> blocks that we'll rebuild
        existing_styles = re.findall(r'<style[^>]*>.*?</style>', existing_head, re.DOTALL)
        for s in existing_styles:
            existing_head = existing_head.replace(s, "")

        # Remove charset/viewport if present — we'll re-add
        existing_head_clean = re.sub(r'<meta\s+charset[^>]*>', '', existing_head)
        existing_head_clean = re.sub(r'<meta\s+name="viewport"[^>]*>', '', existing_head_clean)

        new_head = f"""<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Banamex × Velpay — Presentación</title>
  <style>
{fontface_css}
{DESIGN_TOKENS_CSS}
{PATTERN_CSS}
  </style>
  {existing_head_clean}"""

        output_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  {new_head}
</head>
{body_open}
{body_content}
{body_close}
</html>"""
    else:
        # Fallback — wrap everything
        output_html = build_wrapped(html, fontface_css)
else:
    # Fragment — wrap in full doc
    def build_wrapped(inner, fc):
        return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Banamex × Velpay — Presentación</title>
  <style>
{fc}
{DESIGN_TOKENS_CSS}
{PATTERN_CSS}
  </style>
</head>
<body>
{inner}
</body>
</html>"""
    output_html = build_wrapped(html, fontface_css)

# ── 11. Write output ────────────────────────────────────────────────────────
print(f"Writing output to {DST}…")
with open(DST, "w", encoding="utf-8") as f:
    f.write(output_html)

size_mb = len(output_html.encode("utf-8")) / 1_048_576
print(f"Done. Output size: {size_mb:.1f} MB")
print(f"File: {DST}")
