# Fallback palette

Use this only when the project has **no** color system. Once applied, these become
the project's own tokens; never hardcode them in components.

```css
:root {
  color-scheme: dark;
  --background: #2d2f42;   /* page background */
  --elevated: #34364a;     /* sidebar, bars, composer */
  --panel: #383b50;        /* windows, dialogs */
  --deep: #242637;         /* inset areas, logs, gauges */
  --raised: #42455c;       /* selected entries, secondary buttons */
  --hover: #4a4d65;        /* hover surfaces */
  --text: #f7e6ea;         /* body text */
  --muted: #dac8cd;        /* secondary labels */
  --subtle: #b9a9ae;       /* overlines, metadata */
  --brand: #d46c7f;        /* primary action (use dark text on it) */
  --brand-strong: #a84e5f; /* strong brand surface */
  --accent: #f6798c;       /* focus, corner marks, current item */
  --accent-soft: #ff9cab;  /* cursor, links */
  --success: #7bc6a4;
  --warning: #e2b36a;
  --danger: #e08696;
  --info: #97b7ff;
  --border: rgba(247, 230, 234, .12); /* separators only; use a stronger frame for controls */
}
```

Before relying on any pairing, measure the actual foreground and background
contrast. Text needs 4.5:1; large text, focus indicators and control boundaries
need 3:1.
