# Design Tokens — Human Reference

> ⚠️ **Este documento es solo orientación para humanos.**
> La fuente de verdad son los archivos JSON:
> `color-primitives.json`, `color-semantic.json`, `layout-tokens.json`,
> `typography-primitives.json`, `typography-semantic.json`.
>
> Al implementar en código o Storybook, leer siempre los JSON directamente.
> Este documento puede estar desactualizado respecto a los JSON.

---

## Spacing Scale (8pt Grid)

```css
--space-0:   0px;
--space-px:  1px;
--space-0-5: 2px;
--space-1:   4px;   /* fine-tuning inside components */
--space-1-5: 6px;
--space-2:   8px;   /* tight spacing, icon gaps, label-to-input gap */
--space-3:   12px;  /* label-to-input gap (alternativo) */
--space-4:   16px;  /* default internal padding */
--space-5:   20px;  /* compact section spacing */
--space-6:   24px;  /* card padding, form field gaps */
--space-7:   28px;
--space-8:   32px;  /* section spacing */
--space-10:  40px;  /* large section gaps */
--space-12:  48px;  /* section dividers */
--space-16:  64px;  /* page section spacing */
--space-20:  80px;  /* hero spacing */
--space-24:  96px;  /* major page divisions */
```

**Rule:** Internal spacing ≤ external spacing. Always.

---

## Color Scales

### Neutral

```css
/* neutral */
--neutral-0:   #FFFFFF;  /* white, card/input backgrounds — intencional */
--neutral-50:  #F9FAFB;  /* page background */
--neutral-100: #F3F4F6;  /* surface background */

/* gray */
--gray-50:  #E5E7EB;  /* borders, dividers */
--gray-100: #D0D5DD;  /* strong borders, disabled elements */
--gray-200: #6B7280;  /* disabled text */
--gray-300: #4B5563;  /* placeholder text */
--gray-400: #374151;  /* secondary text */
--gray-500: #111827;  /* primary text — usar text.primary, no hardcodear */
```

### Brand (Purple) — 8 stops

```css
--purple-50:  #F4F3FF;  /* info badge bg, hover backgrounds suaves */
--purple-100: #E8E3FB;  /* tints decorativos */
--purple-200: #D1C7F6;  /* tints decorativos */
--purple-300: #B5A4F0;  /* chart.series-2 */
--purple-400: #9179EA;  /* chart.series-3 */
--purple-500: #754BF1;  /* CTAs, links, focus rings — acento primario */
--purple-600: #6844D4;  /* hover de primary y secondary */
--purple-700: #2D006D;  /* secondary default, info badge fg, high-emphasis */
```

### Status Colors

```css
/* success */
--green-50:  #027A48;  /* foreground: texto, iconos */
--green-100: #E8FFF4;  /* background: badges, alerts */

/* error */
--red-50:  #F04438;  /* foreground: texto, iconos */
--red-100: #FFDFDF;  /* background: badges, alerts */

/* warning */
--yellow-50:  #F7B500;  /* foreground: texto, iconos */
--yellow-100: #FFF7E0;  /* background: badges, alerts */

/* alert */
--orange-50:  #F7732A;  /* foreground: texto, iconos */
--orange-100: #FBE7CB;  /* background: badges, alerts */
```

---

## Semantic Color Tokens

### Backgrounds
```css
--bg-surface: #F3F4F6;   /* neutral.100 */
--bg-page:    #F9FAFB;   /* neutral.50 */
--bg-card:    #FFFFFF;   /* neutral.0 */
--bg-input:   #FFFFFF;   /* neutral.0 */
--bg-tooltip: #111827;   /* gray.500 — token dedicado */
```

### Text
```css
--text-primary:     #111827;  /* gray.500 — gris muy oscuro, NO black puro */
--text-secondary:   #374151;  /* gray.400 */
--text-placeholder: #4B5563;  /* gray.300 */
--text-disabled:    #6B7280;  /* gray.200 */
--text-link:        #754BF1;  /* purple.500 — 4.6:1 sobre blanco, pasa AA */
```

### Borders
```css
--border-default: #E5E7EB;  /* gray.50 */
--border-strong:  #D0D5DD;  /* gray.100 */
--border-focus:   #754BF1;  /* purple.500 */
--border-error:   #F04438;  /* red.50 */
--border-success: #027A48;  /* green.50 */
```

### Actions
```css
--action-primary:              #754BF1;  /* purple.500 */
--action-primary-hover:        #6844D4;  /* purple.600 */
--action-primary-text:         #FFFFFF;
--action-secondary:            #2D006D;  /* purple.700 — default alta prominencia */
--action-secondary-hover:      #6844D4;  /* purple.600 — aclara en hover intencionalmente */
--action-secondary-text:       #FFFFFF;
--action-secondary-text-hover: #FFFFFF;  /* 5.2:1 sobre purple.600, pasa AA */
--action-tertiary:             #FFFFFF;
--action-tertiary-hover:       #F9FAFB;
--action-tertiary-border:      #D0D5DD;
--action-tertiary-border-hover:#6B7280;
--action-tertiary-text:        #111827;
--action-disabled:             #D0D5DD;
--action-disabled-text:        #6B7280;
```

### Status (siempre usar el par fg + bg)
```css
--status-success:    #027A48;  /* fg */   --status-success-bg: #E8FFF4;
--status-error:      #F04438;  /* fg */   --status-error-bg:   #FFDFDF;
--status-warning:    #F7B500;  /* fg */   --status-warning-bg: #FFF7E0;
--status-alert:      #F7732A;  /* fg */   --status-alert-bg:   #FBE7CB;
--status-info:       #2D006D;  /* fg — purple.700, 9.5:1 sobre purple.50, pasa AAA */
--status-info-bg:    #F4F3FF;
```

### Chart
```css
--chart-series-1:    #754BF1;  /* purple.500 */
--chart-series-2:    #B5A4F0;  /* purple.300 */
--chart-series-3:    #9179EA;  /* purple.400 */
--chart-reference:   #D0D5DD;  /* gray.100 */
--chart-fill-opacity: 0.08;
--chart-axis:        #4B5563;  /* gray.300 */
--chart-tooltip-bg:  #FFFFFF;
```

---

## Type Scales

### Tamaños disponibles
```css
--font-size-11: 11px;  /* badges, overline, captions */
--font-size-12: 12px;  /* helper text, etiquetas auxiliares */
--font-size-13: 13px;  /* labels de componentes */
--font-size-14: 14px;  /* body small, labels de formulario */
--font-size-15: 15px;  /* body denso — ver body.dense */
--font-size-16: 16px;  /* body base (1rem) */
--font-size-17: 17px;  /* body large */
--font-size-22: 22px;  /* heading small, price-sm */
--font-size-28: 28px;  /* heading medium */
--font-size-36: 36px;  /* heading large, price hero */
```

### Line Heights
```css
--leading-tight:   1.15;   /* headings grandes (28px+) */
--leading-snug:    1.3;    /* headings pequeños, labels */
--leading-normal:  1.5;    /* body text */
--leading-relaxed: 1.625;  /* lectura larga */
```

### Letter Spacing (valores en em — no convertir)
```css
--tracking-tighter: -0.04em;  /* headings grandes (28px+) */
--tracking-tight:   -0.02em;  /* headings medianos */
--tracking-normal:   0;        /* body text */
--tracking-wide:     0.025em; /* labels pequeños */
--tracking-wider:    0.05em;  /* ALL CAPS */
--tracking-widest:   0.06em;  /* overline */
```

### Font Variant Numeric
```css
font-variant-numeric: tabular-nums;  /* columnas de montos, precios, tablas */
font-variant-numeric: normal;        /* texto corrido */
```

---

## Shadow Scale

```css
--shadow-xs:   0 1px 2px rgba(0,0,0,0.04);
--shadow-sm:   0 1px 2px rgba(0,0,0,0.04), 0 2px 8px rgba(0,0,0,0.06);
--shadow-md:   0 2px 4px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.08);
--shadow-lg:   0 4px 8px rgba(0,0,0,0.04), 0 16px 40px rgba(0,0,0,0.10);
--shadow-xl:   0 8px 16px rgba(0,0,0,0.06), 0 24px 48px rgba(0,0,0,0.12);
--shadow-card: 0 0 0 1px rgba(0,0,0,0.04), 0 2px 8px rgba(0,0,0,0.04);
--shadow-focus: 0 0 0 3px rgba(117,75,241,0.20); /* derivado de purple.500 */
```

**Hover states:** subir un nivel (xs → sm, sm → md)

---

## Border Radius

```css
--radius-xs:   2px;
--radius-sm:   4px;
--radius-md:   8px;
--radius-lg:   12px;
--radius-xl:   16px;
--radius-2xl:  20px;
--radius-full: 9999px;
```

**Rule:** Elementos anidados tienen MENOR radius que su padre.
Fórmula: `child-radius = parent-radius - padding`

---

## Motion

```css
--duration-fast: 120ms;  /* micro-interacciones, toggles */
--duration-base: 200ms;  /* la mayoría de transiciones */
--duration-slow: 300ms;  /* transiciones de página, modals */

--easing-out:    cubic-bezier(0.2, 0, 0, 1);    /* elementos entrando */
--easing-in:     cubic-bezier(0.4, 0, 1, 1);    /* elementos saliendo */
--easing-in-out: cubic-bezier(0.4, 0, 0.2, 1);  /* cambios de posición */
```

---

## Z-Index

```css
--z-dropdown: 100;
--z-modal:    200;
--z-toast:    300;
```

---

## Responsive Breakpoints

```css
--bp-sm:  640px;
--bp-md:  768px;
--bp-lg:  1024px;
--bp-xl:  1280px;
--bp-2xl: 1536px;
```
