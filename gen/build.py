import io, json, os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo as SEO
import pagemeta as META
from content import PAGES
from prodmap import PROD

import pathlib
DOCS=str(pathlib.Path(__file__).resolve().parent.parent / 'docs')
SHELL=SEO.strip_headmeta(io.open(DOCS+'/about.html',encoding='utf-8').read())
SP='<div data-gp-spacer aria-hidden="true"></div>'
HEAD=SHELL[:SHELL.find(SP)+len(SP)]
FOOTER=SHELL[SHELL.find('<footer'):SHELL.find('</footer>')+9]
E=html.escape
from inline import EL

MONO="font-family:'IBM Plex Mono',monospace;font-weight:500"
def eyebrow(t, dark=False):
    if dark:
        return ('<span style="display:inline-block;%s;font-size:12px;letter-spacing:.16em;text-transform:uppercase;'
                'color:#143026;background:#8FBFA6;border-radius:1000px;padding:8px 14px;margin-bottom:22px">%s</span>'%(MONO,E(t)))
    return ('<span style="display:inline-block;%s;font-size:12px;letter-spacing:.16em;text-transform:uppercase;'
            'color:#1C4034;border:1px solid rgba(28,64,52,.3);border-radius:1000px;padding:7px 13px;margin-bottom:20px">%s</span>'%(MONO,E(t)))

H1="font-family:'Archivo',sans-serif;font-weight:600;font-size:clamp(32px,3.8vw,52px);letter-spacing:-.035em;line-height:1.02;margin:0 0 16px"
H2="font-family:'Archivo',sans-serif;font-weight:600;font-size:clamp(26px,3vw,40px);letter-spacing:-.03em;line-height:1.05;margin:0 0 16px"
H3="font-family:'Archivo',sans-serif;font-weight:600;font-size:clamp(22px,2.4vw,30px);letter-spacing:-.025em;margin:0"
LEAD="margin:0 0 16px;font-size:17.5px;line-height:1.55;color:#3A3A38;max-width:46ch"
CARD="background:#FAFAFA;border:1px solid #E3E3E1;border-radius:22px;padding:26px 24px"
CARDT="font-family:'Archivo',sans-serif;font-weight:600;font-size:18px;letter-spacing:-.02em;margin-bottom:9px"
CARDB="font-size:15.5px;line-height:1.55;color:#3A3A38"
WRAP='max-width:1440px;margin:0 auto;padding:clamp(48px,7vw,96px) clamp(20px,5vw,72px)'

KIT_CAT = {'glp-1-injections':'syringes-needles','trt-injections':'syringes-needles',
           'peptide-reconstitution':'diluents-swabs','diabetes-at-home':'diagnostics',
           'wound-care-at-home':'wound-care','clinic-fit-out':'clinic-disposal'}

def build_main(p):
    o=[]
    a=o.append
    a('<main>\n')
    # page head
    a('    <section style="border-bottom:1px solid #E3E3E1">\n')
    a('      <div data-gp-pagehead style="max-width:1440px;margin:0 auto;padding:clamp(32px,5vw,64px) clamp(20px,5vw,72px) clamp(48px,7vw,96px)">\n')
    a('        <div data-gp-pagehead-grid style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:clamp(28px,4vw,64px);align-items:center">\n')
    a('          <div>\n            %s\n'%eyebrow(p['eyebrow']))
    a('            <h1 style="%s">%s</h1>\n'%(H1,E(p['h1'])))
    for i,l in enumerate(p['lead']):
        a('            <p style="%s">%s</p>\n'%(LEAD if i<len(p['lead'])-1 else LEAD.replace('0 0 16px','0'),EL(l)))
    # The answer, straight after the lead rather than halfway down the page. A
    # reader skimming and a model looking for something to quote want the same
    # thing: the sentence that answers the question the headline asks.
    a('            <div style="margin-top:22px;padding:16px 18px;background:#EDEDEB;border-radius:16px;max-width:46ch">\n')
    a('              <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;margin-bottom:8px">The short answer</div>\n'%MONO)
    a('              <p style="margin:0;font-size:16px;line-height:1.5;color:#0E0E0E">%s</p>\n'%E(p['answer']))
    a('            </div>\n')
    a('          </div>\n')
    a('          <div style="border-radius:28px;overflow:hidden;background:#EDEDEB;aspect-ratio:4/3">\n')
    a('            <img src="%s" alt="%s" style="width:100%%;height:100%%;object-fit:cover">\n'%(p['img'],E(p['alt'])))
    a('          </div>\n        </div>\n      </div>\n    </section>\n\n')
    # what we supply / what we do not
    a('    <section style="background:#F2F2F1;border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:14px">\n')
    a('          <div style="%s">\n            <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;margin-bottom:16px">What we supply</div>\n'%(CARD,MONO))
    a('            <div style="%s">%s</div>\n          </div>\n'%(CARDB,E(p['supplies'])))
    a('          <div style="%s">\n            <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;margin-bottom:16px">What comes from your pharmacy</div>\n'%(CARD,MONO))
    a('            <div style="%s">%s</div>\n          </div>\n        </div>\n      </div>\n    </section>\n\n'%(CARDB,E(p['pharmacy'])))
    # the kit
    a('    <section id="kit" style="border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <div style="max-width:52ch;margin-bottom:clamp(32px,4vw,48px)">\n          %s\n'%eyebrow('The kit'))
    a('          <h2 style="%s">%s</h2>\n'%(H2,E(p['sel_title'])))
    a('          <p style="%s">Set it below and the order follows. Each line shows how long a pack lasts at that rate, so you can see what is a monthly buy and what is a once a year one.</p>\n        </div>\n'%LEAD.replace('0 0 16px','0'))
    a('        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:clamp(20px,3vw,40px);align-items:start">\n')
    # selector
    a('          <div style="border:1px solid #E3E3E1;background:#F2F2F1;border-radius:22px;padding:24px 22px">\n')
    a('            <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;margin-bottom:16px">%s</div>\n'%(MONO,E(p['sel_title'])))
    a('            <div style="display:flex;flex-wrap:wrap;gap:8px">\n')
    a('              <sc-for list="{{ freqOptions }}" as="o" hint-placeholder-count="%d">\n'%len(p['sel']))
    a('                <button type="button" onClick="{{ o.pick }}" aria-pressed="{{ o.on }}" style="cursor:pointer;font-family:\'Archivo\',sans-serif;font-size:15px;font-weight:500;border:1px solid {{ o.border }};background:{{ o.bg }};color:{{ o.fg }};border-radius:1000px;padding:11px 18px">{{ o.label }}</button>\n')
    a('              </sc-for>\n            </div>\n')
    a('            <div style="font-size:15.5px;line-height:1.55;color:#3A3A38;margin-top:20px">{{ note }}</div>\n')
    a('          </div>\n')
    # forest kit panel
    a('          <div style="background:#143026;color:#FAFAFA;border-radius:22px;overflow:hidden">\n')
    a('            <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;padding:20px 24px;border-bottom:1px solid #2A5245">\n')
    a('              <span style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#8FBFA6">What to order</span>\n'%MONO)
    a('              <span style="%s;font-size:11px;color:#B7CFC3">{{ itemCount }}</span>\n            </div>\n'%MONO)
    a('            <div style="padding:8px 24px 4px">\n')
    a('              <sc-for list="{{ rows }}" as="r" hint-placeholder-count="%d">\n'%len(p['kit']))
    a('                <a href="{{ r.href }}" style="display:flex;justify-content:space-between;gap:20px;padding:16px 0;border-bottom:1px solid #2A5245;align-items:baseline;color:inherit" style-hover="background:rgba(143,191,166,.07)">\n')
    a('                  <span style="flex:1 1 auto">\n')
    a('                    <span style="display:block;font-size:15.5px;color:#FAFAFA;margin-bottom:4px">{{ r.name }}</span>\n')
    a('                    <span style="display:block;font-size:14px;line-height:1.5;color:#B7CFC3">{{ r.spec }}</span>\n')
    a('                    <span style="display:block;%s;font-size:12px;color:#8FBFA6;margin-top:6px">{{ r.qty }}</span>\n'%MONO)
    a('                    <span style="display:block;font-size:13.5px;color:#B7CFC3;margin-top:4px">{{ r.lasts }}</span>\n')
    a('                  </span>\n')
    a('                  <span style="%s;font-size:15px;color:#FAFAFA;text-align:right;white-space:nowrap">{{ r.price }}</span>\n'%MONO)
    a('                </a>\n              </sc-for>\n            </div>\n')
    a('            <div style="padding:20px 24px 26px">\n')
    a('              <div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px;margin-bottom:20px">\n')
    a('                <span style="font-size:16px;color:#DCE5E1">Order total</span>\n')
    a('                <span style="%s;font-size:22px;color:#FAFAFA">{{ total }}</span>\n              </div>\n'%MONO)
    a('              <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center">\n')
    a('                <a href="/shop/%s" data-cta style="background:#8FBFA6;color:#143026;border-radius:1000px;padding:14px 26px;font-size:15.5px;font-weight:600">Shop the whole kit</a>\n'%KIT_CAT[p['slug']])
    a('                <a href="/always-stocked" style="%s;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#B7CFC3;border-bottom:1px solid #2A5245;padding-bottom:3px">Or set it to repeat</a>\n'%MONO)
    a('              </div>\n            </div>\n          </div>\n        </div>\n')
    a('        <div style="%s;font-size:11.5px;color:#59595A;margin-top:28px;line-height:1.7;max-width:78ch">Quantities are a starting point, not a prescription. Your prescriber sets your dose, your route and your schedule. Where those differ from anything here, follow them.</div>\n'%MONO)
    a('      </div>\n    </section>\n\n')
    # A wide photograph between the kit and the reasoning. These pages ran four
    # card rows deep off a single product shot, which read as a different site
    # to the homepage.
    a('    <section style="border-bottom:1px solid #E3E3E1">\n')
    a('      <div style="background:#EDEDEB;overflow:hidden;height:clamp(200px,30vw,400px)">\n')
    a('        <img src="%s" alt="%s" loading="lazy" style="width:100%%;height:100%%;object-fit:cover;display:block">\n'%(p['scene'],E(p['scene_alt'])))
    a('      </div>\n    </section>\n\n')
    # why
    a('    <section style="background:#F2F2F1;border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <h2 style="%s">%s</h2>\n'%(H2.replace('0 0 16px','0 0 clamp(28px,4vw,40px)'),E(p['why_title'])))
    a('        <div data-reveal style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(240px,100%),1fr));gap:14px">\n')
    for i,(t,b) in enumerate(p['why']):
        a('          <div style="%s">\n'%CARD)
        a('            <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;margin-bottom:16px">%02d</div>\n'%(MONO,i+1))
        a('            <div style="%s">%s</div>\n            <div style="%s">%s</div>\n          </div>\n'%(CARDT,E(t),CARDB,E(b)))
    a('        </div>\n      </div>\n    </section>\n\n')
    # faq
    a('    <section style="border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr));gap:clamp(28px,4vw,64px);align-items:start">\n')
    a('          <div>\n            %s\n            <h2 style="%s">Questions people actually ask.</h2>\n'%(eyebrow('FAQ'),H2))
    a('            <p style="%s">If yours is not here, the contact form routes straight to the team that can answer it.</p>\n          </div>\n'%LEAD.replace('0 0 16px','0'))
    a('          <div style="border-top:1px solid #E3E3E1">\n')
    for q,ans in p['faq']:
        a('            <div style="padding:22px 0;border-bottom:1px solid #E3E3E1">\n')
        a('              <div style="%s">%s</div>\n'%(CARDT,E(q)))
        a('              <div style="%s">%s</div>\n            </div>\n'%(CARDB,E(ans)))
    a('          </div>\n        </div>\n      </div>\n    </section>\n\n')
    # learn
    a('    <section style="background:#F2F2F1;border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:22px">\n')
    a('          <h3 style="%s">Read the background</h3>\n'%H3)
    a('          <a href="/learn" data-link style="font-size:15px;font-weight:600;border-bottom:1.5px solid #C4C4C2;padding-bottom:3px;white-space:nowrap">All guides <span data-arrow>&rarr;</span></a>\n        </div>\n')
    a('        <div data-reveal style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));gap:14px">\n')
    for meta,t,b in p['learn']:
        a('          <a href="/learn" data-card style="%s;display:flex;flex-direction:column;gap:34px" style-hover="border-color:#0E0E0E">\n'%CARD)
        a('            <span style="%s;font-size:11.5px;color:#59595A">%s</span>\n'%(MONO,E(meta)))
        a('            <span>\n              <span style="display:block;%s;line-height:1.25">%s</span>\n'%(CARDT.replace('font-size:18px','font-size:19px'),E(t)))
        a('              <span style="display:block;%s">%s</span>\n            </span>\n          </a>\n'%(CARDB,E(b)))
    a('        </div>\n      </div>\n    </section>\n\n')
    # cta band
    a('    <section style="background:#1C4034;color:#FAFAFA">\n      <div style="%s">\n'%WRAP)
    a('        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr));gap:clamp(28px,4vw,64px);align-items:center">\n')
    a('          <div>\n            %s\n'%eyebrow('Not sure yet', dark=True))
    a('            <h2 style="%s;color:#FAFAFA">Three questions and we will tell you what to buy.</h2>\n'%H2)
    a('            <p style="margin:0;font-size:17px;line-height:1.55;color:#DCE5E1;max-width:44ch">The Gauge Finder asks what you are injecting, where, and how often. Nothing you answer is stored, and we never ask what it is for.</p>\n          </div>\n')
    a('          <div style="display:flex;gap:12px;flex-wrap:wrap">\n')
    a('            <a href="/gauge-finder" data-cta style="background:#8FBFA6;color:#143026;border-radius:1000px;padding:16px 30px;font-size:16px;font-weight:600">Open the Gauge Finder</a>\n')
    a('            <a href="/shop" data-cta style="border:1px solid rgba(143,191,166,.55);color:#FAFAFA;border-radius:1000px;padding:16px 30px;font-size:16px;font-weight:600">Browse the range</a>\n')
    a('          </div>\n        </div>\n      </div>\n    </section>\n\n  </main>')
    return ''.join(o)

SCRIPT_HEAD = '<script type="text/x-dc" data-dc-script data-props="{&quot;$preview&quot;:{&quot;width&quot;:1280,&quot;height&quot;:880}}">'

# the header values every page needs, lifted verbatim from the shared header
HEADER_VALS = """      shopOpen: this.state.menu === 'shop',
      shopCaret: this.state.menu === 'shop' ? 'rotate(180deg)' : 'none',
      toggleShop: () => this.setState(s => ({ menu: s.menu === 'shop' ? null : 'shop' })),
      learnOpen: this.state.menu === 'learn',
      learnCaret: this.state.menu === 'learn' ? 'rotate(180deg)' : 'none',
      toggleLearn: () => this.setState(s => ({ menu: s.menu === 'learn' ? null : 'learn' })),
      navOpen: this.state.menu === 'nav',
      toggleNav: () => this.setState(s => ({ menu: s.menu === 'nav' ? null : 'nav' })),
      cartCount: String(this.state.cart || 0),
"""

def grab(marker, src):
    """Pull a renderVals block (learnCols / menuCols) out of an existing page."""
    i = src.find('      %s: [' % marker)
    assert i != -1, marker
    j = src.find('\n      ],', i) + len('\n      ],')
    return src[i:j]

def build_script(p, learn_cols, menu_cols):
    items = [{'name':n, 'spec':sp, 'pack':pk, 'price':pr, 'size':sz, 'use':us, 'href':PROD[n]}
             for n, sp, pk, pr, sz, us in p['kit']]
    labels = [l for _, l in p['sel']]
    notes = {
      'glp-1-injections': 'Most weekly medicines need one injection and two swabs. Step it up and the swabs are what run out first.',
      'trt-injections': 'Two needles per injection, one to draw and one to inject. That is what drives the quantities here.',
      'peptide-reconstitution': 'One vial of bacteriostatic water covers a single reconstitution comfortably, with room for error.',
      'diabetes-at-home': 'Four or more injections a day gets through a box of 100 in under a month. Buy the bigger box.',
      'wound-care-at-home': 'Daily changes double the dressings and the saline. The gloves and tape last either way.',
      'clinic-fit-out': 'Per room, per month, at a normal clinic load. Gloves scale hardest because three sizes means three boxes.',
    }
    return """%s
class Component extends DCLogic {
  state = { menu: null, freq: 0 };

  componentDidMount() {
    const nodes = Array.from(document.querySelectorAll('[data-reveal]'));
    if (!nodes.length || !('IntersectionObserver' in window)) return;
    this._io = new IntersectionObserver((entries, obs) => {
      entries.filter(e => e.isIntersecting).forEach((e, i) => {
        e.target.style.setProperty('--reveal-delay', (i * 70) + 'ms');
        e.target.classList.add('is-in');
        obs.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -12%% 0px', threshold: 0.08 });
    nodes.forEach(n => this._io.observe(n));
  }

  componentWillUnmount() {
    if (this._io) this._io.disconnect();
  }

  renderVals() {
    const f = this.state.freq;
    const LABELS = %s;
    const ITEMS = %s;
    const money = c => '$' + (c / 100).toFixed(2);

    // How long a pack lasts, rather than pretending a box of 100 is a month's use.
    const lasts = months => {
      if (months >= 24) return 'two years or more at this rate';
      if (months >= 12) return 'about a year at this rate';
      if (months >= 2) return 'about ' + Math.round(months) + ' months at this rate';
      return 'about a month at this rate';
    };
    const packsFor = it => Math.max(1, Math.ceil(it.use[f] / it.size));

    const rows = ITEMS.map(it => {
      const n = packsFor(it);
      return {
        name: it.name,
        spec: it.spec,
        href: it.href,
        qty: n + ' × ' + it.pack,
        lasts: lasts(n * it.size / it.use[f]),
        price: money(n * it.price)
      };
    });
    const totalCents = ITEMS.reduce((t, it) => t + packsFor(it) * it.price, 0);

    return {
%s
      freqOptions: LABELS.map((label, i) => ({
        label,
        on: f === i,
        bg: f === i ? '#0E0E0E' : '#FAFAFA',
        fg: f === i ? '#FAFAFA' : '#0E0E0E',
        border: f === i ? '#0E0E0E' : '#E3E3E1',
        pick: () => this.setState({ freq: i })
      })),
      rows,
      total: money(totalCents),
      itemCount: ITEMS.length + ' items',
      note: %s,

%s
%s
    };
  }
}
</script>""" % (SCRIPT_HEAD, json.dumps(labels), json.dumps(items, indent=6).replace('\n', '\n    '),
                HEADER_VALS.rstrip(), json.dumps(notes[p['slug']]), learn_cols, menu_cols)

def main():
    src = SEO.strip_headmeta(io.open(DOCS + '/about.html', encoding='utf-8').read())
    learn_cols, menu_cols = grab('learnCols', src), grab('menuCols', src)
    os.makedirs(DOCS + '/for', exist_ok=True)
    for p in PAGES:
        head = HEAD.replace('<title>About | Good Practice Supply</title>',
                            '<title>%s | Good Practice Supply</title>' % E(p['title']))
        assert '<title>%s' % E(p['title']) in head, 'title not swapped for ' + p['slug']
        head = SEO.set_robots(head, '/for/' + p['slug'])
        path, meta = META.guide(p)
        head = head.replace('</head>', META.blocks(path, meta) + '\n</head>', 1)
        doc = (head + '\n\n  ' + build_main(p) + '\n\n  ' + FOOTER +
               '\n\n</div>\n\n</x-dc>\n' + build_script(p, learn_cols, menu_cols) + '\n</body>\n</html>\n')
        out = '%s/for/%s.html' % (DOCS, p['slug'])
        io.open(out, 'w', encoding='utf-8').write(doc)
        print('%-26s %6d bytes' % (p['slug'], len(doc)))

main()
