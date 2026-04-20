import csv
import difflib
import re
from urllib.parse import urlparse

# ==============================================
# LOAD DATASET (Whitelist + Blacklist)
# ==============================================
def load_dataset():
    whitelist = []
    blacklist = []

    with open("dataset/whitelist.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            brand = row.get("brand")
            domain = row.get("domain")
            dtype = row.get("type")

            if not brand or not domain or not dtype:
                continue

            domain = domain.lower().strip()

            if dtype in ["main", "login", "reset"]:
                whitelist.append(domain)
            elif dtype == "phishing":
                blacklist.append(domain)

    return whitelist, blacklist

# ==============================================
# NORMALISASI KARAKTER MIRIP (untuk similarity saja)
# ==============================================
def normalize_domain(domain):
    replacements = {
        "0": "o",
        "1": "l",
        "3": "e",
        "5": "s",
        "@": "a"
    }
    for k, v in replacements.items():
        domain = domain.replace(k, v)
    return domain

# ==============================================
# STRING SIMILARITY
# ==============================================
def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

# ==============================================
# FUNGSI UTAMA DETEKSI
# ==============================================
def cek_typo_phishing(url):
    whitelist, blacklist = load_dataset()

    # Ambil hanya domain pertama kalau input ada koma
    url = url.split(",")[0].strip()

    parsed = urlparse(url if url.startswith("http") else "http://" + url)
    domain = parsed.netloc.lower() + parsed.path.lower()
    normalized_domain = normalize_domain(domain)

    hasil = f"""
==================================================
HASIL ANALISIS DOMAIN
==================================================
URL              : {url}
Domain dianalisis: {domain}
==================================================
"""

    # 1️⃣ CEK BLACKLIST (PHISHING)
    if domain in blacklist:
        hasil += """
Status: PHISHING
Keterangan: Domain terdeteksi sebagai phishing (blacklist).
==================================================
"""
        return hasil, "phishing"

    # 2️⃣ CEK WHITELIST (LEGIT) → pakai domain asli, bukan normalisasi
    if domain in whitelist:
        hasil += """
Status: LEGIT
Keterangan: Domain terdaftar sebagai domain resmi (whitelist).
==================================================
"""
        return hasil, "legit"

    # 3️⃣ CEK KEMIRIPAN (TYPOSQUATTING) → pakai normalisasi
    for legit_domain in whitelist:
        score = similarity(normalized_domain, legit_domain)
        if score >= 0.85 and domain != legit_domain:
            hasil += f"""
Indikasi Typosquatting Terdeteksi
Domain mencurigakan : {domain}
Mirip dengan domain : {legit_domain}
Similarity Score    : {score:.2f}

Status: PHISHING
==================================================
"""
            return hasil, "phishing"

    # 4️⃣ DOMAIN DI LUAR CAKUPAN
    hasil += """
Status: TIDAK DIKETAHUI
Keterangan: Domain tidak terdaftar dalam whitelist maupun blacklist.
==================================================
"""
    return hasil, "unknown"
