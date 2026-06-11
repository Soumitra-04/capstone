---
name: Obsidian Stream
colors:
  surface: '#121414'
  surface-dim: '#121414'
  surface-bright: '#383939'
  surface-container-lowest: '#0d0e0f'
  surface-container-low: '#1b1c1c'
  surface-container: '#1f2020'
  surface-container-high: '#292a2a'
  surface-container-highest: '#343535'
  on-surface: '#e3e2e2'
  on-surface-variant: '#b9ccb2'
  inverse-surface: '#e3e2e2'
  inverse-on-surface: '#303031'
  outline: '#84967e'
  outline-variant: '#3b4b37'
  surface-tint: '#00e639'
  primary: '#ebffe2'
  on-primary: '#003907'
  primary-container: '#00ff41'
  on-primary-container: '#007117'
  inverse-primary: '#006e16'
  secondary: '#ffb4ab'
  on-secondary: '#690006'
  secondary-container: '#d30017'
  on-secondary-container: '#ffe2de'
  tertiary: '#f9f9f9'
  on-tertiary: '#2f3131'
  tertiary-container: '#dcdddd'
  on-tertiary-container: '#5f6161'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#72ff70'
  primary-fixed-dim: '#00e639'
  on-primary-fixed: '#002203'
  on-primary-fixed-variant: '#00530e'
  secondary-fixed: '#ffdad6'
  secondary-fixed-dim: '#ffb4ab'
  on-secondary-fixed: '#410002'
  on-secondary-fixed-variant: '#93000c'
  tertiary-fixed: '#e2e2e2'
  tertiary-fixed-dim: '#c6c6c7'
  on-tertiary-fixed: '#1a1c1c'
  on-tertiary-fixed-variant: '#454747'
  background: '#121414'
  on-background: '#e3e2e2'
  surface-variant: '#343535'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  body-main:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  data-mono:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.1em
spacing:
  unit: 8px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 32px
  container-max: 1440px
---

## Brand & Style

The design system is engineered for the high-stakes environment of real-time gaming infrastructure. It targets DevOps engineers who require split-second situational awareness. The aesthetic is **Minimalist-Futuristic**, characterized by a "void" philosophy where non-essential UI elements are stripped away, leaving only mission-critical data.

The emotional response is one of absolute control and precision. By utilizing a deep dark-mode palette and removing traditional borders, the system achieves a "glass-cockpit" feel. Visual hierarchy is driven by luminance rather than color, with status indicators providing the only vibrant breaks in the monochromatic environment.

## Colors

This design system utilizes a high-contrast, deep-sea palette to minimize eye strain during long monitoring sessions.

- **Background (#0A0A0A):** A matte black foundation that absorbs light and recedes, allowing data to float.
- **Surface (#111111):** Subtle elevation changes are handled through these slightly lighter surfaces, never through borders.
- **Primary / Healthy (#00FF41):** An electric "Matrix" green used exclusively for active streams, healthy nodes, and successful deployments.
- **Secondary / Alert (#FF3131):** A high-intensity crimson reserved for critical failures and performance bottlenecks.
- **Typography:** Stark white (#FFFFFF) for primary data and muted gray (#888888) for metadata and labels.

## Typography

The typography system strikes a balance between human-readable sans-serif and technical monospaced fonts.

- **Inter** is the workhorse for the UI structure, providing clarity in navigation and headers. Use tighter letter-spacing for large headlines to maintain a dense, high-tech look.
- **JetBrains Mono** is utilized for all technical data, including IP addresses, latency metrics, and log outputs. 
- **Hierarchy Rule:** Labels should always be displayed in `label-caps` using the muted gray color to ensure they recede, allowing the white `data-mono` values to dominate the visual field.

## Layout & Spacing

The layout follows a **Fluid Grid** model with high density but significant negative space between functional groups. Separation is achieved through 24px gutters rather than lines.

- **Grid:** A 12-column system for desktop. Components should snap to the grid to maintain a disciplined, architectural feel.
- **Rhythm:** An 8px base unit governs all padding and margins. 
- **Density:** While the UI is data-dense, use generous 32px external margins on desktop to prevent the interface from feeling "cramped" against the screen edges.

## Elevation & Depth

This design system rejects traditional shadows and physical metaphors. Depth is communicated through **Tonal Layering**:

- **Level 0 (#0A0A0A):** The main canvas.
- **Level 1 (#111111):** Cards, containers, and sidebars.
- **Level 2 (#1A1A1A):** Hover states and active selections.

To indicate "Live" or "Critical" status, use a **minimalist glow**. This is not a drop shadow, but a soft Gaussian blur of the accent color (#00FF41 or #FF3131) limited to a 4px-8px radius behind the status indicator light.

## Shapes

The shape language is **Strictly Geometric**. To reinforce the technical, futuristic nature of the dashboard, all elements use **0px corner radius**. 

Square edges convey a sense of modularity and precision. This applies to buttons, cards, input fields, and status pips. The only exception is the circular "Status Pulse" indicator used to denote real-time connectivity.

## Components

- **Buttons:** Primary buttons are white text on a #1A1A1A background with no border. On hover, the background shifts to primary green (#00FF41) with black text.
- **Status Indicators:** A small 8x8px square. If 'Live', it features a subtle pulse animation with a 50% opacity glow of #00FF41.
- **Cards:** No borders. Background is #111111. Headers within cards use `label-caps` in #888888.
- **Input Fields:** Bottom-border only (1px #888888) or solid #0A0A0A background. Focus state changes the bottom border to #FFFFFF.
- **Data Tables:** Row-based layout. No vertical lines. Hovering over a row changes the background to #1A1A1A.
- **Charts:** Use thin 1px lines for trend data. The area under the line should have a very subtle gradient (accent color to transparent) at 10% opacity.