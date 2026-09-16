import io, json, os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pagemeta as META
from shop import HEAD, FOOTER, LEARNCOLS, MENUCOLS, HEADER_VALS, REVEAL, SCRIPT_OPEN, MONO, WRAP, H1, H2, LEAD, CARD, crumbs, page, E
import pathlib
DOCS=str(pathlib.Path(__file__).resolve().parent.parent / 'docs')

EYE_L = ('<span style="display:inline-block;%s;font-size:12px;letter-spacing:.16em;text-transform:uppercase;'
         'color:#1C4034;border:1px solid rgba(28,64,52,.3);border-radius:1000px;padding:7px 13px;margin-bottom:20px">%%s</span>'%MONO)

CDN='https://d8j0ntlcm91z4.cloudfront.net/user_302vtY04kC9nbtUjJJAhLoDVMFw/'
SHOT_VIAL=CDN+'hf_20260912_014655_c87ec5d7-96f6-4729-b6ef-fc062184ab3f.png'
SHOT_NEEDLES=CDN+'hf_20260914_222009_74578d27-0f2f-4e67-bddc-bd5e151ef2fe.png'

def head_grid_open():
    return ('        <div data-gp-pagehead-grid style="display:grid;grid-template-columns:'
            'repeat(auto-fit,minmax(min(340px,100%),1fr));gap:clamp(28px,4vw,64px);align-items:center">\n')

def head_shot(src, alt):
    """The tools pages were the only two on the site with no photography at all,
    which made them read as a different product. One shot in the page head."""
    return ('          <div data-reveal style="border-radius:28px;overflow:hidden;background:#E4E4E2;aspect-ratio:3/2">\n'
            '            <img src="' + src + '" alt="' + alt + '" loading="lazy" '
            'style="width:100%;height:100%;object-fit:cover;display:block">\n'
            '          </div>\n        </div>\n')

# ---------------------------------------------------------------- drawn parts
def barrel_svg():
    """A U-100 barrel with the draw point filled live from the calculation."""
    o=['              <svg viewBox="0 0 640 118" width="100%" style="display:block;overflow:visible" role="img" aria-label="A U-100 insulin syringe barrel with the draw point marked">\n']
    a=o.append
    # plunger and flange
    a('                <path d="M10 59h34M14 41v36" stroke="#8FBFA6" stroke-width="3" stroke-linecap="round" fill="none"/>\n')
    a('                <rect x="44" y="47" width="16" height="24" rx="3" fill="#8FBFA6"/>\n')
    # barrel body
    a('                <rect x="60" y="41" width="500" height="36" rx="6" fill="rgba(250,250,250,.05)" stroke="#2A5245" stroke-width="2"/>\n')
    # the drawn volume
    a('                <rect x="60" y="41" width="{{ fillW }}" height="36" rx="6" fill="#8FBFA6" opacity=".55"/>\n')
    # needle
    a('                <path d="M560 59h34M594 59h34" stroke="#8FBFA6" stroke-width="3" stroke-linecap="round" fill="none"/>\n')
    # graduations, every 10 units, taller and labelled every 20
    for i in range(11):
        x=60+i*50
        major = (i % 2 == 0)
        a('                <path d="M%d 77v%d" stroke="#B7CFC3" stroke-width="%s" opacity="%s"/>\n'
          %(x, 13 if major else 8, '1.6' if major else '1.2', '.85' if major else '.5'))
        if major:
            a('                <text x="%d" y="108" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="12" fill="#B7CFC3">%d</text>\n'%(x,i*10))
    # the marker
    a('                <path d="M{{ markX }} 28v53" stroke="#FAFAFA" stroke-width="2.5" stroke-linecap="round"/>\n')
    a('                <circle cx="{{ markX }}" cy="26" r="5" fill="#FAFAFA"/>\n')
    a('              </svg>\n')
    a('              <div style="%s;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#8FBFA6;text-align:center;margin-top:14px">Draw to the mark</div>\n'%MONO)
    return ''.join(o)

def steps_svg():
    """Three drawn steps with the worked example under each."""
    G='stroke="#1C4034" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    art=[
      # vial plus water going in
      '<path d="M22 14h20M25 14v8a9 9 0 0 0-5 8v22a6 6 0 0 0 6 6h12a6 6 0 0 0 6-6V30a9 9 0 0 0-5-8v-8" %s/><path d="M20 38h24" %s/><path d="M56 12c0 0-7 8-7 12a7 7 0 0 0 14 0c0-4-7-12-7-12z" %s/>'%(G,G,G),
      # vial full, swirled
      '<path d="M22 14h20M25 14v8a9 9 0 0 0-5 8v22a6 6 0 0 0 6 6h12a6 6 0 0 0 6-6V30a9 9 0 0 0-5-8v-8" %s/><path d="M20 34c4 3 8 3 12 0s8-3 12 0" %s/><path d="M20 42c4 3 8 3 12 0s8-3 12 0" %s/>'%(G,G,G),
      # syringe with the mark
      '<path d="M8 32h8M12 24v16" %s/><path d="M16 26h34v12H16z" %s/><path d="M50 32h8M58 32h8" %s/><path d="M24 38v6M31 38v6M38 38v6" %s/><path d="M31 18v8" stroke="#1C4034" stroke-width="2.4" stroke-linecap="round"/><circle cx="31" cy="16" r="3.5" fill="#1C4034"/>'%(G,G,G,G),
    ]
    steps=[
      ('Add the water','Push the bacteriostatic water down the inside wall of the glass, not straight onto the powder.','10mg vial + 2mL water'),
      ('Work out the strength','What is in the vial divided by the water you added. This one number drives everything after it.','5mg per mL'),
      ('Draw to the mark','Your dose divided by the strength, then read off the barrel. A U-100 barrel counts to 100, not in millilitres.','1mg dose = 20 units'),
    ]
    o=['        <div data-reveal style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));gap:14px">\n']
    a=o.append
    for i,((t,b,ex),g) in enumerate(zip(steps,art)):
        a('          <div style="%s">\n'%CARD)
        a('            <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:18px">\n')
        a('              <svg viewBox="0 0 72 60" width="72" height="60" role="img" aria-label="%s">%s</svg>\n'%(E(t),g))
        a('              <span style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#59595A">Step %d</span>\n'%(MONO,i+1))
        a('            </div>\n')
        a('            <div style="font-family:\'Archivo\',sans-serif;font-weight:600;font-size:18px;letter-spacing:-.02em;margin-bottom:9px">%s</div>\n'%E(t))
        a('            <div style="font-size:15.5px;line-height:1.55;color:#3A3A38;margin-bottom:16px">%s</div>\n'%E(b))
        a('            <div style="%s;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#1C4034;background:#EDEDEB;border-radius:1000px;padding:9px 14px;display:inline-block">%s</div>\n'%(MONO,E(ex)))
        a('          </div>\n')
    a('        </div>\n')
    return ''.join(o)

# ---------------------------------------------------------------- calculator
def reconstitution():
    m=['<main>\n']; a=m.append
    a('    <section style="border-bottom:1px solid #E3E3E1">\n')
    a('      <div data-gp-pagehead style="max-width:1440px;margin:0 auto;padding:clamp(32px,5vw,64px) clamp(20px,5vw,72px) clamp(40px,5vw,56px)">\n')
    a(crumbs([('Home','/'),('Tools','/tools/reconstitution-calculator'),('Peptide reconstitution calculator',None)]))
    a(head_grid_open())
    a('        <div style="max-width:54ch">\n          %s\n'%(EYE_L%'Free tool'))
    a('          <h1 style="%s">Peptide reconstitution calculator</h1>\n'%H1)
    a('          <p style="%s">Enter what is in the vial, how much bacteriostatic water you are adding and the dose you were given. You get the concentration, the volume to draw, and the exact mark to line up on a U-100 insulin syringe.</p>\n'%LEAD)
    a('          <p style="%s;margin-top:14px">We do not decide your dose. Your prescriber does that. This turns the number they gave you into a mark on a barrel.</p>\n        </div>\n'%LEAD)
    a(head_shot(SHOT_VIAL, 'A glass vial beside a carton and foil swab sachets'))
    a('      </div>\n    </section>\n\n')
    # calculator
    a('    <section id="calc" style="border-bottom:1px solid #E3E3E1">\n      <div style="max-width:1440px;margin:0 auto;padding:clamp(28px,4vw,44px) clamp(20px,5vw,72px) clamp(48px,7vw,96px)">\n')
    a('        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:clamp(20px,3vw,40px);align-items:start">\n')
    a('          <div style="display:flex;flex-direction:column;gap:12px">\n')
    for key,label,count in [('strengths','How much is in the vial?',5),('waters','How much water are you adding?',4)]:
        a('            <div style="border:1px solid #E3E3E1;background:#F2F2F1;border-radius:22px;padding:24px 22px">\n')
        a('              <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;margin-bottom:14px">%s</div>\n'%(MONO,label))
        a('              <div style="display:flex;flex-wrap:wrap;gap:8px">\n')
        a('                <sc-for list="{{ %s }}" as="o" hint-placeholder-count="%d">\n'%(key,count))
        a('                  <button type="button" onClick="{{ o.pick }}" aria-pressed="{{ o.on }}" style="cursor:pointer;font-family:\'Archivo\',sans-serif;font-size:15px;font-weight:500;border:1px solid {{ o.border }};background:{{ o.bg }};color:{{ o.fg }};border-radius:1000px;padding:11px 18px">{{ o.label }}</button>\n')
        a('                </sc-for>\n              </div>\n            </div>\n')
    # dose stepper
    a('            <div style="border:1px solid #E3E3E1;background:#F2F2F1;border-radius:22px;padding:24px 22px">\n')
    a('              <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;margin-bottom:6px">The dose you were prescribed</div>\n'%MONO)
    a('              <div style="font-size:15px;line-height:1.55;color:#3A3A38;margin-bottom:16px">Your prescriber sets this. We only convert it.</div>\n')
    a('              <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">\n')
    a('                <div style="display:flex;align-items:center;gap:6px;border:1px solid #E3E3E1;border-radius:1000px;padding:6px 10px;background:#FAFAFA">\n')
    a('                  <button type="button" onClick="{{ doseDown }}" aria-label="Smaller dose" style="border:0;background:none;cursor:pointer;font-size:19px;width:34px;height:34px;color:#0E0E0E">&minus;</button>\n')
    a('                  <span style="%s;font-size:15px;min-width:74px;text-align:center">{{ doseLabel }}</span>\n'%MONO)
    a('                  <button type="button" onClick="{{ doseUp }}" aria-label="Larger dose" style="border:0;background:none;cursor:pointer;font-size:19px;width:34px;height:34px;color:#0E0E0E">+</button>\n')
    a('                </div>\n                <span style="%s;font-size:12px;color:#59595A">{{ doseMcg }}</span>\n'%MONO)
    a('              </div>\n            </div>\n          </div>\n')
    # results panel
    a('          <div style="background:#143026;color:#FAFAFA;border-radius:22px;overflow:hidden">\n')
    a('            <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;padding:20px 24px;border-bottom:1px solid #2A5245">\n')
    a('              <span style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#8FBFA6">What to draw</span>\n'%MONO)
    a('              <span style="%s;font-size:11px;color:#B7CFC3">{{ mix }}</span>\n            </div>\n'%MONO)
    a('            <div style="padding:26px 24px 20px;border-bottom:1px solid #2A5245">\n')
    a('              <div style="%s;font-size:clamp(44px,7vw,64px);line-height:1;color:#FAFAFA;text-align:center">{{ units }}</div>\n'%MONO)
    a('              <div style="font-size:15.5px;color:#B7CFC3;margin:10px 0 22px;text-align:center">units on a U-100 insulin syringe</div>\n')
    a(barrel_svg())
    a('            </div>\n')
    a('            <div style="padding:8px 24px 4px">\n')
    a('              <sc-for list="{{ rows }}" as="r" hint-placeholder-count="4">\n')
    a('                <div style="display:flex;justify-content:space-between;gap:20px;padding:16px 0;border-bottom:1px solid #2A5245;align-items:baseline">\n')
    a('                  <span style="font-size:15.5px;color:#B7CFC3">{{ r.k }}</span>\n')
    a('                  <span style="%s;font-size:15px;color:#FAFAFA;text-align:right">{{ r.v }}</span>\n'%MONO)
    a('                </div>\n              </sc-for>\n            </div>\n')
    a('            <div style="padding:22px 24px 26px">\n')
    a('              <div style="font-size:15px;line-height:1.6;color:#B7CFC3;margin-bottom:20px">{{ note }}</div>\n')
    a('              <div style="display:flex;gap:12px;flex-wrap:wrap">\n')
    a('                <a href="/shop/diluents-swabs/bacteriostatic-water" data-cta style="background:#8FBFA6;color:#143026;border-radius:1000px;padding:14px 26px;font-size:15.5px;font-weight:600">Bacteriostatic water</a>\n')
    a('                <a href="/shop/syringes-needles/u-100-insulin-syringes" data-cta style="border:1px solid rgba(143,191,166,.55);color:#FAFAFA;border-radius:1000px;padding:14px 26px;font-size:15.5px;font-weight:600">U-100 syringes</a>\n')
    a('              </div>\n            </div>\n          </div>\n        </div>\n')
    a('        <div style="%s;font-size:11.5px;color:#59595A;margin-top:28px;line-height:1.7;max-width:80ch">Nothing you enter is stored, sent to us or attached to an order. The calculation runs in this browser tab and is gone when you close it. This tool converts a dose you were already given into a volume. It does not suggest a dose, and it is not medical advice.</div>\n'%MONO)
    a('      </div>\n    </section>\n\n')
    # safety layer, which is the whole editorial reason this page exists
    a('    <section style="background:#1C4034;color:#FAFAFA;border-bottom:1px solid #2A5245">\n      <div style="%s">\n'%WRAP)
    a('        <div style="max-width:52ch;margin-bottom:clamp(28px,4vw,40px)">\n')
    a('          <span style="display:inline-block;%s;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#143026;background:#8FBFA6;border-radius:1000px;padding:8px 14px;margin-bottom:22px">Read this first</span>\n'%MONO)
    a('          <h2 style="%s;color:#FAFAFA">The arithmetic is the easy part.</h2>\n'%H2)
    a('          <p style="margin:0;font-size:17px;line-height:1.55;color:#DCE5E1">Every other calculator stops at the number. These are the things that actually go wrong, and none of them are arithmetic.</p>\n        </div>\n')
    a('        <div data-reveal style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:14px">\n')
    for t,b in [
      ('The maths is only as good as the label',
       'Every number here assumes the vial contains what it says it contains. A vial from outside the regulated supply chain carries no such assurance, and no calculator can tell you otherwise. If you cannot trace what is in it, the output of this tool is meaningless.'),
      ('Bacteriostatic is not sterile water',
       'Bacteriostatic water is preserved with benzyl alcohol, which is what lets a vial keep for weeks once broached. Sterile water has no preservative and is single use the moment you open it. Substituting one for the other is a genuine infection risk, not a technicality.'),
      ('Swab both stoppers, every time',
       'The powder vial and the water vial. A stopper looks clean and is not. This is the single cheapest thing you can do to avoid an abscess, and it is the step most often skipped once something becomes routine.'),
      ('Never share a vial or a needle',
       'Not with a partner, not with a friend on the same protocol. A multi-dose vial that more than one person draws from is a bloodborne transmission route. Needles are single use and blunt on first pass.'),
      ('Under two units cannot be read',
       'If your dose lands below about two units on a U-100 barrel, you cannot draw it accurately and neither can anyone else. Adding more water spreads the same dose across more units. The tool flags this when it happens.'),
      ('Used needles are not household waste',
       'A sharps container is not optional and it is not a suggestion. Kerbside disposal is prohibited in every Australian state, and the rules for a full container differ by state.')]:
        a('          <div style="background:#143026;border:1px solid #2A5245;border-radius:22px;padding:26px 24px">\n')
        a('            <div style="font-family:\'Archivo\',sans-serif;font-weight:600;font-size:18px;letter-spacing:-.02em;margin-bottom:10px;color:#FAFAFA">%s</div>\n'%E(t))
        a('            <div style="font-size:15.5px;line-height:1.55;color:#B7CFC3">%s</div>\n          </div>\n'%E(b))
    a('        </div>\n')
    a('        <div style="%s;font-size:12px;color:#B7CFC3;margin-top:28px;line-height:1.8;max-width:80ch">Good Practice Supply sells consumables. We do not supply peptides, hormones or any prescription medicine, and we take no position on what you have been prescribed. Anything you inject should come from your prescriber through a regulated pharmacy. Nothing on this page is medical advice.</div>\n'%MONO)
    a('      </div>\n    </section>\n\n')
    # what we supply
    a('    <section style="background:#F2F2F1;border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:14px">\n')
    for t,b in [('What we supply','Bacteriostatic water, insulin syringes, vial adapters, drawing-up needles and swabs. All of it consumables, all priced on the page without an account.'),
                ('What we do not','Whatever goes in the vial. Good Practice Supply does not stock peptides, hormones or any prescription medicine, and this calculator does not care what is in there. It only does the arithmetic.')]:
        a('          <div style="%s">\n            <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;margin-bottom:16px">%s</div>\n'%(CARD,MONO,E(t)))
        a('            <div style="font-size:15.5px;line-height:1.55;color:#3A3A38">%s</div>\n          </div>\n'%E(b))
    a('        </div>\n      </div>\n    </section>\n\n')
    # how it works, drawn rather than described
    a('    <section style="border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <div style="max-width:50ch;margin-bottom:clamp(28px,4vw,44px)">\n')
    a('          <h2 style="%s">Three steps, with a worked example.</h2>\n'%H2)
    a('          <p style="%s">A 10mg vial, 2mL of water and a 1mg dose. The numbers under each step are that example.</p>\n        </div>\n'%LEAD)
    a(steps_svg())
    a('      </div>\n    </section>\n\n')
    # cta
    a('    <section style="background:#1C4034;color:#FAFAFA">\n      <div style="%s;display:flex;justify-content:space-between;gap:32px;flex-wrap:wrap;align-items:center">\n'%WRAP)
    a('        <div>\n          <h2 style="%s;color:#FAFAFA">Not sure which syringe reads your dose best?</h2>\n'%H2)
    a('          <p style="margin:0;font-size:16.5px;line-height:1.5;color:#B7CFC3;max-width:46ch">The Gauge Finder covers thickness and length. This one covers what goes in the barrel.</p>\n        </div>\n')
    a('        <a href="/gauge-finder" data-cta style="background:#8FBFA6;color:#143026;border-radius:1000px;padding:16px 30px;font-size:16px;font-weight:600;white-space:nowrap">Open the Gauge Finder</a>\n')
    a('      </div>\n    </section>\n\n  </main>')

    script="""%s
class Component extends DCLogic {
  state = { menu: null, strength: 2, water: 1, dose: 5 };

%s
  renderVals() {
    const s = this.state;
    const STRENGTHS = [2, 5, 10, 15, 30];          // mg in the vial
    const WATERS = [1, 2, 3, 5];                    // mL of bacteriostatic water
    const DOSES = [0.1, 0.125, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10];
    const sel = on => ({
      bg: on ? '#0E0E0E' : '#FAFAFA',
      fg: on ? '#FAFAFA' : '#0E0E0E',
      border: on ? '#0E0E0E' : '#E3E3E1'
    });
    const mg = STRENGTHS[s.strength];
    const mL = WATERS[s.water];
    const dose = DOSES[s.dose];

    const conc = mg / mL;                 // mg per mL
    const volume = dose / conc;           // mL to draw
    const units = volume * 100;           // a U-100 barrel is marked in hundredths of a mL
    const dosesPerVial = Math.floor(mg / dose);
    const trim = n => Number(n.toFixed(2)).toString();

    // A U-100 barrel cannot be read finer than about half a unit.
    const readable = units >= 2 && units <= 100;

    return {
%s
      cartCount: String(this.state.cart || 0),

      strengths: STRENGTHS.map((v, i) => {
        const c = sel(s.strength === i);
        return { label: v + 'mg', on: s.strength === i, bg: c.bg, fg: c.fg, border: c.border,
                 pick: () => this.setState({ strength: i }) };
      }),
      waters: WATERS.map((v, i) => {
        const c = sel(s.water === i);
        return { label: v + 'mL', on: s.water === i, bg: c.bg, fg: c.fg, border: c.border,
                 pick: () => this.setState({ water: i }) };
      }),
      doseLabel: trim(dose) + 'mg',
      doseMcg: (dose * 1000) + ' micrograms',
      doseUp: () => this.setState(p => ({ dose: Math.min(DOSES.length - 1, p.dose + 1) })),
      doseDown: () => this.setState(p => ({ dose: Math.max(0, p.dose - 1) })),

      units: trim(units),
      // barrel geometry: 500 user units of SVG span 0 to 100 on the scale
      fillW: String(Math.max(0, Math.min(1, units / 100)) * 500),
      markX: String(60 + Math.max(0, Math.min(1, units / 100)) * 500),
      mix: mg + 'mg in ' + mL + 'mL',
      rows: [
        { k: 'Concentration', v: trim(conc) + 'mg per mL' },
        { k: 'Volume to draw', v: trim(volume) + 'mL' },
        { k: 'Doses in the vial', v: String(dosesPerVial) },
        { k: 'Bacteriostatic water', v: Math.ceil(mL / 10) + ' × 10mL vial' }
      ],
      note: readable
        ? 'Draw to ' + trim(units) + ' on a U-100 barrel. Check it against the markings in good light before you inject.'
        : (units < 2
            ? 'Under two units is too small to read accurately on a U-100 barrel. Adding more water spreads the same dose across more units and makes it readable.'
            : 'Over one hundred units will not fit in a 1mL barrel. Using less water concentrates the dose into a volume you can draw.'),

%s
%s
    };
  }
}
</script>"""%(SCRIPT_OPEN, REVEAL, HEADER_VALS, LEARNCOLS, MENUCOLS)
    return ''.join(m), script

# ---------------------------------------------------------------- gauge chart
GAUGES = [
 ('14G','2.11','Orange','Large bore transfer. Rarely used outside a hospital.','draw'),
 ('16G','1.65','White','Transfer and rapid infusion.','draw'),
 ('18G','1.27','Pink','Drawing up a thick oil. Too wide to inject with.','draw'),
 ('19G','1.07','Cream','Drawing up. Also blunt fill needles.','draw'),
 ('20G','0.91','Yellow','Drawing up, or intramuscular in a large muscle.','draw'),
 ('21G','0.82','Green','The common drawing-up gauge. Also venepuncture.','draw'),
 ('22G','0.72','Black','Intramuscular, or drawing a thinner solution.','im'),
 ('23G','0.64','Blue','Intramuscular. A frequent choice for the deltoid.','im'),
 ('25G','0.51','Orange','Intramuscular in a smaller muscle, or intradermal.','im'),
 ('26G','0.46','Brown','Fine intramuscular and subcutaneous.','sub'),
 ('27G','0.41','Grey','Subcutaneous. Noticeably more comfortable.','sub'),
 ('29G','0.34','Red','Insulin syringes. Fills fastest of the fine gauges.','insulin'),
 ('30G','0.31','Yellow','Insulin syringes and pen needles. The middle choice.','insulin'),
 ('31G','0.26','Violet','Insulin syringes and pen needles. Least sensation.','insulin'),
 ('32G','0.23','Bright green','Pen needles. The finest in common use.','insulin'),
 ('33G','0.21','Blue','Speciality pen needles.','insulin'),
 ('34G','0.18','Ochre','The finest made. Speciality use only.','insulin'),
]
def gauge_chart():
    m=['<main>\n']; a=m.append
    a('    <section style="border-bottom:1px solid #E3E3E1">\n')
    a('      <div data-gp-pagehead style="max-width:1440px;margin:0 auto;padding:clamp(32px,5vw,64px) clamp(20px,5vw,72px) clamp(40px,5vw,56px)">\n')
    a(crumbs([('Home','/'),('Learn','/learn'),('Needle gauge chart',None)]))
    a(head_grid_open())
    a('        <div style="max-width:54ch">\n          %s\n'%(EYE_L%'Reference'))
    a('          <h1 style="%s">Needle gauge chart</h1>\n'%H1)
    a('          <p style="%s">Every gauge in common use, its outer diameter in millimetres, the ISO hub colour and what it is actually for. The scale runs backwards: the higher the number, the thinner the needle.</p>\n        </div>\n'%LEAD)
    a(head_shot(SHOT_NEEDLES, 'Seven capped needles laid side by side, largest to smallest'))
    a('      </div>\n    </section>\n\n')
    a('    <section id="chart" style="border-bottom:1px solid #E3E3E1">\n      <div style="max-width:1440px;margin:0 auto;padding:clamp(28px,4vw,44px) clamp(20px,5vw,72px) clamp(48px,7vw,96px)">\n')
    a('        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:24px">\n')
    a('          <sc-for list="{{ filters }}" as="fl" hint-placeholder-count="5">\n')
    a('            <button type="button" onClick="{{ fl.pick }}" aria-pressed="{{ fl.on }}" data-chip style="cursor:pointer;font-family:\'Archivo\',sans-serif;font-size:15px;font-weight:500;border:1px solid {{ fl.border }};background:{{ fl.bg }};color:{{ fl.fg }};border-radius:1000px;padding:10px 18px">{{ fl.label }}</button>\n')
    a('          </sc-for>\n        </div>\n')
    a('        <div style="overflow-x:auto;border:1px solid #E3E3E1;border-radius:22px;background:#FAFAFA">\n')
    a('          <div style="min-width:640px">\n')
    a('            <div style="display:grid;grid-template-columns:90px 120px 130px 1fr;gap:0;background:#F2F2F1;border-bottom:1px solid #E3E3E1">\n')
    for h in ['Gauge','Outer diameter','Hub colour','Typical use']:
        a('              <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;padding:16px 18px">%s</div>\n'%(MONO,h))
    a('            </div>\n')
    for g,od,col,use,tag in GAUGES:
        a('            <div data-tag="%s" style="display:grid;grid-template-columns:90px 120px 130px 1fr;gap:0;border-bottom:1px solid #E3E3E1;align-items:center">\n'%tag)
        a('              <div style="%s;font-size:15px;color:#0E0E0E;padding:16px 18px">%s</div>\n'%(MONO,g))
        a('              <div style="%s;font-size:14px;color:#3A3A38;padding:16px 18px">%smm</div>\n'%(MONO,od))
        a('              <div style="font-size:15px;color:#3A3A38;padding:16px 18px">%s</div>\n'%E(col))
        a('              <div style="font-size:15px;line-height:1.5;color:#3A3A38;padding:16px 18px">%s</div>\n            </div>\n'%E(use))
    a('          </div>\n        </div>\n')
    a('        <div style="%s;font-size:11.5px;color:#59595A;margin-top:24px;line-height:1.7;max-width:80ch">Hub colours follow ISO 6009. Manufacturers occasionally differ, so read the carton rather than trusting the colour alone. Diameters are nominal outer diameter.</div>\n'%MONO)
    a('      </div>\n    </section>\n\n')
    # shop the gauges
    a('    <section style="background:#F2F2F1;border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <div style="max-width:48ch;margin-bottom:clamp(28px,4vw,40px)">\n          %s\n'%(EYE_L%'Shop the gauges'))
    a('          <h2 style="%s">Once you know the number.</h2>\n'%H2)
    a('          <p style="%s">Every gauge in the chart, priced and in stock, with no account needed to see what it costs.</p>\n        </div>\n'%LEAD)
    a('        <div data-reveal style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));gap:14px">\n')
    for name,blurb,href in [
      ('Insulin syringes','29G, 30G and 31G with the needle fixed and a unit scale.','/shop/syringes-needles/u-100-insulin-syringes'),
      ('Pen needles','32G 4mm through 31G 8mm, universal thread.','/shop/syringes-needles/pen-needles'),
      ('Hypodermic needles','23G, 25G and 27G, ISO colour coded.','/shop/syringes-needles/hypodermic-needles'),
      ('Drawing-up needles','18G blunt fill and 21G sharp fill.','/shop/syringes-needles/drawing-up-needles')]:
        a('          <a href="%s" data-card style="%s;display:block" style-hover="border-color:#0E0E0E">\n'%(href,CARD))
        a('            <span style="display:block;font-family:\'Archivo\',sans-serif;font-weight:600;font-size:17px;letter-spacing:-.02em;margin-bottom:8px">%s</span>\n'%E(name))
        a('            <span style="display:block;font-size:15px;line-height:1.5;color:#3A3A38">%s</span>\n          </a>\n'%E(blurb))
    a('        </div>\n      </div>\n    </section>\n\n')
    a('    <section style="background:#1C4034;color:#FAFAFA">\n      <div style="%s;display:flex;justify-content:space-between;gap:32px;flex-wrap:wrap;align-items:center">\n'%WRAP)
    a('        <div>\n          <h2 style="%s;color:#FAFAFA">Still not sure which one you want?</h2>\n'%H2)
    a('          <p style="margin:0;font-size:16.5px;line-height:1.5;color:#B7CFC3;max-width:46ch">Three plain questions, no medical words, and the Gauge Finder picks the gauge and the length for you.</p>\n        </div>\n')
    a('        <a href="/gauge-finder" data-cta style="background:#8FBFA6;color:#143026;border-radius:1000px;padding:16px 30px;font-size:16px;font-weight:600;white-space:nowrap">Open the Gauge Finder</a>\n')
    a('      </div>\n    </section>\n\n  </main>')
    script="""%s
class Component extends DCLogic {
  state = { menu: null, filter: 'all' };

%s
  renderVals() {
    const f = this.state.filter;
    const FILTERS = [
      { tag: 'all', label: 'Every gauge' },
      { tag: 'draw', label: 'Drawing up' },
      { tag: 'im', label: 'Intramuscular' },
      { tag: 'sub', label: 'Subcutaneous' },
      { tag: 'insulin', label: 'Insulin & pen' }
    ];
    return {
%s
      cartCount: String(this.state.cart || 0),
      filters: FILTERS.map(o => ({
        label: o.label,
        on: f === o.tag,
        bg: f === o.tag ? '#0E0E0E' : '#FAFAFA',
        fg: f === o.tag ? '#FAFAFA' : '#0E0E0E',
        border: f === o.tag ? '#0E0E0E' : '#E3E3E1',
        pick: () => this.setState({ filter: o.tag })
      })),

%s
%s
    };
  }

  componentDidUpdate() { this.syncFilter(); }

  syncFilter() {
    // The full table is rendered server side so it stays crawlable.
    const f = this.state.filter;
    document.querySelectorAll('#chart [data-tag]').forEach(el => {
      el.style.display = (f === 'all' || el.getAttribute('data-tag') === f) ? '' : 'none';
    });
  }
}
</script>"""%(SCRIPT_OPEN, REVEAL, HEADER_VALS, LEARNCOLS, MENUCOLS)
    return ''.join(m), script

def main():
    os.makedirs(DOCS+'/tools',exist_ok=True)
    os.makedirs(DOCS+'/learn',exist_ok=True)
    mn,sc=reconstitution()
    io.open(DOCS+'/tools/reconstitution-calculator.html','w',encoding='utf-8').write(
        page('Peptide reconstitution calculator, mg to units on a syringe',mn,sc,
             head_extra=META.blocks('/tools/reconstitution-calculator',
                 META.FIXED['/tools/reconstitution-calculator']),
             path='/tools/reconstitution-calculator'))
    mn,sc=gauge_chart()
    io.open(DOCS+'/learn/needle-gauge-chart.html','w',encoding='utf-8').write(
        page('Needle gauge chart, sizes in mm with hub colours',mn,sc,
             head_extra=META.blocks('/learn/needle-gauge-chart',
                 META.FIXED['/learn/needle-gauge-chart']),
             path='/learn/needle-gauge-chart'))
    print('wrote 2 pages')

main()
