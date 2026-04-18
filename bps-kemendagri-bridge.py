import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

BASE = "https://sig.bps.go.id/rest-bridging/getwilayah"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (research scraper)"})

def fetch(level=None, parent=None):
    params = {}
    if level:  params["level"] = level
    if parent: params["parent"] = parent
    r = S.get(BASE, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def walk(parents, level, workers=16):
    out = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(fetch, level, p): p for p in parents}
        for f in tqdm(as_completed(futures), total=len(futures), desc=level):
            out.extend(f.result())
    return out

# 1. Provinsi (34–38 rows)
prov = fetch()
# 2. Kabupaten/Kota (~514)
kab  = walk([p["kode_bps"] for p in prov], "kabupaten")
# 3. Kecamatan (~7,160)
kec  = walk([k["kode_bps"] for k in kab],  "kecamatan")
# 4. Desa/Kelurahan (~83,000)
desa = walk([k["kode_bps"] for k in kec],  "desa")

df = pd.DataFrame(desa)
df.to_csv("bridging_bps_kemendagri.csv", index=False)
print(df.head())
print(f"Total: {len(df):,} desa/kelurahan")
