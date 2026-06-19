# Component Library

Specifications for common UI components. Read when building, reviewing,
or standardizing component design.

All values reference tokens from `color-semantic.json`, `layout-tokens.json`,
and `typography-semantic.json`. Never hardcode colors, spacing, radius, or
motion values — always use tokens.

---

## Quick Token Reference

| Component          | Background              | Border                  | Text                    | Shadow      | Radius      |
|--------------------|-------------------------|-------------------------|-------------------------|-------------|-------------|
| Button primary     | action.primary          | —                       | action.primary-text     | —           | radius.md   |
| Button secondary   | —                       | action.secondary        | action.secondary-text   | —           | radius.md   |
| Button tertiary    | action.tertiary         | action.tertiary-border  | action.tertiary-text    | shadow.xs   | radius.md   |
| Button ghost       | —                       | —                       | text.primary            | —           | radius.md   |
| Input              | bg.input                | border.default          | text.primary            | shadow.xs   | radius.md   |
| Input focus        | bg.input                | border.focus            | text.primary            | shadow.focus| radius.md   |
| Input error        | bg.input                | border.error            | text.primary            | —           | radius.md   |
| Input success      | bg.input                | border.success          | text.primary            | —           | radius.md   |
| Card               | bg.card                 | border.default          | text.primary            | shadow.card | radius.lg   |
| Badge              | status.X-bg             | —                       | status.X                | —           | radius.full |
| Modal              | bg.card                 | border.default          | text.primary            | shadow.lg   | radius.lg   |
| Tooltip            | bg.tooltip              | —                       | neutral.0               | shadow.sm   | radius.sm   |
| Toast              | bg.card                 | border.default          | text.primary            | shadow.sm   | radius.md   |

---

## Component Height Scale

Buttons and inputs MUST share the same heights. This is non-negotiable.

| Size | Height   | Use                                                          |
|------|----------|--------------------------------------------------------------|
| XS   | 28px     | Dense UIs, table actions, tags — **desktop only** ⚠         |
| SM   | 32px     | Secondary actions, compact forms — **desktop only** ⚠       |
| MD   | 36–40px  | Default for most interfaces                                  |
| LG   | 44–48px  | Primary CTAs, mobile touch targets (minimum for mobile)      |
| XL   | 56px     | Hero CTAs, landing pages                                     |

> ⚠ **XS y SM son solo para desktop.** En mobile, todos los targets interactivos
> deben ser LG (44px) mínimo, según Apple HIG y Material guidelines.

Horizontal padding en botones = 2× padding vertical.

---

## Buttons

### Tokens by variant

| State                  | Background              | Text                         | Border                      |
|------------------------|-------------------------|------------------------------|-----------------------------|
| Primary default        | action.primary          | action.primary-text          | —                           |
| Primary hover          | action.primary-hover    | action.primary-text          | —                           |
| Secondary default      | —                       | action.secondary-text        | action.secondary            |
| Secondary hover        | action.secondary-hover  | action.secondary-text-hover  | action.secondary-hover      |
| Tertiary default       | action.tertiary         | action.tertiary-text         | action.tertiary-border      |
| Tertiary hover         | action.tertiary-hover   | action.tertiary-text-hover   | action.tertiary-border-hover|
| Ghost default          | —                       | text.primary                 | —                           |
| Ghost hover            | bg.surface              | text.primary                 | —                           |
| Disabled (all)         | action.disabled         | action.disabled-text         | —                           |
| Focus (all)            | —                       | —                            | border.focus + shadow.focus |

**Secondary:** El estado default usa `action.secondary` (purple.700, #2D006D) — alta
prominencia intencional para acciones de marca. El hover aclara a `action.secondary-hover`
(purple.600, #6844D4) para comunicar interactividad mediante contraste de luminosidad.
El texto usa `action.secondary-text-hover` (`neutral.0`, blanco) en hover: 5.2:1 sobre
purple.600, pasa WCAG AA.

**Tertiary:** Botón outlined con fondo blanco y borde gris. Usa `shadow.xs` en reposo —
la sombra es lo que le da presencia cuando el contraste del borde solo es bajo.
Distinto de ghost: ghost no tiene borde ni sombra.

**Disabled:** Siempre usar `action.disabled` + `action.disabled-text` para todas las
variantes. Nunca usar `opacity: 0.5` sobre el estado habilitado — produce resultados
inconsistentes sobre fondos distintos.

### States (ALL required)
- **Default:** apariencia base según la tabla de variantes
- **Hover:** cambio de background/border según tabla
- **Active/Pressed:** ligeramente más oscuro, sensación de presionado (`transform: scale(0.98)`)
- **Focus:** `border.focus` + `shadow.focus` via `:focus-visible` — el ring aparece solo
  en navegación por teclado, no en click con ratón
- **Disabled:** `action.disabled` bg + `action.disabled-text`. Sin pointer events.
- **Loading:** spinner reemplaza el label, mismas dimensiones, mismo bg que el estado habilitado

### Hierarchy
1. **Primary:** fill `action.primary` — UNO por sección
2. **Secondary:** borde `action.secondary` + bg transparente — acento de marca, contenido
3. **Tertiary:** bg blanco `action.tertiary` + borde gris + `shadow.xs` — neutro, recesivo
4. **Ghost:** solo texto, `bg.surface` en hover — énfasis mínimo
5. **Destructive:** `status.error` como bg, `neutral.0` como texto

### Cuándo usar tertiary vs ghost
- **Tertiary** cuando el botón necesita sostenerse visualmente junto a otros elementos
  (toolbar, footer de card, junto a un primary en el mismo nivel)
- **Ghost** cuando la acción es genuinamente de baja prioridad y el botón apenas debe
  registrarse hasta el hover (ej: "editar", "eliminar" inline en una lista densa)

### Icon Placement
- Leading (izquierda): agrega significado ("+ Nuevo", "Buscar")
- Trailing (derecha): indica comportamiento ("→", "↗", "▾")
- Solo icono: DEBE tener `aria-label` y tooltip en hover

### Border Radius
- Estándar: `radius.md` (8px)
- Variante pill: `radius.full` (9999px)
- Nunca mezclar ambos en la misma vista

---

## Inputs

### Tokens by state

| State    | Border         | Shadow       |
|----------|----------------|--------------|
| Default  | border.default | shadow.xs    |
| Hover    | border.strong  | shadow.xs    |
| Focus    | border.focus   | shadow.focus |
| Error    | border.error   | —            |
| Success  | border.success | —            |
| Disabled | border.default | — (opacity en container) |

### Anatomy
- **Label:** token `component.label`, color `text.primary`, encima del input
- **Label-to-input gap:** `space.2` (8px)
- **Entre campos de formulario:** `space.4`–`space.6` (16–24px) — debe superar el label gap
- **Placeholder:** color `text.placeholder` — solo hint de formato, nunca reemplaza el label
- **Helper text:** tipo `body.sm`, color `text.secondary`, bajo el input
- **Error message:** tipo `body.sm`, color `status.error` + icono, reemplaza el helper text
- **Success message:** tipo `body.sm`, color `status.success` + icono, reemplaza el helper text
- **Background:** `bg.input`
- **Border-radius:** `radius.md` (8px)

### Focus
Usar `:focus-visible` — el ring de focus aparece solo en navegación por teclado.
La interacción con ratón no muestra el ring.

### Heights
Deben coincidir con las alturas de botones en la misma clase de tamaño. Un botón de
40px junto a un input de 40px deben sentirse como una unidad.

---

## Cards

### Tokens
- Background: `bg.card`
- Border: `border.default` (0.5px)
- Border-radius: `radius.lg` (12px)
- Padding: `space.4`–`space.6` (16–24px) — consistente en todas las cards de la misma vista
- Shadow resting: `shadow.card`
- Shadow hover: `shadow.sm`

### Rules
- Gap entre cards > padding dentro de cards (externo ≥ interno, siempre)
- Un único propósito claro por card
- Acciones al pie o en el header, nunca dispersas
- Hover: subir un nivel de sombra (`shadow.card` → `shadow.sm`)
- Click target: toda la card si es navegacional

### Anatomy
```
┌─────────────────────────┐
│  Image/Media (optional) │
├─────────────────────────┤
│  Eyebrow / Category     │  ← body.overline, text.secondary
│  Title                  │  ← h3 o h4, text.primary
│  Description            │  ← body.base, text.secondary
│                         │
│  [Action]    [Action]   │  ← bottom-aligned, space.6 padding
└─────────────────────────┘
```

---

## Tables

- Texto: alinear a la izquierda. Números: alinear a la derecha.
- Header row: sticky, background `bg.surface`, color `text.secondary`
- Altura de fila: 40–52px para escaneo cómodo
- Hover state: `bg.surface` en filas para mejorar escaneo
- Zebra striping O bordes `border.default` por fila — nunca ambos
- Columnas ordenables: flecha direccional clara, `text.secondary` por defecto, `text.primary` activo
- Empty state: mensaje centrado con acción, color `text.secondary`
- **Columnas numéricas:** aplicar `component.table-cell` que incluye `font-variant-numeric: tabular-nums`

---

## Navigation

### Top Nav
- Height: 48–64px
- Background: `bg.card`, border-bottom: `border.default`
- Logo izquierda, nav centro o izquierda, acciones derecha
- Active state: `text.primary` + subrayado `border.focus` o background `bg.surface`
- Inactivo: `text.secondary`
- Mobile: colapsar a hamburger en `--bp-md`

### Sidebar
- Width: 240–280px expandido, 64–72px colapsado
- Background: `bg.card`, border-right: `border.default`
- Section headers: tipo `body.overline`, color `text.secondary`
- Active state: background `bg.surface` + borde izquierdo `border.focus` (3px) + `text.primary`
- Inactivo: `text.secondary`
- Icons: 20–24px, mismo stroke weight
- Trigger de colapso: claramente visible

### Tabs
- Bottom tabs en mobile: máximo 5 items
- Tab activo: `text.primary` + subrayado `border.focus` o bg `action.secondary-hover`
- Inactivo: `text.secondary`
- Badge dots: `status.error` para errores, `status.alert` para alertas
- Contenido swipeable en vistas mobile con tabs

---

## Modals

| Type         | Max Width | Use                          |
|--------------|-----------|------------------------------|
| Confirmation | 400px     | Delete, acciones destructivas|
| Form         | 480px     | Formularios cortos, settings |
| Content      | 640px     | Artículos, previews          |
| Complex      | 960px     | Multi-step, dashboards       |

### Tokens
- Background: `bg.card`
- Border-radius: `radius.lg` (12px)
- Padding: `space.6`–`space.8` (24–32px)
- Overlay: rgba(0,0,0,0.4) a rgba(0,0,0,0.6)
- Z-index: `z.modal` (200)

### Motion
- Enter: `duration.slow` + `easing.out`
- Exit: `duration.base` + `easing.in`
- Animar solo `transform` (translateY + scale) y `opacity`

### Rules
- Botón de cierre: esquina superior derecha, siempre visible
- Acciones: inferior derecha, acción primaria a la derecha
- Focus trap: Tab cicla solo dentro del modal
- Escape cierra
- Click en backdrop cierra (solo modals no destructivos)

---

## Tooltips

- Background: `bg.tooltip` (#111827), text: `neutral.0`
- Border-radius: `radius.sm` (4px)
- Max width: 240px
- Padding: `space.2` `space.3` (8px 12px)
- Type: `body.sm`
- Delay: 300–500ms antes de mostrar
- Position: auto-flip para mantenerse en viewport
- Flecha apuntando al elemento trigger

---

## Badges & Tags

### Status colors — usar siempre el par de tokens

| Status  | Text token     | Background token  | Color  |
|---------|----------------|-------------------|--------|
| success | status.success | status.success-bg | green  |
| error   | status.error   | status.error-bg   | red    |
| warning | status.warning | status.warning-bg | yellow |
| alert   | status.alert   | status.alert-bg   | orange |
| info    | status.info    | status.info-bg    | purple |

**Cuándo usar cada uno:**
- `success` — completado, confirmado, activo
- `error` — fallido, bloqueado, inválido
- `warning` — atención requerida, no bloqueante
- `alert` — acción requerida pronto, urgencia mayor que warning
- `info` — contexto neutral, informativo

Nunca usar el mismo token para texto y fondo.
Nunca depender solo del color — siempre acompañar con icono o label.

### Specs
- Height: 20–24px (inline con texto)
- Padding: `space.1` `space.2` (4px 8px)
- Border-radius: `radius.full` (9999px) para status badges, `radius.sm` para category tags
- Type: `component.badge` (11px, semibold)
- Tags removibles: incluir icono × con color hover `status.X`

---

## Alert Banners

Banners full-width o contenidos para mensajes de estado persistentes.
Usa los mismos pares de tokens de status que los badges, a mayor escala.

### Anatomy
```
┌────────────────────────────────────────────┐
│ [icon]  Title text              [action?]  │
│         Supporting description             │
└────────────────────────────────────────────┘
```

### Tokens
- Background: `status.X-bg`
- Text e icono: `status.X`
- Border-left accent (3px): `status.X` — usar `border-radius: 0` en el lado izquierdo
- Border-radius: `radius.md` (8px)
- Padding: `space.3` `space.4` (12px 16px)
- Icono: 20px, mismo color que el texto

### Rules
- Siempre incluir icono — nunca depender solo del color
- Title usa `body.base` (semibold), descripción usa `body.sm`
- Banners descartables incluyen botón de cierre (superior derecha)
- Banners persistentes (errores, estado del sistema) no son descartables

---

## Toast / Notifications

### Tokens
- Background: `bg.card`
- Border: `border.default`
- Border-left accent (3px): `status.X` según tipo de toast
- Icono: color `status.X`, 20px
- Border-radius: `radius.md` (8px)
- Z-index: `z.toast` (300)

### Motion
- Enter: `duration.base` + `easing.out` (slide desde borde)
- Exit: `duration.fast` + `easing.in`
- Animar solo `transform` y `opacity`

### Rules
- Posición: superior derecha o inferior centro
- Width: 320–400px
- Auto-dismiss: 5–8s para info/success/warning — nunca para errores o alertas
- Apilar desde el más reciente arriba
- Siempre incluir botón de cierre
- Incluir link de acción cuando sea relevante ("Deshacer", "Ver")
- Siempre acompañar color con icono — nunca solo color para diferenciar tipo

---

## Loading States

### Skeleton screens
Usar para contenido que carga asincrónicamente (cards, filas de tabla, feed items).

- Skeleton bg: `bg.surface`
- Shimmer highlight: `border.default`
- Border-radius: coincidir con el componente que se está cargando
- Animation: shimmer sweep, `duration.slow`, **easing lineal**
  (lineal es la excepción correcta para loops de shimmer)
- Animar solo `background-position` u `opacity`

#### Skeletons para componentes financieros

**Balance hero** — 1 bloque ancho (180px × 40px) + 1 bloque label (80px × 14px encima)

**Transaction row** — 3 bloques en línea:
- Avatar/icono: círculo 36px
- Descripción: bloque 120px × 14px + bloque 80px × 12px debajo
- Monto: bloque 64px × 16px, alineado a la derecha

**Metric card** — 1 bloque label (60px × 12px) + 1 bloque número (100px × 24px) debajo

**Table row** — bloques proporcionales a cada columna, mismo ancho que el header correspondiente

### Spinner
Usar para acciones de duración indeterminada (botón loading, transiciones de página).

- Color: `action.primary` sobre fondo claro, `action.primary-text` dentro de primary buttons
- Tamaño: coincide con el tamaño del icono del contexto circundante (16–24px)
- Animation: rotación, `duration.slow` por vuelta, easing lineal

### Rules
- Preferir skeleton sobre spinner para carga de página/sección
- Nunca mostrar skeleton y spinner en la misma vista
- Siempre mantener las dimensiones del layout durante la carga (evitar layout shift)
