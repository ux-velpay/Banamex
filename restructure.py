#!/usr/bin/env python3
import re

with open('/Users/ivonnegonzalez/Desktop/Banamex/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract sections by depth-tracking
def extract_sections(html):
    sections = {}
    pos = 0
    while True:
        start = html.find('<section ', pos)
        if start == -1:
            break
        # Get the data-label
        label_match = re.search(r'data-label="([^"]+)"', html[start:start+200])
        if not label_match:
            pos = start + 1
            continue
        label = label_match.group(1)
        # Depth tracking
        depth = 0
        i = start
        while i < len(html):
            if html[i:i+9] == '<section ':
                depth += 1
                i += 9
            elif html[i:i+10] == '</section>':
                depth -= 1
                if depth == 0:
                    end = i + 10
                    sections[label] = html[start:end]
                    break
                i += 10
            else:
                i += 1
        pos = start + 1
    return sections

sections = extract_sections(html)

# Modification helpers
def replace_eyebrow(section_html, new_text):
    # Find short uppercase span/div near the top (eyebrow text)
    # Try to match spans with letter-spacing or uppercase styling
    patterns = [
        r'(<span[^>]*(?:letter-spacing|uppercase|eyebrow)[^>]*>)([^<]+)(</span>)',
        r'(<div[^>]*(?:letter-spacing|uppercase|eyebrow)[^>]*>)([^<]+)(</div>)',
    ]
    for pat in patterns:
        m = re.search(pat, section_html[:2000], re.IGNORECASE)
        if m:
            return section_html[:m.start(2)] + new_text + section_html[m.end(2):]
    # Fallback: find first short text in a span/div
    m = re.search(r'(<(?:span|div)[^>]*>)([A-Z][A-Z ·]+)(</(?:span|div)>)', section_html[:2000])
    if m:
        return section_html[:m.start(2)] + new_text + section_html[m.end(2):]
    return section_html

def replace_heading(section_html, new_text):
    for tag in ['h1', 'h2', 'h3']:
        m = re.search(r'(<' + tag + r'[^>]*>)(.*?)(</' + tag + r'>)', section_html, re.DOTALL)
        if m:
            return section_html[:m.start(2)] + new_text + section_html[m.end(2):]
    return section_html

# Modify Slide 2 (Panorama)
slide2 = sections.get('Panorama', '')
if slide2:
    slide2 = slide2.replace('data-label="Panorama"', 'data-label="La plataforma de cobro"')
    slide2 = replace_eyebrow(slide2, 'Velpay · Banamex')
    slide2 = replace_heading(slide2, 'Una plataforma, todos tus canales de cobro')

# Modify Slide 7 (Portales)
slide7 = sections.get('Portales', '')
if slide7:
    slide7 = slide7.replace('data-label="Portales"', 'data-label="Assistant + Backoffice"')
    slide7 = replace_eyebrow(slide7, 'Gestión')
    slide7 = replace_heading(slide7, 'Assistant comercial y backoffice')

# New slides HTML
slide3_new = '''<section data-label="4 canales disponibles" style="font-family:'IBM Plex Sans',sans-serif;background:#F9FAFB;color:#003746;padding:80px 110px;display:flex;flex-direction:column;box-sizing:border-box;overflow:hidden;">
  <div style="display:flex;flex-direction:column;gap:12px;max-width:1280px;">
    <span style="font-size:24px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:#177287;">Velpay</span>
    <h2 style="font-size:60px;line-height:1.08;letter-spacing:-0.025em;font-weight:700;margin:0;">4 canales disponibles</h2>
    <p style="font-size:29px;line-height:1.45;color:#4B5563;margin:8px 0 0;">Una sola integración para cobrar en cualquier escenario</p>
  </div>
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:48px;">
    <div style="background:#fff;border:1px solid #E5E7EB;border-radius:18px;padding:40px;display:flex;flex-direction:column;">
      <span style="width:60px;height:60px;border-radius:14px;background:#CAE8EE;display:flex;align-items:center;justify-content:center;margin-bottom:24px;">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect x="4" y="8" width="24" height="16" rx="3" stroke="#177287" stroke-width="2.2"/><path d="M4 13h24" stroke="#177287" stroke-width="2.2"/><rect x="8" y="18" width="6" height="3" rx="1" fill="#177287"/></svg>
      </span>
      <div style="font-size:30px;font-weight:700;letter-spacing:-0.01em;margin-bottom:12px;">Terminal TPV</div>
      <p style="font-size:25px;line-height:1.5;color:#4B5563;margin:0;">Terminal física con conectividad WiFi, 4G y Bluetooth para cobros presenciales</p>
    </div>
    <div style="background:#fff;border:1px solid #E5E7EB;border-radius:18px;padding:40px;display:flex;flex-direction:column;">
      <span style="width:60px;height:60px;border-radius:14px;background:#CAE8EE;display:flex;align-items:center;justify-content:center;margin-bottom:24px;">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect x="10" y="3" width="12" height="26" rx="3" stroke="#177287" stroke-width="2.2"/><circle cx="16" cy="24" r="1.5" fill="#177287"/><path d="M13 7h6" stroke="#177287" stroke-width="2" stroke-linecap="round"/></svg>
      </span>
      <div style="font-size:30px;font-weight:700;letter-spacing:-0.01em;margin-bottom:12px;">Tap to Phone</div>
      <p style="font-size:25px;line-height:1.5;color:#4B5563;margin:0;">Convierte cualquier smartphone Android en terminal de cobro NFC</p>
    </div>
    <div style="background:#fff;border:1px solid #E5E7EB;border-radius:18px;padding:40px;display:flex;flex-direction:column;">
      <span style="width:60px;height:60px;border-radius:14px;background:#CAE8EE;display:flex;align-items:center;justify-content:center;margin-bottom:24px;">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect x="3" y="8" width="26" height="18" rx="3" stroke="#177287" stroke-width="2.2"/><path d="M10 8V6a6 6 0 0 1 12 0v2" stroke="#177287" stroke-width="2.2"/><circle cx="16" cy="17" r="3" stroke="#177287" stroke-width="2"/></svg>
      </span>
      <div style="font-size:30px;font-weight:700;letter-spacing:-0.01em;margin-bottom:12px;">Botón de pago</div>
      <p style="font-size:25px;line-height:1.5;color:#4B5563;margin:0;">Link y widget embebible para cobros en línea sin redirigir al usuario</p>
    </div>
    <div style="background:#fff;border:1px solid #E5E7EB;border-radius:18px;padding:40px;display:flex;flex-direction:column;">
      <span style="width:60px;height:60px;border-radius:14px;background:#CAE8EE;display:flex;align-items:center;justify-content:center;margin-bottom:24px;">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="12" stroke="#177287" stroke-width="2.2"/><path d="M16 10v6l4 2" stroke="#177287" stroke-width="2.2" stroke-linecap="round"/></svg>
      </span>
      <div style="font-size:30px;font-weight:700;letter-spacing:-0.01em;margin-bottom:12px;">Banamex Pay</div>
      <p style="font-size:25px;line-height:1.5;color:#4B5563;margin:0;">Cobro por referencia en efectivo en más de 9,000 sucursales Banamex</p>
    </div>
  </div>
</section>'''

slide4_new = '''<section data-label="Capítulo 2 · Los productos" style="font-family:'IBM Plex Sans',sans-serif;background:#003746;color:#fff;padding:92px 110px;display:flex;flex-direction:column;justify-content:center;box-sizing:border-box;overflow:hidden;position:relative;">
  <div style="position:absolute;left:0;top:0;bottom:0;width:8px;background:#A0D6E2;"></div>
  <div style="font-size:200px;font-weight:700;letter-spacing:-0.04em;color:rgba(160,214,226,0.14);line-height:1;margin-bottom:-10px;">02</div>
  <div style="font-size:24px;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:#A0D6E2;margin-bottom:18px;">Capítulo 2</div>
  <h2 style="font-size:88px;line-height:1.02;letter-spacing:-0.03em;font-weight:700;margin:0 0 24px;">Los productos</h2>
  <p style="font-size:32px;line-height:1.45;color:#CAE8EE;margin:0;max-width:1000px;">Conoce en detalle cada canal de cobro y sus capacidades técnicas</p>
</section>'''

slide10_new = '''<section data-label="Capítulo 3 · Casos de uso" style="font-family:'IBM Plex Sans',sans-serif;background:#003746;color:#fff;padding:92px 110px;display:flex;flex-direction:column;justify-content:center;box-sizing:border-box;overflow:hidden;position:relative;">
  <div style="position:absolute;left:0;top:0;bottom:0;width:8px;background:#A0D6E2;"></div>
  <div style="font-size:200px;font-weight:700;letter-spacing:-0.04em;color:rgba(160,214,226,0.14);line-height:1;margin-bottom:-10px;">03</div>
  <div style="font-size:24px;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:#A0D6E2;margin-bottom:18px;">Capítulo 3</div>
  <h2 style="font-size:88px;line-height:1.02;letter-spacing:-0.03em;font-weight:700;margin:0 0 24px;">Casos de uso</h2>
  <p style="font-size:32px;line-height:1.45;color:#CAE8EE;margin:0;max-width:1000px;">Industrias y escenarios donde Velpay genera valor inmediato</p>
</section>'''

slide11_new = '''<section data-label="Casos de uso · Industrias" style="font-family:'IBM Plex Sans',sans-serif;background:#F9FAFB;color:#003746;padding:80px 110px;display:flex;flex-direction:column;box-sizing:border-box;overflow:hidden;">
  <div style="display:flex;flex-direction:column;gap:12px;max-width:1280px;">
    <span style="font-size:24px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:#177287;">Casos de uso</span>
    <h2 style="font-size:60px;line-height:1.08;letter-spacing:-0.025em;font-weight:700;margin:0;">E-commerce, créditos, servicios, boletos</h2>
    <p style="font-size:29px;line-height:1.45;color:#4B5563;margin:8px 0 0;">Velpay se adapta a tu modelo de negocio</p>
  </div>
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:48px;">
    <div style="background:#fff;border:1px solid #E5E7EB;border-radius:18px;padding:40px;display:flex;flex-direction:column;">
      <span style="width:60px;height:60px;border-radius:14px;background:#CAE8EE;display:flex;align-items:center;justify-content:center;margin-bottom:24px;">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><path d="M4 6h3l3 14h14l2-10H9" stroke="#177287" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="13" cy="26" r="2" fill="#177287"/><circle cx="23" cy="26" r="2" fill="#177287"/></svg>
      </span>
      <div style="font-size:30px;font-weight:700;letter-spacing:-0.01em;margin-bottom:12px;">E-commerce</div>
      <p style="font-size:25px;line-height:1.5;color:#4B5563;margin:0;">Cobra el carrito sin redirigir al usuario con el widget embebido</p>
    </div>
    <div style="background:#fff;border:1px solid #E5E7EB;border-radius:18px;padding:40px;display:flex;flex-direction:column;">
      <span style="width:60px;height:60px;border-radius:14px;background:#CAE8EE;display:flex;align-items:center;justify-content:center;margin-bottom:24px;">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect x="5" y="8" width="22" height="16" rx="3" stroke="#177287" stroke-width="2.2"/><path d="M5 13h22M10 18h4" stroke="#177287" stroke-width="2" stroke-linecap="round"/></svg>
      </span>
      <div style="font-size:30px;font-weight:700;letter-spacing:-0.01em;margin-bottom:12px;">Créditos</div>
      <p style="font-size:25px;line-height:1.5;color:#4B5563;margin:0;">Recibe el pago de mensualidades en efectivo o tarjeta con referencia única</p>
    </div>
    <div style="background:#fff;border:1px solid #E5E7EB;border-radius:18px;padding:40px;display:flex;flex-direction:column;">
      <span style="width:60px;height:60px;border-radius:14px;background:#CAE8EE;display:flex;align-items:center;justify-content:center;margin-bottom:24px;">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><path d="M6 16a10 10 0 1 0 20 0 10 10 0 0 0-20 0z" stroke="#177287" stroke-width="2.2"/><path d="M16 10v6l3 3" stroke="#177287" stroke-width="2.2" stroke-linecap="round"/></svg>
      </span>
      <div style="font-size:30px;font-weight:700;letter-spacing:-0.01em;margin-bottom:12px;">Servicios</div>
      <p style="font-size:25px;line-height:1.5;color:#4B5563;margin:0;">Agua, luz, telefonía — referencia única por cliente, cobro multicanal</p>
    </div>
    <div style="background:#fff;border:1px solid #E5E7EB;border-radius:18px;padding:40px;display:flex;flex-direction:column;">
      <span style="width:60px;height:60px;border-radius:14px;background:#CAE8EE;display:flex;align-items:center;justify-content:center;margin-bottom:24px;">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect x="4" y="10" width="24" height="14" rx="2" stroke="#177287" stroke-width="2.2"/><path d="M10 10V8a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2M12 17h8" stroke="#177287" stroke-width="2" stroke-linecap="round"/></svg>
      </span>
      <div style="font-size:30px;font-weight:700;letter-spacing:-0.01em;margin-bottom:12px;">Boletos</div>
      <p style="font-size:25px;line-height:1.5;color:#4B5563;margin:0;">Vende entradas y cobra en mostrador o en línea con la misma integración</p>
    </div>
  </div>
</section>'''

slide13_new = '''<section data-label="Capítulo 4 · Integración" style="font-family:'IBM Plex Sans',sans-serif;background:#003746;color:#fff;padding:92px 110px;display:flex;flex-direction:column;justify-content:center;box-sizing:border-box;overflow:hidden;position:relative;">
  <div style="position:absolute;left:0;top:0;bottom:0;width:8px;background:#A0D6E2;"></div>
  <div style="font-size:200px;font-weight:700;letter-spacing:-0.04em;color:rgba(160,214,226,0.14);line-height:1;margin-bottom:-10px;">04</div>
  <div style="font-size:24px;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:#A0D6E2;margin-bottom:18px;">Capítulo 4</div>
  <h2 style="font-size:88px;line-height:1.02;letter-spacing:-0.03em;font-weight:700;margin:0 0 24px;">Integración</h2>
  <p style="font-size:32px;line-height:1.45;color:#CAE8EE;margin:0;max-width:1000px;">De la firma del contrato a producción en 5 días hábiles</p>
</section>'''

slide14_new = '''<section data-label="Proceso de alta · 5 días" style="font-family:'IBM Plex Sans',sans-serif;background:#F9FAFB;color:#003746;padding:80px 110px;display:flex;flex-direction:column;box-sizing:border-box;overflow:hidden;">
  <div style="display:flex;flex-direction:column;gap:12px;max-width:1280px;">
    <span style="font-size:24px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:#177287;">Integración</span>
    <h2 style="font-size:60px;line-height:1.08;letter-spacing:-0.025em;font-weight:700;margin:0;">Proceso de alta en 5 días</h2>
    <p style="font-size:29px;line-height:1.45;color:#4B5563;margin:8px 0 0;">Un proceso ágil y guiado para que estés en producción rápido</p>
  </div>
  <div style="flex:1;display:flex;align-items:center;margin-top:48px;gap:0;">
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;position:relative;">
      <div style="width:64px;height:64px;border-radius:50%;background:#003746;color:#fff;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700;z-index:1;">1</div>
      <div style="position:absolute;top:32px;left:50%;right:-50%;height:3px;background:#A0D6E2;z-index:0;"></div>
      <div style="margin-top:20px;text-align:center;padding:0 8px;">
        <div style="font-size:20px;font-weight:700;color:#177287;margin-bottom:6px;">Día 1</div>
        <div style="font-size:22px;font-weight:600;margin-bottom:8px;">Firma de contrato</div>
        <p style="font-size:20px;line-height:1.4;color:#4B5563;margin:0;">Alta comercial y validación de datos</p>
      </div>
    </div>
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;position:relative;">
      <div style="width:64px;height:64px;border-radius:50%;background:#003746;color:#fff;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700;z-index:1;">2</div>
      <div style="position:absolute;top:32px;left:-50%;right:-50%;height:3px;background:#A0D6E2;z-index:0;"></div>
      <div style="margin-top:20px;text-align:center;padding:0 8px;">
        <div style="font-size:20px;font-weight:700;color:#177287;margin-bottom:6px;">Día 2</div>
        <div style="font-size:22px;font-weight:600;margin-bottom:8px;">Credenciales sandbox</div>
        <p style="font-size:20px;line-height:1.4;color:#4B5563;margin:0;">Acceso al ambiente de pruebas</p>
      </div>
    </div>
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;position:relative;">
      <div style="width:64px;height:64px;border-radius:50%;background:#003746;color:#fff;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700;z-index:1;">3</div>
      <div style="position:absolute;top:32px;left:-50%;right:-50%;height:3px;background:#A0D6E2;z-index:0;"></div>
      <div style="margin-top:20px;text-align:center;padding:0 8px;">
        <div style="font-size:20px;font-weight:700;color:#177287;margin-bottom:6px;">Día 3</div>
        <div style="font-size:22px;font-weight:600;margin-bottom:8px;">Integración y pruebas</div>
        <p style="font-size:20px;line-height:1.4;color:#4B5563;margin:0;">Desarrollo con soporte técnico</p>
      </div>
    </div>
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;position:relative;">
      <div style="width:64px;height:64px;border-radius:50%;background:#003746;color:#fff;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700;z-index:1;">4</div>
      <div style="position:absolute;top:32px;left:-50%;right:-50%;height:3px;background:#A0D6E2;z-index:0;"></div>
      <div style="margin-top:20px;text-align:center;padding:0 8px;">
        <div style="font-size:20px;font-weight:700;color:#177287;margin-bottom:6px;">Día 4</div>
        <div style="font-size:22px;font-weight:600;margin-bottom:8px;">Revisión técnica</div>
        <p style="font-size:20px;line-height:1.4;color:#4B5563;margin:0;">Go / no-go con equipo Velpay</p>
      </div>
    </div>
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;position:relative;">
      <div style="width:64px;height:64px;border-radius:50%;background:#00AF59;color:#fff;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700;z-index:1;">5</div>
      <div style="position:absolute;top:32px;left:-50%;right:50%;height:3px;background:#A0D6E2;z-index:0;"></div>
      <div style="margin-top:20px;text-align:center;padding:0 8px;">
        <div style="font-size:20px;font-weight:700;color:#00AF59;margin-bottom:6px;">Día 5</div>
        <div style="font-size:22px;font-weight:600;margin-bottom:8px;">Producción activa</div>
        <p style="font-size:20px;line-height:1.4;color:#4B5563;margin:0;">Transacciones reales desde el primer día</p>
      </div>
    </div>
  </div>
</section>'''

slide15_new = '''<section data-label="API · Webhooks · Sandbox" style="font-family:'IBM Plex Sans',sans-serif;background:#F9FAFB;color:#003746;padding:80px 110px;display:flex;flex-direction:column;box-sizing:border-box;overflow:hidden;">
  <div style="display:flex;flex-direction:column;gap:12px;max-width:1280px;">
    <span style="font-size:24px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:#177287;">Integración técnica</span>
    <h2 style="font-size:60px;line-height:1.08;letter-spacing:-0.025em;font-weight:700;margin:0;">API, webhooks y sandbox</h2>
    <p style="font-size:29px;line-height:1.45;color:#4B5563;margin:8px 0 0;">Estándares de la industria para una integración sin fricciones</p>
  </div>
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;margin-top:48px;">
    <div style="background:#fff;border:1px solid #E5E7EB;border-radius:18px;padding:40px;display:flex;flex-direction:column;">
      <span style="width:60px;height:60px;border-radius:14px;background:#CAE8EE;display:flex;align-items:center;justify-content:center;margin-bottom:24px;">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><path d="M8 10l-4 6 4 6M24 10l4 6-4 6M18 6l-4 20" stroke="#177287" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </span>
      <div style="font-size:30px;font-weight:700;letter-spacing:-0.01em;margin-bottom:12px;">API REST</div>
      <p style="font-size:23px;line-height:1.5;color:#4B5563;margin:0;">Endpoints documentados en OpenAPI 3.0, autenticación OAuth 2.0 con tokens de corta duración</p>
    </div>
    <div style="background:#fff;border:1px solid #E5E7EB;border-radius:18px;padding:40px;display:flex;flex-direction:column;">
      <span style="width:60px;height:60px;border-radius:14px;background:#CAE8EE;display:flex;align-items:center;justify-content:center;margin-bottom:24px;">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><path d="M6 16c0-5.5 4.5-10 10-10s10 4.5 10 10" stroke="#177287" stroke-width="2.2" stroke-linecap="round"/><path d="M16 6v4M26 16h-4M6 16H2M16 22v4" stroke="#177287" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="3" fill="#177287"/></svg>
      </span>
      <div style="font-size:30px;font-weight:700;letter-spacing:-0.01em;margin-bottom:12px;">Webhooks</div>
      <p style="font-size:23px;line-height:1.5;color:#4B5563;margin:0;">Eventos firmados con HMAC-SHA256, reintentos automáticos en 3 intentos con backoff exponencial</p>
    </div>
    <div style="background:#fff;border:1px solid #E5E7EB;border-radius:18px;padding:40px;display:flex;flex-direction:column;">
      <span style="width:60px;height:60px;border-radius:14px;background:#CAE8EE;display:flex;align-items:center;justify-content:center;margin-bottom:24px;">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect x="4" y="6" width="24" height="20" rx="3" stroke="#177287" stroke-width="2.2"/><path d="M4 12h24M10 18h4M10 22h6" stroke="#177287" stroke-width="2" stroke-linecap="round"/></svg>
      </span>
      <div style="font-size:30px;font-weight:700;letter-spacing:-0.01em;margin-bottom:12px;">Sandbox</div>
      <p style="font-size:23px;line-height:1.5;color:#4B5563;margin:0;">Ambiente idéntico a producción con tarjetas y referencias de prueba incluidas desde el día 2</p>
    </div>
  </div>
</section>'''

slide16_new = '''<section data-label="SLA · Monitoreo · Conciliación" style="font-family:'IBM Plex Sans',sans-serif;background:#F9FAFB;color:#003746;padding:80px 110px;display:flex;flex-direction:column;box-sizing:border-box;overflow:hidden;">
  <div style="display:flex;flex-direction:column;gap:12px;max-width:1280px;">
    <span style="font-size:24px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:#177287;">Operación</span>
    <h2 style="font-size:60px;line-height:1.08;letter-spacing:-0.025em;font-weight:700;margin:0;">SLA, monitoreo y conciliación</h2>
    <p style="font-size:29px;line-height:1.45;color:#4B5563;margin:8px 0 0;">Infraestructura de clase enterprise con visibilidad total</p>
  </div>
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;margin-top:40px;">
    <div style="background:#003746;border-radius:18px;padding:48px 40px;display:flex;flex-direction:column;align-items:flex-start;">
      <div style="font-size:72px;font-weight:700;letter-spacing:-0.03em;color:#A0D6E2;line-height:1;margin-bottom:16px;">99.95%</div>
      <div style="font-size:28px;font-weight:700;color:#fff;margin-bottom:10px;">Uptime garantizado</div>
      <p style="font-size:22px;line-height:1.5;color:#CAE8EE;margin:0;">SLA contractual con penalizaciones por incumplimiento</p>
    </div>
    <div style="background:#003746;border-radius:18px;padding:48px 40px;display:flex;flex-direction:column;align-items:flex-start;">
      <div style="font-size:72px;font-weight:700;letter-spacing:-0.03em;color:#A0D6E2;line-height:1;margin-bottom:16px;">24/7</div>
      <div style="font-size:28px;font-weight:700;color:#fff;margin-bottom:10px;">Monitoreo continuo</div>
      <p style="font-size:22px;line-height:1.5;color:#CAE8EE;margin:0;">Alertas en tiempo real con escalamiento automático</p>
    </div>
    <div style="background:#003746;border-radius:18px;padding:48px 40px;display:flex;flex-direction:column;align-items:flex-start;">
      <div style="font-size:72px;font-weight:700;letter-spacing:-0.03em;color:#2DDC8E;line-height:1;margin-bottom:16px;">D+1</div>
      <div style="font-size:28px;font-weight:700;color:#fff;margin-bottom:10px;">Conciliación automática</div>
      <p style="font-size:22px;line-height:1.5;color:#CAE8EE;margin:0;">Reporte de transacciones al día siguiente sin intervención manual</p>
    </div>
  </div>
  <div style="margin-top:32px;background:#fff;border:1px solid #E5E7EB;border-radius:14px;padding:28px 36px;">
    <p style="font-size:24px;line-height:1.5;color:#4B5563;margin:0;"><strong style="color:#003746;">Soporte técnico dedicado:</strong> Cuenta con un equipo de ingenieros especialistas disponible durante la integración y en operación regular, con canales prioritarios para incidentes críticos.</p>
  </div>
</section>'''

slide17_new = '''<section data-label="Capítulo 5 · Cierre" style="font-family:'IBM Plex Sans',sans-serif;background:#003746;color:#fff;padding:92px 110px;display:flex;flex-direction:column;justify-content:center;box-sizing:border-box;overflow:hidden;position:relative;">
  <div style="position:absolute;left:0;top:0;bottom:0;width:8px;background:#A0D6E2;"></div>
  <div style="font-size:200px;font-weight:700;letter-spacing:-0.04em;color:rgba(160,214,226,0.14);line-height:1;margin-bottom:-10px;">05</div>
  <div style="font-size:24px;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:#A0D6E2;margin-bottom:18px;">Capítulo 5</div>
  <h2 style="font-size:88px;line-height:1.02;letter-spacing:-0.03em;font-weight:700;margin:0 0 24px;">Cierre</h2>
  <p style="font-size:32px;line-height:1.45;color:#CAE8EE;margin:0;max-width:1000px;">Por qué Velpay es la decisión correcta para Banamex</p>
</section>'''

slide19_new = '''<section data-label="Siguiente paso" style="font-family:'IBM Plex Sans',sans-serif;background:#003746;color:#fff;padding:92px 110px;display:flex;flex-direction:column;justify-content:center;box-sizing:border-box;overflow:hidden;position:relative;">
  <div style="position:absolute;left:0;top:0;bottom:0;width:8px;background:#A0D6E2;"></div>
  <div style="display:flex;flex-direction:column;align-items:center;text-align:center;gap:48px;max-width:1100px;margin:0 auto;">
    <div>
      <h2 style="font-size:88px;line-height:1.02;letter-spacing:-0.03em;font-weight:700;margin:0 0 20px;">¿Listos para integrar?</h2>
      <p style="font-size:32px;line-height:1.45;color:#CAE8EE;margin:0;">Tres pasos para arrancar hoy mismo</p>
    </div>
    <div style="display:flex;gap:32px;width:100%;">
      <div style="flex:1;background:rgba(160,214,226,0.12);border:1px solid rgba(160,214,226,0.3);border-radius:18px;padding:40px;text-align:left;">
        <div style="font-size:48px;font-weight:700;color:#A0D6E2;margin-bottom:12px;">1.</div>
        <div style="font-size:28px;font-weight:700;margin-bottom:8px;">Firma el contrato hoy</div>
        <p style="font-size:22px;line-height:1.5;color:#CAE8EE;margin:0;">Alta comercial en menos de 24 horas</p>
      </div>
      <div style="flex:1;background:rgba(160,214,226,0.12);border:1px solid rgba(160,214,226,0.3);border-radius:18px;padding:40px;text-align:left;">
        <div style="font-size:48px;font-weight:700;color:#A0D6E2;margin-bottom:12px;">2.</div>
        <div style="font-size:28px;font-weight:700;margin-bottom:8px;">Recibe tus credenciales en 48h</div>
        <p style="font-size:22px;line-height:1.5;color:#CAE8EE;margin:0;">Acceso a sandbox y documentación técnica</p>
      </div>
      <div style="flex:1;background:rgba(160,214,226,0.12);border:1px solid rgba(160,214,226,0.3);border-radius:18px;padding:40px;text-align:left;">
        <div style="font-size:48px;font-weight:700;color:#2DDC8E;margin-bottom:12px;">3.</div>
        <div style="font-size:28px;font-weight:700;margin-bottom:8px;">Primeras transacciones en 5 días</div>
        <p style="font-size:22px;line-height:1.5;color:#CAE8EE;margin:0;">De sandbox a producción sin fricciones</p>
      </div>
    </div>
    <div style="display:flex;gap:48px;align-items:center;padding:32px 48px;background:rgba(255,255,255,0.06);border-radius:16px;width:100%;justify-content:center;">
      <div style="text-align:center;">
        <div style="font-size:20px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#A0D6E2;margin-bottom:6px;">Correo</div>
        <div style="font-size:26px;font-weight:600;">integraciones@velpay.mx</div>
      </div>
      <div style="width:1px;height:48px;background:rgba(160,214,226,0.3);"></div>
      <div style="text-align:center;">
        <div style="font-size:20px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#A0D6E2;margin-bottom:6px;">Teléfono</div>
        <div style="font-size:26px;font-weight:600;">+52 55 1234 5678</div>
      </div>
      <div style="width:1px;height:48px;background:rgba(160,214,226,0.3);"></div>
      <div style="text-align:center;">
        <div style="font-size:20px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#A0D6E2;margin-bottom:6px;">Web</div>
        <div style="font-size:26px;font-weight:600;">velpay.mx/banamex</div>
      </div>
    </div>
    <div style="opacity:0.5;">
      <svg width="120" height="40" viewBox="0 0 120 40" fill="none"><rect width="120" height="40" rx="8" fill="white" fill-opacity="0.15"/><text x="60" y="27" text-anchor="middle" fill="white" font-size="18" font-weight="700" font-family="IBM Plex Sans, sans-serif">BANAMEX</text></svg>
    </div>
  </div>
</section>'''

# Build 19 slides in order
ordered_slides = [
    sections.get('Portada', '<!-- PORTADA NOT FOUND -->'),           # 1
    slide2 if slide2 else '<!-- PANORAMA NOT FOUND -->',            # 2
    slide3_new,                                                       # 3
    slide4_new,                                                       # 4
    sections.get('Terminal TPV', '<!-- TERMINAL TPV NOT FOUND -->'), # 5
    sections.get('Tap to Phone', '<!-- TAP TO PHONE NOT FOUND -->'), # 6
    slide7 if slide7 else '<!-- PORTALES NOT FOUND -->',             # 7
    sections.get('Botón de pago', '<!-- BOTON NOT FOUND -->'),       # 8
    sections.get('Qué es Banamex Pay', '<!-- BANAMEX PAY NOT FOUND -->'), # 9
    slide10_new,                                                      # 10
    slide11_new,                                                      # 11
    sections.get('Cómo funciona', '<!-- COMO FUNCIONA NOT FOUND -->'), # 12
    slide13_new,                                                      # 13
    slide14_new,                                                      # 14
    slide15_new,                                                      # 15
    slide16_new,                                                      # 16
    slide17_new,                                                      # 17
    sections.get('Propuesta de valor', '<!-- PROPUESTA NOT FOUND -->'), # 18
    slide19_new,                                                      # 19
]

new_sections_block = '\n\n'.join(ordered_slides)

# Find the block from first <section to last </section>
first_section = html.find('<section ')
last_section_end = html.rfind('</section>') + len('</section>')

if first_section == -1 or last_section_end == -1:
    print("ERROR: Could not find section boundaries")
    exit(1)

new_html = html[:first_section] + new_sections_block + html[last_section_end:]

with open('/Users/ivonnegonzalez/Desktop/Banamex/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("SUCCESS: index.html restructured with 19 slides")

# Report which slides were found/missing
for label in ['Portada', 'Panorama', 'Cómo funciona', 'Terminal TPV', 'Tap to Phone', 'Portales', 'Botón de pago', 'Qué es Banamex Pay', 'Propuesta de valor']:
    status = "FOUND" if label in sections else "MISSING"
    print(f"  {status}: {label}")
