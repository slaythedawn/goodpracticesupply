import glob, io, re, os
os.chdir('/home/user/goodpracticesupply/docs')
MONO="font-family:'IBM Plex Mono',monospace;font-weight:500"

COLS = [
 ('Shop', [('Syringes & needles','/shop/syringes-needles'),('Gloves & PPE','/shop/gloves-ppe'),
           ('Diluents & swabs','/shop/diluents-swabs'),('Wound care','/shop/wound-care'),
           ('Diagnostics','/shop/diagnostics'),('Clinic & disposal','/shop/clinic-disposal'),
           ('Hygiene & cleaning','/shop/hygiene-cleaning'),('Taping & supports','/shop/taping-supports'),
           ('All products','/shop')]),
 ('Shop by protocol', [('GLP-1 and weight loss','/for/glp-1-injections'),('TRT and hormone therapy','/for/trt-injections'),
           ('Peptide reconstitution','/for/peptide-reconstitution'),('Diabetes at home','/for/diabetes-at-home'),
           ('Wound care at home','/for/wound-care-at-home'),('Clinic fit-out','/for/clinic-fit-out')]),
 ('Guides & tools', [('Peptide reconstitution calculator','/tools/reconstitution-calculator'),
           ('Needle gauge chart','/learn/needle-gauge-chart'),('Gauge Finder','/gauge-finder'),
           ('Always Stocked','/always-stocked'),('All guides','/learn')]),
 ('Company', [('About','/about'),('Clinic Portal','/clinic-portal'),('Contact','/contact'),('Delivery & returns','/contact')]),
]

def build():
    o=['  <footer style="background:#143026;color:#B7CFC3">\n']
    a=o.append
    a('    <div style="max-width:1440px;margin:0 auto;padding:clamp(40px,6vw,80px) clamp(20px,5vw,72px)">\n')
    a('      <div data-gp-footer-grid style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(170px,100%),1fr));gap:36px;padding-bottom:36px;border-bottom:1px solid #2A5245">\n')
    a('        <div>\n          <a href="/" style="display:flex;flex-direction:column;gap:6px;margin-bottom:16px">\n')
    a('            <span style="font-family:\'Archivo Black\',\'Archivo\',sans-serif;font-size:25px;letter-spacing:-.055em;line-height:.9;color:#FAFAFA">goodpractice</span>\n')
    a('            <span style="font-family:\'Archivo\',sans-serif;font-weight:600;font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:#B7CFC3;line-height:1">Supply</span>\n')
    a('          </a>\n          <div style="font-size:15px;color:#B7CFC3">Medical supplies for clinics and home.</div>\n        </div>\n')
    for title,links in COLS:
        a('        <div style="display:flex;flex-direction:column;gap:11px">\n')
        a('          <div style="font-size:13.5px;font-weight:600;color:#FAFAFA;margin-bottom:3px">%s</div>\n'%title.replace('&','&amp;'))
        for label,href in links:
            a('          <a href="%s" style="color:#B7CFC3;font-size:15px" style-hover="color:#FAFAFA">%s</a>\n'%(href,label.replace('&','&amp;')))
        a('        </div>\n')
    a('      </div>\n')
    a('      <div style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding-top:24px">\n')
    a('        <div style="font-size:13.5px;line-height:1.7;color:#B7CFC3;max-width:74ch">Good Practice Supply supplies medical consumables only. We do not supply peptides, hormones or any prescription medicine. Australian approval status is shown per product where it applies. Nothing here is medical advice, so follow the directions of your prescriber or treating practitioner.</div>\n')
    a('        <div style="%s;font-size:11.5px;color:#B7CFC3;white-space:nowrap">&copy; 2026 Good Practice Supply</div>\n'%MONO)
    a('      </div>\n    </div>\n  </footer>')
    return ''.join(o)

FOOTER=build()
n=0
for pat in ['*.html','for/*.html','shop/*.html','shop/*/*.html','tools/*.html','learn/*.html']:
    for p in sorted(glob.glob(pat)):
        s=io.open(p,encoding='utf-8').read()
        i=s.find('  <footer'); j=s.find('</footer>')+len('</footer>')
        assert i>0 and j>i, p
        s2=s[:i]+FOOTER+s[j:]
        if s2!=s: io.open(p,'w',encoding='utf-8').write(s2); n+=1
print('sitewide footer applied to',n,'pages |',FOOTER.count('<a href'),'links per footer')
