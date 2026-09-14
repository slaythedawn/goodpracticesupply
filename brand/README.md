# Good Practice Supply, logo files

Drawn from the design system rather than traced from a screenshot. The type is
real Archivo Black and Archivo SemiBold, set at the exact sizes and tracking the
spec calls for, then converted to outlines. The SVGs carry no font dependency, so
they render identically everywhere.

## What to use

| Use | File |
|---|---|
| Default, most places | `svg/gps-lockup-forest.svg` |
| On a forest or dark ground | `svg/gps-lockup-canvas.svg` |
| Where the lockup is too wide | `svg/gps-wordmark-*.svg` |
| Small or square placements | `svg/gps-monogram-*.svg` |
| App icon, social avatar | `favicon/gps-icon-512.png`, `favicon/gps-avatar-512.png` |
| Browser tab | `favicon/favicon.ico` |

Reach for SVG wherever the destination accepts it. The PNGs are for places that
will not take vector: email signatures, some marketplaces, ad platforms.

## Colour

| Variant | Hex | Where |
|---|---|---|
| Forest | `#1C4034` | On canvas, white or any light ground |
| Canvas | `#FAFAFA` | On forest, forest deep or photography |
| Mint | `#8FBFA6` | Sparingly, where the mark is decorative rather than identifying |

Never pure white or pure black. The mark is never mint on light, since mint is
the action colour and carries a meaning of its own in the interface.

## Clear space and minimum size

Leave clear space of at least the height of the `gp` ring on every side. The
lockup should not be set below 120px wide, and the monogram not below 24px.
Below that, use the simplified favicon mark, which drops the ring.

## The favicon is deliberately a different drawing

At 16 and 32px the ring and its padding collapse into mush. `svg/gps-favicon-small.svg`
drops the ring and lets the `gp` fill the tile. That is the drawing behind
`favicon.ico` and the 16 and 32px PNGs. Everything 48px and up uses the ring.

## Files

- `svg/` source, outlined, no font needed. Monogram, wordmark and lockup in three
  colours, plus tiles and the small favicon mark.
- `png/` transparent exports. Monogram at 64 to 1024px square, lockup at 400 to
  2400px wide, wordmark at 400 to 1600px wide, each in three colours.
- `favicon/` app icons and browser icons on a solid forest ground, since these
  sit on backgrounds you do not control.

## One caveat

Archivo and Archivo Black are licensed under the SIL Open Font License, which
permits commercial use and embedding. Outlining the type in a logo is normal
practice and is fine under that licence. Worth a look from whoever handles your
trade marks before this is filed as a mark, since that is a separate question
from the font licence.
