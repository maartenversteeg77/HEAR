"""Gedeelde tekening van de blokjes (20 nov): schuin van boven, ronde noppen, in de huiskleuren.
Gebruikt door bouw-samenstellen.py. De pagina's hebben dezelfde tekening in JavaScript (ISO_JS)
voor de stapel die groeit; houd beide gelijk."""
# Blokjes, schuin van boven getekend met ronde noppen (20 nov, 'route 3'). Eigen tekening, in de kleuren van de samensteller.
# Dezelfde tekening staat in het script onderaan de pagina (functie isoStapel) voor de stapel die groeit; houd beide gelijk.
KLEUR = {"geluid": "#D47763", "personeel": "#7AC3C9", "licht": "#E9D36B", "scherm": "#C9C8C2", "wit": "#F6F5F1"}

def _tint(kleur, f):
    n = int(kleur[1:], 16)
    return "rgb(%d,%d,%d)" % tuple(round(v * f) for v in (n >> 16, (n >> 8) & 255, n & 255))

def iso_stapel(kleuren, u=40, dik=2, klasse=""):
    """SVG van op elkaar gestapelde blokjes (2 x 2 noppen), onderste eerst."""
    c, s_, h = 0.866, 0.5, u * 0.9
    W = D = 2 * u
    rr = u * 0.29
    rx, ry, sh = rr * 1.2247, rr * 0.7071, u * 0.2
    st = f'stroke="#191A19" stroke-width="{dik}" stroke-linejoin="round"'
    g = ""
    for i, k in enumerate(kleuren):
        z = i * h
        P = lambda x, y, zz: ((x - y) * c, (x + y) * s_ - zz - z)
        pts = lambda a: " ".join(f"{px:.1f},{py:.1f}" for px, py in a)
        g += (f'<polygon points="{pts([P(0, D, h), P(W, D, h), P(W, D, 0), P(0, D, 0)])}" fill="{_tint(k, .86)}" {st}/>'
              f'<polygon points="{pts([P(W, D, h), P(W, 0, h), P(W, 0, 0), P(W, D, 0)])}" fill="{_tint(k, .72)}" {st}/>'
              f'<polygon points="{pts([P(0, 0, h), P(W, 0, h), P(W, D, h), P(0, D, h)])}" fill="{k}" {st}/>')
        for a, b in sorted(((a, b) for a in (0, 1) for b in (0, 1)), key=lambda q: q[0] + q[1]):
            px, py = P((a + .5) * u, (b + .5) * u, h)
            g += (f'<path d="M{px - rx:.1f},{py - sh:.1f}V{py:.1f}A{rx:.1f},{ry:.1f} 0 0 0 {px + rx:.1f},{py:.1f}V{py - sh:.1f}Z" fill="{_tint(k, .8)}" {st}/>'
                  f'<ellipse cx="{px:.1f}" cy="{py - sh:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{k}" {st}/>')
    x0, x1 = -D * c - 3, W * c + 3
    y0, y1 = -h - (len(kleuren) - 1) * h - sh - ry - 3, (W + D) * s_ + 3
    return f'<svg class="{klasse}" viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}" aria-hidden="true" focusable="false">{g}</svg>'

# Dezelfde tekening voor in de pagina: tint() en isoStapel(lijst van kleuren, onderste eerst).
ISO_JS = r"""function tint(k,f){var n=parseInt(k.slice(1),16);return 'rgb('+[n>>16,(n>>8)&255,n&255].map(function(v){return Math.round(v*f)}).join(',')+')'}
function isoStapel(kl){var u=40,c=0.866,s=0.5,h=u*0.9,W=2*u,D=2*u,rr=u*0.29,rx=rr*1.2247,ry=rr*0.7071,sh=u*0.2,st='stroke="#191A19" stroke-width="2" stroke-linejoin="round"',g='';
 kl.forEach(function(k,i){var z=i*h;function P(x,y,zz){return [(x-y)*c,(x+y)*s-zz-z]}function pts(a){return a.map(function(p){return p[0].toFixed(1)+','+p[1].toFixed(1)}).join(' ')}
  g+='<polygon points="'+pts([P(0,D,h),P(W,D,h),P(W,D,0),P(0,D,0)])+'" fill="'+tint(k,.86)+'" '+st+'/><polygon points="'+pts([P(W,D,h),P(W,0,h),P(W,0,0),P(W,D,0)])+'" fill="'+tint(k,.72)+'" '+st+'/><polygon points="'+pts([P(0,0,h),P(W,0,h),P(W,D,h),P(0,D,h)])+'" fill="'+k+'" '+st+'/>';
  [[0,0],[0,1],[1,0],[1,1]].forEach(function(q){var p=P((q[0]+.5)*u,(q[1]+.5)*u,h);g+='<path d="M'+(p[0]-rx)+','+(p[1]-sh)+'V'+p[1]+'A'+rx+','+ry+' 0 0 0 '+(p[0]+rx)+','+p[1]+'V'+(p[1]-sh)+'Z" fill="'+tint(k,.8)+'" '+st+'/><ellipse cx="'+p[0]+'" cy="'+(p[1]-sh)+'" rx="'+rx+'" ry="'+ry+'" fill="'+k+'" '+st+'/>'})});
 var x0=-D*c-3,x1=W*c+3,y0=-h-(kl.length-1)*h-sh-ry-3,y1=(W+D)*s+3;return '<svg viewBox="'+x0+' '+y0+' '+(x1-x0)+' '+(y1-y0)+'" aria-hidden="true" focusable="false">'+g+'</svg>'}"""
