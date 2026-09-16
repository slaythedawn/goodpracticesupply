import io, json, os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import CATEGORIES, SHOTS, I, REGULATORY
import seo as SEO

import pathlib
DOCS=str(pathlib.Path(__file__).resolve().parent.parent / 'docs')
SRC=SEO.strip_headmeta(io.open(DOCS+'/about.html',encoding='utf-8').read())
SP='<div data-gp-spacer aria-hidden="true"></div>'
HEAD=SRC[:SRC.find(SP)+len(SP)]
FOOTER=SRC[SRC.find('<footer'):SRC.find('</footer>')+9]
E=html.escape

def grab(marker, src=SRC):
    i=src.find('      %s: ['%marker); j=src.find('\n      ],',i)+len('\n      ],')
    return src[i:j]
LEARNCOLS, MENUCOLS = grab('learnCols'), grab('menuCols')

MONO="font-family:'IBM Plex Mono',monospace;font-weight:500"
WRAP='max-width:1440px;margin:0 auto;padding:clamp(48px,7vw,96px) clamp(20px,5vw,72px)'
H1="font-family:'Archivo',sans-serif;font-weight:600;font-size:clamp(32px,3.8vw,52px);letter-spacing:-.035em;line-height:1.02;margin:0 0 16px"
H2="font-family:'Archivo',sans-serif;font-weight:600;font-size:clamp(26px,3vw,40px);letter-spacing:-.03em;line-height:1.05;margin:0 0 16px"
LEAD="margin:0;font-size:17.5px;line-height:1.55;color:#3A3A38;max-width:52ch"
CARD="background:#FAFAFA;border:1px solid #E3E3E1;border-radius:22px;padding:26px 24px"
money=lambda c:'$%.2f'%(c/100.0)

def crumbs(items):
    """items: list of (label, href or None)"""
    out=['        <div style="%s;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:#59595A;margin-bottom:clamp(20px,3vw,28px)">\n'%MONO]
    parts=[]
    for label,href in items:
        if href: parts.append('<a href="%s" style="color:#59595A">%s</a>'%(href,E(label)))
        else:    parts.append('<span style="color:#0E0E0E">%s</span>'%E(label))
    out.append('          '+' / '.join(parts)+'\n        </div>\n')
    return ''.join(out)

def page(title, main, script, head_extra='', path='/'):
    head=HEAD.replace('<title>About | Good Practice Supply</title>','<title>%s | Good Practice Supply</title>'%E(title))
    assert E(title) in head
    head=SEO.set_robots(head, path)
    if head_extra:
        assert '</head>' in head
        head=head.replace('</head>', head_extra.rstrip()+'\n</head>', 1)
    return head+'\n\n  '+main+'\n\n  '+FOOTER+'\n\n</div>\n\n</x-dc>\n'+script+'\n</body>\n</html>\n'

SCRIPT_OPEN='<script type="text/x-dc" data-dc-script data-props="{&quot;$preview&quot;:{&quot;width&quot;:1280,&quot;height&quot;:880}}">'
HEADER_VALS="""      shopOpen: this.state.menu === 'shop',
      shopCaret: this.state.menu === 'shop' ? 'rotate(180deg)' : 'none',
      toggleShop: () => this.setState(s => ({ menu: s.menu === 'shop' ? null : 'shop' })),
      learnOpen: this.state.menu === 'learn',
      learnCaret: this.state.menu === 'learn' ? 'rotate(180deg)' : 'none',
      toggleLearn: () => this.setState(s => ({ menu: s.menu === 'learn' ? null : 'learn' })),
      navOpen: this.state.menu === 'nav',
      toggleNav: () => this.setState(s => ({ menu: s.menu === 'nav' ? null : 'nav' })),"""
REVEAL="""  componentDidMount() {
    const nodes = Array.from(document.querySelectorAll('[data-reveal]'));
    if (!nodes.length || !('IntersectionObserver' in window)) return;
    this._io = new IntersectionObserver((entries, obs) => {
      entries.filter(e => e.isIntersecting).forEach((e, i) => {
        e.target.style.setProperty('--reveal-delay', (i * 70) + 'ms');
        e.target.classList.add('is-in');
        obs.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    nodes.forEach(n => this._io.observe(n));
  }

  componentWillUnmount() {
    if (this._io) this._io.disconnect();
  }
"""

# ------------------------------------------------------- long form sections
# A product page with a buy panel and a spec table has nothing on it for a
# search engine to understand, and nothing for a buyer who has not decided yet.
# These two sections are what the page is actually about.

def prose(sections, bg=''):
    """[(heading, [paragraph, ...])] as one readable column."""
    o=[]; a=o.append
    a('    <section style="%sborder-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%(bg,WRAP))
    for i,(head,paras) in enumerate(sections):
        a('        <div style="max-width:74ch%s">\n'%('' if i==0 else ';margin-top:clamp(36px,5vw,60px)'))
        a('          <h2 style="%s">%s</h2>\n'%(H2,E(head)))
        for t in paras:
            a('          <p style="margin:0 0 18px;font-size:17px;line-height:1.62;color:#3A3A38">%s</p>\n'%E(t))
        a('        </div>\n')
    a('      </div>\n    </section>\n\n')
    return ''.join(o)

def faq_block(title, pairs, bg='background:#F2F2F1;'):
    o=[]; a=o.append
    a('    <section style="%sborder-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%(bg,WRAP))
    a('        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr));gap:clamp(28px,4vw,64px);align-items:start">\n')
    a('          <div>\n            <h2 style="%s">%s</h2>\n'%(H2,E(title)))
    a('            <p style="%s">If yours is not here, the contact form routes to the person who can answer it.</p>\n          </div>\n'%LEAD.replace('0 0 16px','0'))
    a('          <div style="border-top:1px solid #E3E3E1">\n')
    for q,ans in pairs:
        a('            <div style="padding:22px 0;border-bottom:1px solid #E3E3E1">\n')
        a('              <h3 style="font-family:\'Archivo\',sans-serif;font-weight:600;font-size:17px;letter-spacing:-.02em;margin:0 0 8px">%s</h3>\n'%E(q))
        a('              <div style="font-size:15.5px;line-height:1.6;color:#3A3A38">%s</div>\n            </div>\n'%E(ans))
    a('          </div>\n        </div>\n      </div>\n    </section>\n\n')
    return ''.join(o)

# Where a category sits in the rest of the site. Product pages that only link to
# other product pages are a dead end for a crawler and for a reader.
USE_WITH = {
 'syringes-needles': [('/gauge-finder','Gauge Finder','Three questions and it picks the thickness and the length.'),
                      ('/learn/needle-gauge-chart','Needle gauge chart','Every gauge, its diameter in millimetres and its hub colour.'),
                      ('/for/glp-1-injections','For GLP-1 injections','The whole kit for a weekly injection at home.')],
 'diluents-swabs':  [('/tools/reconstitution-calculator','Reconstitution calculator','Turns a dose in milligrams into a mark on the barrel.'),
                      ('/for/peptide-reconstitution','For reconstitution','What to have on the bench, and the part that goes wrong.'),
                      ('/learn/needle-gauge-chart','Needle gauge chart','Which gauge draws and which one injects.')],
 'gloves-ppe':      [('/for/clinic-fit-out','For a clinic fit-out','The consumables list, room by room, priced.'),
                      ('/always-stocked','Always Stocked','Set the list once and the room looks after itself.'),
                      ('/clinic-portal','Clinic Portal','Trade pricing and standing orders per site.')],
 'wound-care':      [('/for/wound-care-at-home','For wound care at home','What a treatment room does differently.'),
                      ('/for/clinic-fit-out','For a clinic fit-out','The consumables list, room by room, priced.'),
                      ('/always-stocked','Always Stocked','It ships before a line runs low.')],
 'diagnostics':     [('/for/diabetes-at-home','For diabetes at home','Lancets, strips and what the NDSS covers.'),
                      ('/for/clinic-fit-out','For a clinic fit-out','The consumables list, room by room, priced.'),
                      ('/clinic-portal','Clinic Portal','Trade pricing and standing orders per site.')],
 'clinic-disposal': [('/for/clinic-fit-out','For a clinic fit-out','The consumables list, room by room, priced.'),
                      ('/always-stocked','Always Stocked','The category that should never be on someone\u2019s memory.'),
                      ('/learn','Guides','Sharps disposal, state by state.')],
 'hygiene-cleaning':[('/always-stocked','Always Stocked','Set the list once and the basin looks after itself.'),
                      ('/for/clinic-fit-out','For a clinic fit-out','The consumables list, room by room, priced.'),
                      ('/clinic-portal','Clinic Portal','Carton rates and standing orders per site.')],
 'taping-supports': [('/for/clinic-fit-out','For a clinic fit-out','The consumables list, room by room, priced.'),
                      ('/clinic-portal','Clinic Portal','Trade pricing and standing orders per site.'),
                      ('/always-stocked','Always Stocked','It ships before a line runs low.')],
}

def use_with(cat_slug, heading='Use it with'):
    links=USE_WITH.get(cat_slug) or []
    if not links: return ''
    o=[]; a=o.append
    a('    <section style="border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <h2 style="font-family:\'Archivo\',sans-serif;font-weight:600;font-size:clamp(22px,2.4vw,30px);letter-spacing:-.025em;margin:0 0 22px">%s</h2>\n'%E(heading))
    a('        <div data-reveal style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));gap:14px">\n')
    for href,name,blurb in links:
        a('          <a href="%s" data-card style="%s;display:block" style-hover="border-color:#0E0E0E">\n'%(href,CARD))
        a('            <span style="display:block;font-family:\'Archivo\',sans-serif;font-weight:600;font-size:17px;letter-spacing:-.02em;margin-bottom:8px">%s</span>\n'%E(name))
        a('            <span style="display:block;font-size:15px;line-height:1.5;color:#3A3A38">%s</span>\n          </a>\n'%E(blurb))
    a('        </div>\n      </div>\n    </section>\n\n')
    return ''.join(o)

def product_card(cat, p):
    url='/shop/%s/%s'%(cat['slug'],p['slug'])
    key,alt=SHOTS[p['family']][0]
    return ('          <a href="%s" data-card data-tag="%s" style="border:1px solid #E3E3E1;border-radius:22px;overflow:hidden;display:block;background:#FAFAFA" style-hover="border-color:#0E0E0E">\n'
            '            <span style="display:block;background:#EDEDEB;aspect-ratio:4/3;overflow:hidden">\n'
            '              <img src="%s" alt="%s" style="width:100%%;height:100%%;object-fit:cover">\n            </span>\n'
            '            <span style="padding:18px 20px 20px;display:flex;flex-direction:column;gap:7px">\n'
            '              <span style="%s;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:#59595A">%s</span>\n'
            '              <span style="font-family:\'Archivo\',sans-serif;font-weight:600;font-size:17px;letter-spacing:-.02em">%s</span>\n'
            '              <span style="display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-top:4px">\n'
            '                <span style="font-size:16.5px;font-weight:600">%s</span>\n'
            '                <span style="%s;font-size:12px;color:#59595A">%s</span>\n'
            '              </span>\n            </span>\n          </a>\n'
            %(url,p['tag'],I[key],E(alt),MONO,E(p['spec']),E(p['name']),money(p['packs'][0][1]),MONO,E(p['packs'][0][0])))

# ---------------------------------------------------------------- category page
def build_category(cat):
    m=['<main>\n']
    a=m.append
    a('    <section style="border-bottom:1px solid #E3E3E1">\n')
    a('      <div data-gp-pagehead style="max-width:1440px;margin:0 auto;padding:clamp(32px,5vw,64px) clamp(20px,5vw,72px) clamp(40px,5vw,56px)">\n')
    a(crumbs([('Home','/'),('Shop','/shop'),(cat['name'],None)]))
    a('        <div data-gp-pagehead-grid style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:clamp(28px,4vw,64px);align-items:center">\n')
    a('          <div>\n            <span style="display:inline-block;%s;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;border:1px solid rgba(28,64,52,.3);border-radius:1000px;padding:7px 13px;margin-bottom:20px">%d products</span>\n'%(MONO,cat['count']))
    a('            <h1 style="%s">%s</h1>\n'%(H1,E(cat['name'])))
    a('            <p style="%s">%s</p>\n          </div>\n'%(LEAD,E(cat['intro'])))
    a('          <div style="border-radius:28px;overflow:hidden;background:#EDEDEB;aspect-ratio:4/3">\n')
    a('            <img src="%s" alt="%s" style="width:100%%;height:100%%;object-fit:cover">\n          </div>\n        </div>\n      </div>\n    </section>\n\n'%(cat['img'],E(cat['alt'])))
    # grid
    a('    <section id="grid" style="border-bottom:1px solid #E3E3E1">\n      <div style="max-width:1440px;margin:0 auto;padding:clamp(28px,4vw,44px) clamp(20px,5vw,72px) clamp(48px,7vw,96px)">\n')
    a('        <div style="display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;margin-bottom:24px">\n')
    a('          <div style="display:flex;gap:8px;flex-wrap:wrap">\n')
    a('            <sc-for list="{{ filters }}" as="fl" hint-placeholder-count="%d">\n'%len(cat['filters']))
    a('              <button type="button" onClick="{{ fl.pick }}" aria-pressed="{{ fl.on }}" data-chip style="cursor:pointer;font-family:\'Archivo\',sans-serif;font-size:15px;font-weight:500;border:1px solid {{ fl.border }};background:{{ fl.bg }};color:{{ fl.fg }};border-radius:1000px;padding:10px 18px">{{ fl.label }}</button>\n')
    a('            </sc-for>\n          </div>\n')
    a('          <div style="%s;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#59595A">{{ resultLabel }}</div>\n        </div>\n'%MONO)
    a('        <div data-reveal style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));gap:14px">\n')
    for p in cat['products']:
        a(product_card(cat,p))
    a('        </div>\n      </div>\n    </section>\n\n')
    # gauge finder band
    a('    <section style="background:#1C4034;color:#FAFAFA">\n      <div style="%s;display:flex;justify-content:space-between;gap:32px;flex-wrap:wrap;align-items:center">\n'%WRAP)
    a('        <div>\n          <h2 style="%s;color:#FAFAFA">Not sure which one you need?</h2>\n'%H2)
    a('          <p style="margin:0;font-size:16.5px;line-height:1.5;color:#B7CFC3;max-width:46ch">Three plain questions and the Gauge Finder tells you the thickness, the length and how many. Nothing you answer is stored.</p>\n        </div>\n')
    a('        <a href="/gauge-finder" data-cta style="background:#8FBFA6;color:#143026;border-radius:1000px;padding:16px 30px;font-size:16px;font-weight:600;white-space:nowrap">Open the Gauge Finder</a>\n')
    a('      </div>\n    </section>\n\n')
    cs=SEO.CATEGORY_SEO[cat['slug']]
    a(prose(cs['guide'], bg='background:#F2F2F1;'))
    a(use_with(cat['slug'], 'Work out what you need'))
    a(faq_block('Questions about %s'%SEO.lower_name(cat['name']), cs['faq'], bg=''))
    a('  </main>')
    tags=[t for t,_ in cat['filters']]
    prods=[{'tag':p['tag']} for p in cat['products']]
    script="""%s
class Component extends DCLogic {
  state = { menu: null, filter: 'all' };

%s
  renderVals() {
    const f = this.state.filter;
    const FILTERS = %s;
    const TAGS = %s;
    const shown = TAGS.filter(t => f === 'all' || t === f).length;

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
      resultLabel: shown + (shown === 1 ? ' product' : ' products'),

%s
%s
    };
  }

  componentDidUpdate() { this.syncFilter(); }

  syncFilter() {
    // The grid is rendered server side for crawlers, so filtering toggles
    // visibility on the cards rather than rebuilding the list.
    const f = this.state.filter;
    document.querySelectorAll('#grid [data-tag]').forEach(el => {
      el.style.display = (f === 'all' || el.getAttribute('data-tag') === f) ? '' : 'none';
    });
  }
}
</script>"""%(SCRIPT_OPEN, REVEAL,
              json.dumps([{'tag':t,'label':l} for t,l in cat['filters']]),
              json.dumps([p['tag'] for p in cat['products']]),
              HEADER_VALS, LEARNCOLS, MENUCOLS)
    path='/shop/'+cat['slug']
    head_extra='\n'.join([
        SEO.head_tags(path=path, title=cs['title'], description=cs['desc'], image=cat['img']),
        SEO.jsonld({'@context':'https://schema.org','@type':'CollectionPage',
                    'name':cs['title'],'description':cs['desc'],'url':SEO.ORIGIN+path,
                    'isPartOf':{'@type':'WebSite','name':SEO.BRAND,'url':SEO.ORIGIN}}),
        SEO.jsonld(SEO.breadcrumbs([('Home','/'),('Shop','/shop'),(cat['name'],path)])),
        SEO.jsonld(SEO.item_list(cat['products'], cat['slug'])),
        SEO.jsonld(SEO.faq_schema(cs['faq'])),
    ])
    return ''.join(m), script, head_extra

# ---------------------------------------------------------------- product page
def build_product(cat, p, idx):
    shots=SHOTS[p['family']]
    related=[q for q in cat['products'] if q is not p][:3]
    m=['<main>\n']; a=m.append
    a('    <section style="border-bottom:1px solid #E3E3E1">\n')
    a('      <div data-gp-pagehead style="max-width:1440px;margin:0 auto;padding:clamp(32px,5vw,64px) clamp(20px,5vw,72px) clamp(48px,7vw,96px)">\n')
    a(crumbs([('Home','/'),('Shop','/shop'),(cat['name'],'/shop/'+cat['slug']),(p['name'],None)]))
    a('        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(380px,100%),1fr));gap:clamp(28px,4vw,64px);align-items:start">\n')
    # gallery
    a('          <div>\n            <div style="position:relative;border-radius:28px;overflow:hidden;background:#EDEDEB;aspect-ratio:4/3">\n')
    for i,(key,alt) in enumerate(shots):
        a('              <img src="%s" alt="%s" style="position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;opacity:{{ op%d }};transition:opacity var(--dur-base,260ms) ease">\n'%(I[key],E(alt),i))
    a('            </div>\n')
    # A product with one photograph gets no thumbnail strip. A single thumbnail
    # under a single image is a control that does nothing.
    if len(shots) > 1:
        a('            <div style="display:grid;grid-template-columns:repeat(%d,1fr);gap:10px;margin-top:10px">\n'%len(shots))
        for i,(key,alt) in enumerate(shots):
            a('              <button type="button" onClick="{{ pick%d }}" aria-label="%s" style="padding:0;cursor:pointer;background:#EDEDEB;border:1px solid {{ th%d }};border-radius:14px;overflow:hidden;aspect-ratio:1/1">\n'%(i,E(alt),i))
            a('                <img src="%s" alt="" style="width:100%%;height:100%%;object-fit:cover">\n              </button>\n'%I[key])
        a('            </div>\n')
    a('          </div>\n')
    # buy panel
    a('          <div id="buy">\n')
    a('            <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:18px">\n')
    pill='In stock' if SEO.PURCHASABLE else 'Coming soon'
    a('              <span style="display:inline-block;%s;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:#143026;background:#8FBFA6;border-radius:1000px;padding:7px 12px">%s</span>\n'%(MONO,pill))
    a('              <span style="%s;font-size:11.5px;color:#59595A">{{ batchLine }}</span>\n            </div>\n'%MONO)
    a('            <h1 style="font-family:\'Archivo\',sans-serif;font-weight:600;font-size:clamp(30px,3.4vw,46px);letter-spacing:-.035em;line-height:1.04;margin:0 0 14px">%s</h1>\n'%E(p['name']))
    a('            <p style="margin:0 0 26px;font-size:17px;line-height:1.55;color:#3A3A38;max-width:46ch">%s</p>\n'%E(p['blurb']))
    # variants
    a('            <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;margin-bottom:12px">Option</div>\n'%MONO)
    a('            <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:24px">\n')
    a('              <sc-for list="{{ variants }}" as="v" hint-placeholder-count="%d">\n'%len(p['variants']))
    a('                <button type="button" onClick="{{ v.pick }}" aria-pressed="{{ v.on }}" style="cursor:pointer;text-align:left;font-family:\'Archivo\',sans-serif;font-size:15px;font-weight:500;border:1px solid {{ v.border }};background:{{ v.bg }};color:{{ v.fg }};border-radius:14px;padding:12px 16px">\n')
    a('                  <span style="display:block">{{ v.label }}</span>\n')
    a('                  <span style="display:block;%s;font-size:11px;opacity:.7;margin-top:4px">{{ v.hint }}</span>\n'%MONO)
    a('                </button>\n              </sc-for>\n            </div>\n')
    # packs
    a('            <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;margin-bottom:12px">Pack size</div>\n'%MONO)
    a('            <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:24px">\n')
    a('              <sc-for list="{{ packs }}" as="k" hint-placeholder-count="%d">\n'%len(p['packs']))
    a('                <button type="button" onClick="{{ k.pick }}" aria-pressed="{{ k.on }}" style="cursor:pointer;text-align:left;width:100%%;display:flex;justify-content:space-between;align-items:center;gap:16px;font-family:\'Archivo\',sans-serif;font-size:15.5px;font-weight:500;border:1px solid {{ k.border }};background:{{ k.bg }};color:{{ k.fg }};border-radius:14px;padding:14px 18px">\n')
    a('                  <span>{{ k.label }}</span>\n                  <span style="%s;font-size:14px">{{ k.price }}</span>\n'%MONO)
    a('                </button>\n              </sc-for>\n            </div>\n')
    # qty + cart
    a('            <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:20px">\n')
    a('              <div style="display:flex;align-items:center;gap:6px;border:1px solid #E3E3E1;border-radius:1000px;padding:6px 10px;background:#FAFAFA">\n')
    a('                <button type="button" onClick="{{ dec }}" aria-label="Decrease quantity" style="border:0;background:none;cursor:pointer;font-size:19px;width:34px;height:34px;color:#0E0E0E">&minus;</button>\n')
    a('                <span style="%s;font-size:15px;min-width:26px;text-align:center">{{ qty }}</span>\n'%MONO)
    a('                <button type="button" onClick="{{ inc }}" aria-label="Increase quantity" style="border:0;background:none;cursor:pointer;font-size:19px;width:34px;height:34px;color:#0E0E0E">+</button>\n')
    a('              </div>\n              <span style="%s;font-size:22px">{{ totalLabel }}</span>\n            </div>\n'%MONO)
    # A button that cannot do anything should not look like it can.
    if SEO.PURCHASABLE:
        a('            <button type="button" onClick="{{ addToCart }}" data-cta style="width:100%%;cursor:pointer;border:0;background:#0E0E0E;color:#FAFAFA;border-radius:1000px;padding:17px 30px;font-family:\'Archivo\',sans-serif;font-size:16px;font-weight:600">{{ ctaLabel }}</button>\n')
    else:
        a('            <button type="button" disabled style="width:100%%;cursor:not-allowed;border:1px solid #C4C4C2;background:#EDEDEB;color:#59595A;border-radius:1000px;padding:17px 30px;font-family:\'Archivo\',sans-serif;font-size:16px;font-weight:600">{{ ctaLabel }}</button>\n')
    ship=('Free delivery over $99. Dispatched from Sydney. Plain unmarked box.'
          if SEO.PURCHASABLE else
          'Ordering opens shortly. Delivery will be free over $99, dispatched from Sydney in a plain unmarked box.')
    a('            <div style="%s;font-size:11.5px;color:#59595A;margin-top:14px;line-height:1.7">%s</div>\n'%(MONO,ship))
    a('          </div>\n        </div>\n      </div>\n    </section>\n\n')
    ps=SEO.compose(cat,p)
    a(prose(ps['body']))
    # specs
    a('    <section style="background:#F2F2F1;border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr));gap:clamp(28px,4vw,64px);align-items:start">\n')
    a('          <div>\n            <h2 style="%s">Everything on the box, before you buy.</h2>\n'%H2)
    a('            <p style="%s">The incumbents make you register to see a price. The batch and the expiry you are shipped are the ones printed here.</p>\n          </div>\n'%LEAD)
    a('          <div style="border-top:1px solid #E3E3E1">\n')
    a('            <sc-for list="{{ specRows }}" as="r" hint-placeholder-count="9">\n')
    a('              <div style="display:flex;justify-content:space-between;gap:20px;padding:16px 0;border-bottom:1px solid #E3E3E1;align-items:baseline">\n')
    a('                <span style="font-size:16px;color:#3A3A38">{{ r.k }}</span>\n')
    a('                <span style="%s;font-size:14.5px;color:#0E0E0E;text-align:right">{{ r.v }}</span>\n'%MONO)
    a('              </div>\n            </sc-for>\n          </div>\n        </div>\n      </div>\n    </section>\n\n')
    a(faq_block('Questions about %s'%SEO.lower_name(p['name']), ps['faq'], bg=''))
    a(use_with(cat['slug']))
    # related
    a('    <section style="background:#F2F2F1;border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:22px">\n')
    a('          <h2 style="font-family:\'Archivo\',sans-serif;font-weight:600;font-size:clamp(22px,2.4vw,30px);letter-spacing:-.025em;margin:0">Often bought together</h2>\n')
    a('          <a href="/shop/%s" data-link style="font-size:15px;font-weight:600;border-bottom:1.5px solid #C4C4C2;padding-bottom:3px;white-space:nowrap">All %s <span data-arrow>&rarr;</span></a>\n        </div>\n'%(cat['slug'],E(cat['name'].lower())))
    a('        <div data-reveal style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));gap:14px">\n')
    for q in related:
        a(product_card(cat,q))
    a('        </div>\n      </div>\n    </section>\n\n  </main>')

    # ARTG and country of origin come from REGULATORY, which is empty until a
    # supplier gives us a real value per product. A generic "ARTG: Listed" on a
    # box of tissues is a claim we cannot stand behind, so nothing is printed
    # rather than something convenient.
    specs=[('Brand','Good Practice Supply')]+[(k,v) for k,v in p['extra']]+[
           ('Pack','{{ packLabel }}'),('Product code','{{ code }}'),('Batch','{{ batch }}'),
           ('Expiry','04/2028')]+[(k,v) for k,v in REGULATORY.get(p['slug'],[])]
    code='GPS-%s-%03d'%(cat['slug'][:3].upper(), idx+1)
    script="""%s
class Component extends DCLogic {
  state = { menu: null, img: 0, variant: 0, pack: 0, qty: 1, cart: 0, added: false };

%s
  renderVals() {
    const s = this.state;
    const VARIANTS = %s;
    const PACKS = %s;
    const money = c => '$' + (c / 100).toFixed(2);
    const sel = on => ({
      bg: on ? '#0E0E0E' : '#FAFAFA',
      fg: on ? '#FAFAFA' : '#0E0E0E',
      border: on ? '#0E0E0E' : '#E3E3E1'
    });
    const pack = PACKS[s.pack];
    const total = pack.price * s.qty;
    const code = %s + '-' + String(s.variant + 1).padStart(2, '0');

    const vals = {
%s
      cartCount: String(s.cart),

      variants: VARIANTS.map((v, i) => {
        const c = sel(s.variant === i);
        return { label: v.label, hint: v.hint || '\\u00a0', on: s.variant === i,
                 bg: c.bg, fg: c.fg, border: c.border,
                 pick: () => this.setState({ variant: i, added: false }) };
      }),
      packs: PACKS.map((k, i) => {
        const c = sel(s.pack === i);
        return { label: k.label, price: money(k.price), on: s.pack === i,
                 bg: c.bg, fg: c.fg, border: c.border,
                 pick: () => this.setState({ pack: i, added: false }) };
      }),
      qty: String(s.qty),
      inc: () => this.setState(p => ({ qty: Math.min(20, p.qty + 1), added: false })),
      dec: () => this.setState(p => ({ qty: Math.max(1, p.qty - 1), added: false })),
      totalLabel: money(total),
      ctaLabel: %s,
      addToCart: () => %s,

      batchLine: code + ' · Batch 26F-114 · Exp 04/28',
      code,
      batch: '26F-114',
      packLabel: pack.label,
      artg: 'Listed, see carton',
      specRows: %s,

%s
%s
    };
    // stacked images, one visible
    for (let i = 0; i < %d; i++) {
      vals['op' + i] = s.img === i ? '1' : '0';
      vals['th' + i] = s.img === i ? '#0E0E0E' : '#E3E3E1';
      vals['pick' + i] = () => this.setState({ img: i });
    }
    return vals;
  }
}
</script>"""%(SCRIPT_OPEN, REVEAL,
              json.dumps([{'label':l,'hint':h} for l,h in p['variants']]),
              json.dumps([{'label':l,'price':pr} for l,pr in p['packs']]),
              json.dumps(code),
              HEADER_VALS,
              # ctaLabel and addToCart sit above specRows in the template, so
              # they go here. Getting this order wrong puts the spec table in
              # the button, which is exactly as visible as it sounds.
              ("s.added ? 'Added to cart' : 'Add to cart'" if SEO.PURCHASABLE
               else "'Coming soon'"),
              ("this.setState(p => ({ added: true, cart: p.cart + p.qty }))"
               if SEO.PURCHASABLE else "undefined"),
              json.dumps([{'k':k,'v':v} for k,v in specs]).replace('"{{ packLabel }}"','pack.label').replace('"{{ code }}"','code').replace('"{{ batch }}"',"'26F-114'").replace('"{{ artg }}"',"'Listed, see carton'"),
              LEARNCOLS, MENUCOLS,
              len(shots))
    path='/shop/%s/%s'%(cat['slug'],p['slug'])
    # The offer carries the cheapest pack, because that is the price a result
    # should show. Prices are still placeholders: nothing is sourced yet, which
    # is the other reason SEO.INDEXABLE is off.
    head_extra='\n'.join([
        SEO.head_tags(path=path, title=ps['title'], description=ps['desc'],
                      image=I[SHOTS[p['family']][0][0]], kind='product'),
        SEO.jsonld(SEO.product_schema(path=path, name=p['name'],
                    description=ps['desc'], image=I[SHOTS[p['family']][0][0]],
                    sku=code, price_cents=min(pr for _,pr in p['packs']),
                    category=cat['name'])),
        SEO.jsonld(SEO.breadcrumbs([('Home','/'),('Shop','/shop'),
                    (cat['name'],'/shop/'+cat['slug']),(p['name'],path)])),
        SEO.jsonld(SEO.faq_schema(ps['faq'])),
    ])
    return ''.join(m), script, head_extra

# ---------------------------------------------------------------- shop index
def build_shop():
    total=sum(c['count'] for c in CATEGORIES)
    m=['<main>\n']; a=m.append
    a('    <section style="border-bottom:1px solid #E3E3E1">\n')
    a('      <div data-gp-pagehead style="max-width:1440px;margin:0 auto;padding:clamp(32px,5vw,64px) clamp(20px,5vw,72px) clamp(40px,5vw,56px)">\n')
    a(crumbs([('Home','/'),('Shop',None)]))
    a('        <div data-gp-pagehead-grid style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:clamp(28px,4vw,64px);align-items:center">\n')
    a('          <div>\n            <span style="display:inline-block;%s;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;border:1px solid rgba(28,64,52,.3);border-radius:1000px;padding:7px 13px;margin-bottom:20px">%d products</span>\n'%(MONO,total))
    a('            <h1 style="%s">Every product, priced, without an account.</h1>\n'%H1)
    a('            <p style="%s">Eight categories covering what a treatment room and a bathroom cupboard both need. Every price on this site is visible to anyone, including search engines, which is not true of a single one of our competitors.</p>\n          </div>\n'%LEAD)
    a('          <div style="border-radius:28px;overflow:hidden;background:#EDEDEB;aspect-ratio:4/3">\n')
    a('            <img src="%s" alt="A box of insulin syringes with three laid in front" style="width:100%%;height:100%%;object-fit:cover">\n          </div>\n        </div>\n      </div>\n    </section>\n\n'%I['syringe_box'])
    # category grid
    a('    <section style="border-bottom:1px solid #E3E3E1">\n      <div style="max-width:1440px;margin:0 auto;padding:clamp(28px,4vw,44px) clamp(20px,5vw,72px) clamp(48px,7vw,96px)">\n')
    a('        <div data-reveal style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr));gap:14px">\n')
    for c in CATEGORIES:
        a('          <a href="/shop/%s" data-card style="border-radius:22px;overflow:hidden;display:block;background:#FAFAFA;border:1px solid #E3E3E1" style-hover="border-color:#0E0E0E">\n'%c['slug'])
        a('            <span style="display:block;background:#EDEDEB;aspect-ratio:4/3;overflow:hidden">\n')
        a('              <img src="%s" alt="%s" style="width:100%%;height:100%%;object-fit:cover">\n            </span>\n'%(c['img'],E(c['alt'])))
        a('            <span style="display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding:16px 18px;min-height:62px">\n')
        a('              <span style="font-family:\'Archivo\',sans-serif;font-weight:600;font-size:16.5px;letter-spacing:-.02em">%s</span>\n'%E(c['name']))
        a('              <span style="%s;font-size:12px;color:#59595A">%d</span>\n            </span>\n          </a>\n'%(MONO,c['count']))
    a('        </div>\n      </div>\n    </section>\n\n')
    # by protocol
    a('    <section style="background:#F2F2F1;border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'%WRAP)
    a('        <div style="max-width:48ch;margin-bottom:clamp(28px,4vw,40px)">\n')
    a('          <span style="display:inline-block;%s;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#1C4034;border:1px solid rgba(28,64,52,.3);border-radius:1000px;padding:7px 13px;margin-bottom:20px">By protocol</span>\n'%MONO)
    a('          <h2 style="%s">Or start from what you are doing.</h2>\n'%H2)
    a('          <p style="%s">If you know the protocol but not the part numbers, these pages list what you need and why, with the whole kit priced.</p>\n        </div>\n'%LEAD)
    a('        <div data-reveal style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));gap:14px">\n')
    for slug,name,blurb in [
        ('glp-1-injections','GLP-1 and weight loss','What you need to inject a weekly medicine at home.'),
        ('trt-injections','TRT and hormone therapy','Two needles per injection, and why.'),
        ('peptide-reconstitution','Peptide reconstitution','Bacteriostatic water and the part that goes wrong.'),
        ('diabetes-at-home','Diabetes at home','Syringes, lancets and what the NDSS covers.'),
        ('wound-care-at-home','Wound care at home','What a treatment room does differently.'),
        ('clinic-fit-out','Clinic fit-out','The consumables list, per room, priced.')]:
        a('          <a href="/for/%s" data-card style="%s;display:block" style-hover="border-color:#0E0E0E">\n'%(slug,CARD))
        a('            <span style="display:block;font-family:\'Archivo\',sans-serif;font-weight:600;font-size:17px;letter-spacing:-.02em;margin-bottom:8px">%s</span>\n'%E(name))
        a('            <span style="display:block;font-size:15px;line-height:1.5;color:#3A3A38">%s</span>\n          </a>\n'%E(blurb))
    a('        </div>\n      </div>\n    </section>\n\n')
    a(prose([
      ('How the shop is organised', [
       'Eight categories, and a product only ever sits in one of them, so there is no hunting through three places for the same box. If you know what you want, the category is the fastest route. If you know the job but not the part number, the protocol pages below list a whole kit with every line priced.',
       'Every price on this page and every page under it is visible without an account, including to search engines. That is not true of a single one of the incumbents, and it is the main thing we are trying to change about buying consumables in Australia.',
      ]),
      ('Pack sizes and what they are for', [
       'Most lines come in three sizes: a box for a household, a larger box for someone injecting regularly, and a carton for a treatment room. The carton is always cheaper per unit and the difference is on the page, so you can see whether it is worth the shelf space.',
       'There is no minimum order. One box of gloves is a normal thing to buy here, and it costs what the page says it costs.',
      ]),
    ], bg='background:#F2F2F1;'))
    SHOP_FAQ=[
      ('Do I need an account to buy?',
       'No. Every price is on the page and you can order without one. A Clinic Portal account adds trade pricing and standing orders on top, but it is not a gate.'),
      ('Is there a minimum order?',
       'No. One box is fine.'),
      ('Do I need a prescription for any of this?',
       'No. Everything here is a consumable. We do not stock peptides, hormones or any prescription medicine, and anything that needs a script comes from your pharmacy.'),
      ('Where do orders ship from?',
       'Sydney, Australia wide, in a plain unmarked box. Delivery is free over $99.'),
    ]
    a(faq_block('Questions about ordering', SHOP_FAQ, bg=''))
    a('  </main>')
    script="""%s
class Component extends DCLogic {
  state = { menu: null };

%s
  renderVals() {
    return {
%s
      cartCount: String(this.state.cart || 0),

%s
%s
    };
  }
}
</script>"""%(SCRIPT_OPEN, REVEAL, HEADER_VALS, LEARNCOLS, MENUCOLS)
    desc=('Every product priced on the page, no account needed. %d medical consumables across %d categories, '
          'from insulin syringes to sharps containers. Dispatched from Sydney.'%(total,len(CATEGORIES)))
    head_extra='\n'.join([
        SEO.head_tags(path='/shop', title='Shop all products', description=desc, image=I['syringe_box']),
        SEO.jsonld({'@context':'https://schema.org','@type':'CollectionPage',
                    'name':'Shop all products','description':desc,'url':SEO.ORIGIN+'/shop',
                    'isPartOf':{'@type':'WebSite','name':SEO.BRAND,'url':SEO.ORIGIN}}),
        SEO.jsonld(SEO.breadcrumbs([('Home','/'),('Shop','/shop')])),
        SEO.jsonld({'@context':'https://schema.org','@type':'ItemList',
                    'itemListElement':[{'@type':'ListItem','position':i+1,'name':c['name'],
                                        'url':'%s/shop/%s'%(SEO.ORIGIN,c['slug'])}
                                       for i,c in enumerate(CATEGORIES)]}),
        SEO.jsonld(SEO.faq_schema(SHOP_FAQ)),
    ])
    return ''.join(m), script, head_extra

def main():
    os.makedirs(DOCS+'/shop',exist_ok=True)
    n=0
    mn,sc,hx=build_shop()
    io.open(DOCS+'/shop.html','w',encoding='utf-8').write(page('Shop all products',mn,sc,hx,'/shop')); n+=1
    for cat in CATEGORIES:
        os.makedirs('%s/shop/%s'%(DOCS,cat['slug']),exist_ok=True)
        mn,sc,hx=build_category(cat)
        cs=SEO.CATEGORY_SEO[cat['slug']]
        io.open('%s/shop/%s.html'%(DOCS,cat['slug']),'w',encoding='utf-8').write(page(cs['title'],mn,sc,hx,'/shop/'+cat['slug'])); n+=1
        for i,p in enumerate(cat['products']):
            mn,sc,hx=build_product(cat,p,i)
            io.open('%s/shop/%s/%s.html'%(DOCS,cat['slug'],p['slug']),'w',encoding='utf-8').write(
                page(SEO.compose(cat,p)['title'],mn,sc,hx,
                     '/shop/%s/%s'%(cat['slug'],p['slug']))); n+=1
    print('wrote',n,'pages')

main()
