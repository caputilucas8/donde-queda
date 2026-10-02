import json, os
here = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(here, 'template.html'), encoding='utf-8').read()
topo = json.load(open(os.path.join(here, 'ar.topo.json'), encoding='utf-8'))
cities = open(os.path.join(here, 'cities.json'), encoding='utf-8').read()
html = tpl.replace('/*__TOPO__*/null', json.dumps(topo, separators=(',', ':'), ensure_ascii=False)) \
          .replace('/*__CITIES__*/null', cities)
out_dir = os.path.dirname(here)  # la carpeta del proyecto, un nivel arriba de /fuente
out = os.path.join(out_dir, 'index.html')
open(out, 'w', encoding='utf-8').write(html)
print(out, len(html.encode('utf-8')) // 1024, 'KB')
