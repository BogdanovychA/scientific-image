# Design System Inspired by Scientific World Knowledge Base

## 1. Visual Theme & Atmosphere

This design system serves an academic knowledge base centered on scientific concepts, natural philosophy, and educational content. The visual identity reflects intellectual rigor and clarity through a refined, minimal aesthetic that prioritizes content accessibility and navigational hierarchy. The palette combines primary blue-grey branding with a clean Wikipedia-inspired neutral foundation, creating a trustworthy, scholarly atmosphere. Typography emphasizes readability with serif body text and headings (Linux Libertine) paired with clean sans-serif (Roboto) for UI and meta elements, evoking a blend of traditional academic publishing and modern digital design. The overall mood is contemplative yet approachable, designed to support deep learning and exploration through intuitive visual structure.

**Key Characteristics**
- Minimalist, content-focused layout with generous whitespace
- Blue-Grey primary branding (`#607D8B`) establishing scholarly authority
- Serif headings and body text for classic encyclopedic reading
- Sans-serif (Roboto) for UI elements, sidebar lists, and article descriptions
- Flat card components (no shadows) and hairline borders for clean layouts
- Clean, wrap-based index quick navigation bar for easy content discovery
- Semantic color integration for status feedback and validation states
- Fully adapted dark (slate) mode matching light theme contrasts

---

## 2. Color Palette & Roles

### Primary (Theme Brand)
- **Primary Blue-Grey** (`#607D8B`): Core brand color for header backgrounds and primary layout wrapper elements (configured via MkDocs Material palette)
- **Slate Header BG** (`#546D78`): Secondary shade for navigation bars and header states

### Accent & Interactive
- **Link Blue** (`#1565C0`): Interactive color for text links, navigation links, and hover states
- **Accent Muted Blue** (`#4051B5`): Secondary interactive accent color for selected/focused navigation items

### Neutral Scale (Light Theme)
- **Black** (`#000000`): Default text color for body content (87% opacity `rgba(0,0,0,0.87)` in content blocks)
- **Muted Gray** (`#54595D`): Secondary text color for article descriptions, copyright text, and meta info (`--wiki-muted`)
- **Border Gray** (`#A2A9B1`): Hairline borders, tables, and dividers (`--wiki-border`)
- **Box Background** (`#F8F9FA`): Light gray tint for code containers, blockquotes, and zebra striping (`--wiki-box-bg`)
- **Header Background** (`#EAECF0`): Background for table headers and list navigation items (`--wiki-header-bg`)

### Neutral Scale (Dark Slate Theme)
- **Text Light** (`#E2E4E9`): Primary text color in dark mode
- **Muted Gray Slate** (`#959BA2`): Secondary text color for descriptions and meta (`--wiki-muted` override)
- **Border Slate** (`#3B3E43`): Border lines and table dividers (`--wiki-border` override)
- **Box BG Slate** (`#27292D`): Dark background tint for code, blockquotes, and table rows (`--wiki-box-bg` override)
- **Header BG Slate** (`#27292D`): Background for table headers and index tags (`--wiki-header-bg` override)

### Semantic / Status
- **Danger Red** (`#FF1947`): Critical alerts, errors, and danger states (e.g. MONO/emergency notes)
- **Success Green** (`#00C753`): Confirmation states and success indicators
- **Warning Yellow** (`#FFD500`): Caution, warnings, and advisory blocks

---

## 3. Typography Rules

### Font Family
- **Primary (Body, Headings, and Quotes)**: `Linux Libertine`, `Georgia`, `Times New Roman`, `serif` (`--wiki-serif`)
- **Secondary (UI, Labels, Descriptions, and Nav)**: `Roboto`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `sans-serif`
- **Monospace (Code Blocks)**: `Roboto Mono`, `Courier New`, `monospace`

### Hierarchy

| Role | Font Family | Size | Weight | Line Height | Letter Spacing | Notes / Usage |
|------|-------------|------|--------|-------------|----------------|---------------|
| **Display 1 (H1)** | Linux Libertine | 32px | 400 | 1.3 | 0px | Primary page heading |
| **Heading 2 (H2)** | Linux Libertine | 24px | 400 | 1.3 | 0px | Major article section headings |
| **Heading 3 (H3)** | Linux Libertine | 20px | 400 | 1.3 | 0px | Subsection headings |
| **Body Large** | Linux Libertine | 16px | 400 | 1.65 | 0px | Primary article paragraph text |
| **Body Regular** | Roboto | 14px | 400 | 1.5 | 0.5px | Sidebar links, meta text, list item details |
| **Body Small** | Roboto | 12.8px | 400 | 1.4 | 0px | Captions, metadata, footer notes |
| **Link** | Roboto / Serif | 14px | 600 | 1.5 | 0px | Text links and navigation anchors |
| **Code** | Roboto Mono | 12px | 400 | 1.4 | 0px | Inline code and block codes |

### Principles
- **Wikipedia-like Headers**: All headings (`h1`, `h2`, `h3`) are styled with the serif font (`Linux Libertine`) at weight `400` with a subtle bottom border (`1px solid var(--wiki-border)`), reflecting classic scientific encyclopedias.
- **Contrast Pairing**: High-contrast serif text is utilized for reading long articles, while sans-serif text is utilized for navigation elements, sidebar links, and metadata descriptions.
- **Generous Line Height**: Article text maintains a line height of `1.65` to maximize readability and reduce visual fatigue.

---

## 4. Component Stylings

### Alphabet Quick Navigation Panel (`.alpha-nav`)
- **Layout**: Horizontal flexbox (`display: flex; flex-wrap: wrap; gap: 6px;`)
- **Container**: Padded `8px 12px`, background `var(--wiki-box-bg)`, border `1px solid var(--wiki-border)`, border-radius `4px`
- **Navigation Link (`.alpha-nav-link`)**:
  - Shape: `min-width: 28px`, `height: 28px`, `line-height: 26px`, text-align `center`
  - Font: `Linux Libertine / serif`, weight `600`, size `1.05em`, color `var(--md-typeset-a-color, #1565C0)`
  - Border: `1px solid transparent`, border-radius `3px`
  - Hover: Background `var(--wiki-header-bg)`, border-color `var(--wiki-border)`, text-decoration `none`

### Index Feed Article Items (`.alpha-section + ul`)
- **List Style**: Unordered list with bullet points removed (`list-style: none`), padding-left `0`
- **Spacing**: Margins set to `margin-bottom: 1.2em` for each article to provide vertical separation
- **Title Link (`.article-title`)**:
  - Font: `Linux Libertine / serif`, weight `600`, size `1.05em`
  - Tag: Wrapper `<span class="article-title">` for consistent styling
- **Description (`.article-desc`)**:
  - Display: Block layout (`display: block`) to push description beneath the title
  - Font: `Roboto / sans-serif`, size `0.88em`, color `var(--wiki-muted)`, line-height `1.5`, margin-top `0.15em`

### Admonitions / Callout Cards (`.admonition`)
- **Flat Layout**: No box shadows (`box-shadow: none !important`)
- **Border**: Thin border `1px solid rgba(0, 0, 0, 0.08) !important` (dark slate theme uses `rgba(255, 255, 255, 0.08) !important`)
- **Accent Border**: Thick left border `0.2rem solid var(--md-admonition-icon-color) !important` to preserve warning categories
- **Border Radius**: Subtle rounded corners `border-radius: 4px !important`

### Scientific Citations & Blockquotes (`blockquote`)
- **Container**: Background `var(--wiki-box-bg)`, left border `4px solid var(--wiki-border)`, border-radius `0 4px 4px 0`
- **Spacing**: Padding `0.5em 1.2em`, margins `1.5em 0`
- **Typography**: Italic text style, color `var(--wiki-muted)`

### Wikipedia-Style Tables (`table`)
- **Layout**: Border collapse `collapse`, font size `0.85em`
- **Cells**: Th/td padding `4px 8px`, border `1px solid var(--wiki-border)`
- **Headers (th)**: Background `var(--wiki-header-bg)`, text-align `left`
- **Zebra Striping**: Even rows (`tr:nth-child(even)`) use background color `var(--wiki-box-bg)`

---

## 5. Layout & Spacing Principles

### Spacing System
- **Base Unit**: `4px`
- **Scale**: `4px, 8px, 12px, 16px, 20px, 24px, 28px, 32px, 44px`
- **Applications**:
  - `4px / 6px`: Flex gaps between navigation tags, small inline margins
  - `8px / 12px`: Element padding, card margins, sidebar list items
  - `16px / 20px`: Major container paddings, content block separations
  - `32px`: Main page desktop margins

### Grid Constraints
- **Max Width**: `1220px` (desktop grid containment)
- **Primary Content Area**: `688px` max-width to restrict text line-lengths to an accessible `70-80` characters
- **Sidebar Width**: `240px` (left sidebar containing random articles list)

---

## 6. Depth & Elevation

- **Elevation 0 (Flat)**: The baseline style for the entire site. Containers, cards, tables, blockquotes, and admonitions are completely flat with `box-shadow: none` to support the Wiki style.
- **Elevation 1 (Raised)**: Subtle borders and background offsets (`var(--wiki-box-bg)`) are utilized to establish depth instead of heavy shadows.
- **Elevation 2 (Interactive)**: Hover states for links and alphabet navigation buttons utilize subtle color/border changes (`var(--wiki-header-bg)`), keeping the interface flat and clean.

---

## 7. Do's and Don'ts

### Do
- Use `Linux Libertine` (serif) at regular weight `400` for all article headings and body text.
- Wrap titles in `<span class="article-title">` and descriptions in `<span class="article-desc">` for lists.
- Enforce `display: block` on descriptions to place them on a new line.
- Use `var(--wiki-box-bg)` for blockquotes and even table rows to ensure dark mode compatibility.
- Ensure all custom styling changes are tested in both light and dark (slate) mode color schemes.

### Don't
- Use heavy box shadows (`box-shadow`) or arbitrary elevation settings.
- Use sans-serif fonts for article titles or headings (UI elements only).
- Hardcode color hex values in stylesheets; use CSS variables (`var(--wiki-border)`, `var(--wiki-muted)`, etc.) for dark mode fallback support.
- Set line-height below `1.5` for reading blocks.

---

## 8. Responsive Behavior

### Collapsing Strategy
- **Left Sidebar**: Primary sidebar navigation collapses into the hamburger menu drawer on screens below `768px`.
- **Alphabet Quick Nav**: Letter index navigation tags wrap onto multiple rows using flex-wrap on tablets and mobile screens, maintaining minimum touch target sizes (`44px` height).
- **Index Articles Feed**: Card layouts collapse to `100%` width, and spacing margins adapt proportionally to maintain vertical rhythm.
