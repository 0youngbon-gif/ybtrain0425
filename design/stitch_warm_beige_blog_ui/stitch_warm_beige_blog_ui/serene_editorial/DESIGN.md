---
name: Serene Editorial
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e4e2e1'
  on-surface: '#1b1c1c'
  on-surface-variant: '#4c463d'
  inverse-surface: '#303030'
  inverse-on-surface: '#f3f0f0'
  outline: '#7d766c'
  outline-variant: '#cec5b9'
  surface-tint: '#695d46'
  primary: '#695d46'
  on-primary: '#ffffff'
  primary-container: '#e6d5b8'
  on-primary-container: '#685c45'
  inverse-primary: '#d5c5a8'
  secondary: '#5f5e5b'
  on-secondary: '#ffffff'
  secondary-container: '#e2dfdb'
  on-secondary-container: '#636260'
  tertiary: '#735a3e'
  on-tertiary: '#ffffff'
  tertiary-container: '#f4d1af'
  on-tertiary-container: '#72583d'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#f2e0c3'
  primary-fixed-dim: '#d5c5a8'
  on-primary-fixed: '#231a08'
  on-primary-fixed-variant: '#504530'
  secondary-fixed: '#e5e2de'
  secondary-fixed-dim: '#c8c6c2'
  on-secondary-fixed: '#1c1c1a'
  on-secondary-fixed-variant: '#474744'
  tertiary-fixed: '#ffddbb'
  tertiary-fixed-dim: '#e3c19f'
  on-tertiary-fixed: '#291803'
  on-tertiary-fixed-variant: '#5a4229'
  background: '#fcf9f8'
  on-background: '#1b1c1c'
  surface-variant: '#e4e2e1'
typography:
  headline-xl:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.1em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-margin: 24px
  gutter: 16px
  section-gap: 48px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
---

## Brand & Style
This design system is built for a high-end mobile reading experience that prioritizes focus, tranquility, and intellectual clarity. The brand personality is sophisticated yet approachable, evoking the feeling of reading a physical independent magazine on a quiet afternoon. 

The aesthetic is rooted in **Minimalism** with an "Organic Modern" influence. It eschews the coldness of traditional tech minimalism by using a warm, tactile palette. The UI should feel like a breathable canvas where the content is the primary occupant, supported by a structure that feels almost invisible.

## Colors
The palette is strictly curated to reduce cognitive load and create a "warm paper" effect. 

- **Primary (Warm Beige):** Used for subtle structural elements, active states, and secondary backgrounds.
- **Secondary (Soft Cream):** The foundational background color for the entire application, providing a softer alternative to pure white to reduce eye strain.
- **Deep Charcoal:** Reserved exclusively for typography and iconography to ensure high legibility while maintaining a softer contrast than pure black.
- **Tertiary (Muted Sand):** Used for delicate accents, borders, and disabled states.

Interactive elements should primarily utilize tonal shifts rather than vibrant color changes to maintain the minimalist harmony.

## Typography
The typography utilizes **Plus Jakarta Sans** for all levels to maintain a cohesive, modern, and friendly editorial tone. 

The type scale is designed with a "text-first" philosophy. Body text is slightly larger than standard mobile defaults (18px) with a generous 1.6 line-height to maximize readability during long-form sessions. Headlines feature tighter tracking and line-height to create a distinct visual anchor. All labels and overlines should use increased letter spacing and uppercase styling to provide clear metadata hierarchy without relying on color.

## Layout & Spacing
The layout follows a **fluid grid** model optimized for handheld devices, characterized by unusually generous margins to create a sense of luxury and space. 

- **Outer Margins:** A fixed 24px margin ensures content never feels cramped against the device edges.
- **Vertical Rhythm:** A strict 8px baseline grid is used. Sections are separated by a large 48px gap to clearly delineate different content types or chapters.
- **Breathability:** Negative space is treated as a functional element. Avoid crowding elements; if in doubt, increase the padding.

## Elevation & Depth
This design system avoids heavy shadows and traditional material elevation. Instead, it uses **Tonal Layering** and **Low-Contrast Outlines**.

- **Level 0 (Base):** The Soft Cream (`#F9F6F2`) background.
- **Level 1 (Surface):** Warm Beige (`#E6D5B8`) surfaces for cards or input fields.
- **Definition:** Instead of shadows, use 1px solid borders in a slightly darker shade of beige or very soft, diffused "ambient" shadows (0px 4px 20px) with only 5% opacity of the Charcoal color.
- **Depth:** Depth is achieved by placing lighter elements on top of slightly darker backgrounds, creating a subtle stacked-paper effect.

## Shapes
The shape language is defined by **soft, organic geometry**. 

A base roundedness of 0.5rem (8px) is applied to most UI components, such as input fields and small cards. For larger containers and primary call-to-action buttons, the roundedness scales up to 1rem (16px) or 1.5rem (24px) to emphasize a friendly, tactile quality. Avoid sharp corners entirely to maintain the approachable, calm aesthetic of the system.

## Components
- **Buttons:** Primary buttons use a Deep Charcoal background with Soft Cream text for maximum impact. Secondary buttons use a Warm Beige background with Charcoal text. All buttons feature high internal padding (16px vertical, 24px horizontal).
- **Cards:** Blog post previews should be borderless, using a Warm Beige background against the Soft Cream page. Content inside cards should have at least 20px of internal padding.
- **Input Fields:** Minimalist design with a subtle 1px border. Focus states are indicated by a thickening of the border or a slight shift in the background tone, rather than a color change.
- **Chips/Tags:** Used for categories. These are pill-shaped with a light Warm Beige fill and Deep Charcoal text in the `label-sm` style.
- **Progress Indicators:** For reading progress, use a thin 2px bar in Deep Charcoal at the top of the viewport.
- **Lists:** Clean dividers using a 0.5px line in a muted beige tone. Each list item should have a minimum height of 64px to remain touch-friendly and breathable.