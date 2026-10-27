# Component recipes

These are CSS recipes for the shared primitives. Variable names are placeholders:
map them to the project's own tokens. Every color below is a token reference or a
`color-mix()` of tokens.

## Contents
- Tokens
- Window with stepped corner marks
- Menu entry with pixel cursor
- Buttons
- Fields and focus
- Tabs
- Segmented gauge (HP/MP)
- Status pill and chip
- Indeterminate activity line
- Panel motion and reduced motion

## Tokens

```css
:root {
  /* Existing color tokens stay as they are; add only derived and non-color tokens. */
  --frame: color-mix(in srgb, var(--muted) 28%, transparent);
  --px: 2px;
  --radius: 2px;
  --font-ui: system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-pixel: "Pixel Title Font", var(--font-ui); /* optional, titles >= 15px */
  --font-mono: ui-monospace, "Cascadia Code", Consolas, monospace;
  --quick: 120ms;
}
```

## Window with stepped corner marks

```css
.window { position: relative; background: var(--panel); border: 1px solid var(--frame); border-radius: var(--radius); }
.window::before, .window::after { content: ""; position: absolute; width: var(--px); height: var(--px); background: var(--accent); pointer-events: none; }
.window::before { top: -1px; left: -1px; box-shadow: var(--px) 0 0 var(--accent), 0 var(--px) 0 var(--accent); }
.window::after { bottom: -1px; right: -1px; box-shadow: calc(-1 * var(--px)) 0 0 var(--accent), 0 calc(-1 * var(--px)) 0 var(--accent); }
.window > header { padding: 12px 16px; border-bottom: 1px solid var(--border); font: 600 16px/1.3 var(--font-pixel); }
```

Use the marks on primary windows only. Plain cards can keep the frame without
them.

## Menu entry with pixel cursor

```css
.menu-item { position: relative; display: flex; gap: 10px; padding: 9px 12px 9px 22px; border: 1px solid transparent; border-radius: var(--radius); color: var(--muted); background: transparent; }
.menu-item:hover, .menu-item:focus-visible { background: var(--hover, var(--raised)); color: var(--text); }
.menu-item[aria-current], .menu-item.active { background: var(--raised); border-color: var(--frame); color: var(--text); }
.menu-item[aria-current]::before, .menu-item.active::before, .menu-item:hover::before, .menu-item:focus-visible::before {
  content: ""; position: absolute; left: 8px; top: 50%; width: 6px; height: 10px; margin-top: -5px; background: var(--accent-soft, var(--accent));
  clip-path: polygon(0 0, 34% 0, 34% 20%, 67% 20%, 67% 40%, 100% 40%, 100% 60%, 67% 60%, 67% 80%, 34% 80%, 34% 100%, 0 100%);
}
```

The `clip-path` draws a stepped triangle, which keeps the cursor pixel-crisp at
any zoom. Use the same cursor for the current table row, the active tab and the
focused list item.

## Buttons

```css
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 8px 14px; border: 1px solid var(--frame); border-radius: var(--radius); background: var(--raised); color: var(--text); font: 600 13px/1.2 var(--font-ui); transition: background var(--quick) steps(2), border-color var(--quick) steps(2); }
.btn:hover:not(:disabled) { border-color: var(--subtle); }
.btn:active:not(:disabled) { transform: translateY(1px); }
.btn.primary { background: var(--brand); border-color: var(--brand); color: var(--deep); } /* verify contrast */
.btn:disabled { opacity: .55; cursor: not-allowed; }
```

Use dark text on bright brand fills unless measured contrast says otherwise.

## Fields and focus

```css
input, select, textarea { padding: 8px 10px; border: 1px solid var(--frame); border-radius: var(--radius); background: var(--deep); color: var(--text); }
:focus-visible { outline: var(--px) solid var(--accent-soft, var(--accent)); outline-offset: var(--px); }
[aria-invalid="true"] { border-color: var(--danger); }
```

## Tabs

```css
.tabs { display: flex; gap: 2px; border-bottom: 1px solid var(--frame); }
.tab { position: relative; padding: 9px 14px 9px 24px; border: 1px solid transparent; border-bottom: 0; background: transparent; color: var(--muted); }
.tab[aria-selected="true"] { background: var(--panel); border-color: var(--frame); color: var(--text); margin-bottom: -1px; }
/* Reuse the menu cursor for .tab[aria-selected="true"]::before */
```

## Segmented gauge (HP/MP)

Render one child per segment from real data, at most about 40:

```html
<div class="gauge" role="img" aria-label="2 of 5 tasks verified">
  <span class="filled"></span><span class="filled"></span><span></span><span></span><span></span>
</div>
```

```css
.gauge { display: flex; gap: 2px; height: 10px; padding: 2px; border: 1px solid var(--frame); background: var(--deep); }
.gauge span { flex: 1; background: var(--raised); }
.gauge span.filled { background: var(--success); }  /* HP; use --info for MP-style resource meters */
.gauge.unknown { background: repeating-linear-gradient(90deg, var(--raised) 0 6px, var(--panel) 6px 8px); }
```

## Status pill and chip

```css
.pill { display: inline-flex; align-items: center; gap: 6px; padding: 2px 8px; border: 1px solid var(--frame); border-radius: var(--radius); background: var(--raised); font: 600 12px/1.4 var(--font-ui); }
.pill::before { content: ""; width: 6px; height: 6px; background: var(--info); }
.pill.ok::before { background: var(--success); } .pill.wait::before { background: var(--warning); } .pill.error::before { background: var(--danger); }
```

## Indeterminate activity line

```css
.activity { height: 6px; background: linear-gradient(90deg, var(--raised) 0 30%, var(--accent) 30% 45%, var(--raised) 45%); background-size: 200% 100%; animation: sweep 1.6s steps(10) infinite; }
@keyframes sweep { from { background-position: 100% 0; } to { background-position: -100% 0; } }
```

Show it only while real work runs; it must never imply a percentage.

## Panel motion and reduced motion

```css
dialog[open], .panel-enter { animation: panel-in 140ms steps(3); }
@keyframes panel-in { from { opacity: 0; transform: translateY(2px); } to { opacity: 1; transform: none; } }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}
```
