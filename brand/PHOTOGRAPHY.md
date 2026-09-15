# Human photography, locked

Every image on the site that features a person, or any part of one, is shot to
this brief. It is not a mood board, it is a constraint: the same brief goes into
every generation so the site reads as one campaign rather than a stock library.

## Why this and not something else

The business sits between two audiences who are usually photographed in opposite
ways. Consumer health imagery is warm, smiling and lifestyle-led. Clinical supply
imagery is cold, gloved and institutional. Neither is right. The people buying
here are health and fitness literate, they know what a 29 gauge is, and they are
as likely to be managing their own protocol at a kitchen bench as running a
treatment room. The brief below is deliberately pitched in the gap: premium and
modern, calm rather than cheerful, and plainly capable without being medical.

## The brief

**Casting.** Lean, athletic Australians in their thirties who read as health and
fitness literate rather than as medical staff. Fine black-and-grey tattoo work
visible on forearms where it falls naturally. Never a model type, never a
white-coat type.

**Wardrobe.** Plain, unbranded, in charcoal, slate, stone or off-white. Sleeves
pushed up. No lab coats, no stethoscopes, no scrubs, and no gloves unless the
gloves are the subject of the shot.

**Expression.** Relaxed, easy, self-possessed. Mouth closed or barely smiling.
Never a broad grin. Never posed.

**Light.** Cool neutral north daylight raking from the left. No warm cast, no
golden hour, no practical lamps in shot.

**Palette.** Muted and desaturated. Pale cool grey, concrete, stone, charcoal.

**Setting.** Bare, uncluttered, modern minimal architecture. Generous negative
space, which is also what gives the overlay panels somewhere to sit.

**Capture.** Crisp, precise, high resolution, sharp on the subject, clean
digital. No film grain, no noise. Shallow depth of field, typically 85mm at f/2.

**Never.** Text, logos, branding, printed labels, signage, watermarks. No
medicines and no filled syringes. No before and after.

## Composition rules that come from the layout, not the brief

A hero photograph has to be shot for the panel that sits on it.

- The subject holds the right third of the frame. The left is bare wall.
- There is real headroom: empty wall above the head filling the top fifth or so
  of the picture, because the nav is 107px deep on a desktop and 124px on a phone
  and the face has to clear it.
- Crops are pinned, never centred. The desktop crop takes from the left so the
  subject is never clipped as the window narrows.

## The prompt

The canonical wording lives in `HUMAN_STYLE` in the page generators
(`gen/style.py`), so that every regeneration inherits it rather than
paraphrasing it. Change it there and rebuild, do not edit a generated page.

## Generated lettering

Image models put lettering on anything that looks like packaging, and it always
comes out as gibberish: AVORID DN S PODA on a supply box, Bolioabetrine on a
vial. Prompting against it does not work reliably. Six of seven attempts to
regenerate one shot came back with text on them despite the brief spelling out
"no writing, no letters, no numbers, no words, no text, no symbols, no barcode,
no label" every time.

So it is checked mechanically rather than by eye. Every image on the site is run
through OCR (`rapidocr-onnxruntime`), and anything that reads back as a word is
either repaired or retired.

Repairing beats regenerating, because a composition that works is worth more
than a clean one that does not. The lettering sits on flat, smoothly lit
surfaces, so the fix is a bilinear reconstruction from the four borders of the
patch plus noise matched to the surrounding grain, which on a matte box face is
an exact fit rather than an approximation. Two rules keep it honest:

- Only repair text-shaped regions: short, wide, small. A tall or square
  detection is a real object the detector mistook for a glyph, and filling it
  takes a bite out of the picture. A glucose monitor once came back as "D".
- If the lettering is the subject, retire the shot instead. A close-up of
  syringe graduations reading 43, 45 and 23 cannot be repaired, because painting
  out the numbers paints out the graduations.

Repaired files live on a separate media host to the generated ones, which is why
two CloudFront domains appear in the markup.

## Product still life

The human brief above does not cover the catalogue shots, which are the other
half of the site's imagery and follow their own short brief:

- One product, on a pale cool-grey seamless surface, nothing else in frame.
- Cool neutral daylight raking from the left. The same light as the portraits,
  so the two sit together on a category page.
- Muted, desaturated, plain and unbranded. No packaging, no wrappers, no
  printed labels, and nothing that invites the model to draw a logo.
- Crisp and sharp, clean digital, no film grain.
- Close, but not so close that the product stops being recognisable.

Every product in the launch range has its own photograph. That matters more
than it sounds: a page selling cotton wool illustrated with a picture of a vial
is not a product page, it is a placeholder with a price on it. Where a shot is
shared, it is shared between two products of the same thing in the same
category (crepe and cohesive bandage, cotton wool balls and cotton wool rolls),
never across categories.

The older families still carry four views each, because those shots were made
as a set. The launch range carries one view each, and the product page drops
its thumbnail strip when there is only one image, rather than showing a single
thumbnail of the picture already on screen.
