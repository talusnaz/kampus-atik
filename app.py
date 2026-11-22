def lookup_product(code):
    c = re.sub(r"\D", "", str(code or ""))
    if not c:
        return None
    # 1. Tam 13 hane eşleşmesi
    if c not in URUNLER_DB:
        # 2. Baştaki '8' okunmadıysa (12 hane geldiyse) başına '8' ekleyip dene
        if len(c) == 12 and ("8" + c) in URUNLER_DB:
            c = "8" + c
        # 3. Baştaki '8' yanlış rakam okunduysa (örn: 3 veya 6) son 12 haneden yakala
        elif len(c) == 13:
            for k in URUNLER_DB:
                if k[1:] == c[1:]:
                    c = k
                    break
    if c not in URUNLER_DB:
        return None
    item = URUNLER_DB[c]
    bin_code = BIN_CODE_MAP.get(item["kutu rengi"], "SARI")
    return {
        **item,
        "code": c,
        "name": item["ürün adı"],
        "bin": bin_code,
        "tip": f"{item['kutu etiketi']} ({item['kutu rengi']} Kutu - {item['pin']})",
        "grams": item["ağırlık gram"],
        "co2": item["co2 tasarruf gram"],
        "points": item["puan"]
    }
