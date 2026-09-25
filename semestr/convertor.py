import os
import csv

try:
    import pandas as pd
except ImportError:
    pd = None

class _Column:
    def __init__(self, items):
        self._items = items

    def tolist(self):
        return [str(x) for x in self._items]

class _SimpleDataFrame:
    def __init__(self, rows):
        self._rows = rows

    def __getitem__(self, key):
        return _Column([r[key] for r in self._rows])

    def iterrows(self):
        for idx, r in enumerate(self._rows):
            yield idx, r

    def __str__(self):
        return f"DataFrame({len(self._rows)} rows)"

# Načtení CSV souboru
def load_csv(file_path):
    if pd is not None:
        return pd.read_csv(file_path, delimiter=',', header=None, names=["Predmet", "Ucitel", "Den", "Zacatek", "Konec", "Typ"])
    cols = ["Predmet", "Ucitel", "Den", "Zacatek", "Konec", "Typ"]
    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for r in reader:
            if not r or not any(x.strip() for x in r):
                continue
            item = {}
            for i, col in enumerate(cols):
                item[col] = r[i].strip() if i < len(r) else ""
            rows.append(item)
    return _SimpleDataFrame(rows)

# Unikátní časy v setříděném pořadí
def fill_schedule(df):
    casovy_rozvrh = sorted(set(x.strip() for x in df["Zacatek"].tolist() + df["Konec"].tolist()), key=lambda x: tuple(map(int, x.split(':'))))

    dny_tydne = ["Po", "Út", "St", "Čt", "Pá"]
    rozvrh = {den: {cas: [] for cas in casovy_rozvrh} for den in dny_tydne}
    colspan_map = {den: {cas: 1 for cas in casovy_rozvrh} for den in dny_tydne}

    for _, row in df.iterrows():
        typ = str(row["Typ"]).strip()
        ucitel = f"<i>{str(row['Ucitel']).strip()}</i>"
        den = str(row["Den"]).strip()
        
        # --- Základní styl pro Dark Mode ---
        # box-sizing: border-box je důležité, aby padding nerozhodil šířku buňky
        # color: #eeeeee nastaví výchozí světlou barvu textu
        base_style = "padding: 6px; border-radius: 4px; display: block; box-sizing: border-box; color: #eeeeee; border: 1px solid transparent;" 
        style_css = base_style
        
        if typ == "P":
            # --- Přednáška ---
            # Tmavě zelené pozadí, světlejší zelený text, jemný zelený rámeček
            predmet = f"<b>{str(row['Predmet']).strip()}</b>"
            style_css += "background-color: #1b3a24; color: #c7e6d0; border-color: #2e5e40;" 
            
        elif typ == "Cv":
            # --- Cvičení ---
            # Tmavě hnědé/jantarové pozadí, světle žlutý text
            predmet = str(row['Predmet']).strip()
            style_css += "background-color: #4a3700; color: #fff3cd; border-color: #705a00;"
            
        elif typ == "Cvv":
            # --- Cvičení 1x za 2 týdny (Pruhovaná výplň) ---
            # Použijeme CSS trik s opakujícím se gradientem pro vytvoření pruhů.
            # Střídá se základní barva Cvičení (#4a3700) s ještě tmavším odstínem (#2e2200).
            predmet = str(row['Predmet']).strip()
            gradient_pattern = "repeating-linear-gradient(135deg, #4a3700, #4a3700 10px, #2e2200 10px, #2e2200 20px)"
            
            style_css += f"background-color: #4a3700; background-image: {gradient_pattern}; color: #fff3cd; border: 1px dashed #fff3cd;"
            # Přidal jsem i dashed rámeček světle žlutou barvou, aby to více vyniklo.
        
        elif typ == "Pp":
            # --- Přednáška 1x za 2 týdny (Pruhovaná výplň) ---
            # Střídá se základní barva Přednáška (#1b3a24) s ještě tmavším odstínem (#2e2200).
            predmet = f"<b>{str(row['Predmet']).strip()}</b>"
            gradient_pattern = "repeating-linear-gradient(135deg, #1b3a24, #1b3a24 10px, #2e2200 10px, #2e2200 20px)"
            
            style_css += f"background-color: #1b3a24; background-image: {gradient_pattern}; color: #c7e6d0; border: 1px dashed #c7e6d0;"
            # Přidal jsem i dashed rámeček světle zelenou barvou, aby to více vyniklo.
            
        else:
            # Ostatní - jen základní styl
            predmet = str(row['Predmet']).strip()

        # --- Uložení do rozvrhu ---
        if den in rozvrh:
            start = str(row["Zacatek"]).strip()
            end = str(row["Konec"]).strip()
            start_index = casovy_rozvrh.index(start)
            end_index = casovy_rozvrh.index(end)
            span = end_index - start_index
            
            if colspan_map[den][start] < span:
                colspan_map[den][start] = span
                
            if rozvrh[den][start] is None:
                rozvrh[den][start] = []
                
            rozvrh[den][start].append({
                "style": style_css,
                "predmet": predmet,
                "ucitel": ucitel
            })
            
            for i in range(start_index + 1, start_index + colspan_map[den][start]):
                rozvrh[den][casovy_rozvrh[i]] = None
                
    return rozvrh, dny_tydne, colspan_map, casovy_rozvrh

# Generování HTML tabulky
def fill_html(rozvrh, dny_tydne, colspan_map, casovy_rozvrh):
    html = """
    <h2 id="rozvrh">Rozvrh</h2>
    <table>
        <tr>
            <th>Čas / Den</th>
    """

    for cas in casovy_rozvrh:
        html += f"        <th>{cas}</th>\n"
    html += "    </tr>\n"

    for den in dny_tydne:
        html += f"    <tr>\n        <th>{den}</th>\n"
        for cas in casovy_rozvrh:
            if rozvrh[den][cas] is not None:
                colspan = colspan_map[den][cas]
                items = rozvrh[den][cas]
                if not items:
                    content = ""
                elif len(items) == 1:
                    it = items[0]
                    content = f"<div class='schedule-card' style='{it['style']} height: 100%;'>{it['predmet']}<br><small>{it['ucitel']}</small></div>"
                else:
                    inner = "".join(f"<div class='schedule-card' style='{it['style']} flex: 1;'>{it['predmet']}<br><small>{it['ucitel']}</small></div>" for it in items)
                    content = f"<div class='schedule-wrapper' style='display: flex; flex-direction: column; gap: 6px; height: 100%;'>{inner}</div>"

                if colspan > 1:
                    html += f"        <td colspan='{colspan}'>{content}</td>\n"
                else:
                    html += f"        <td>{content}</td>\n"
        html += "    </tr>\n"

    html += """
        </table>
    </body>
    </html>
    """
    return html

def save_html(html, pth):
    if os.path.exists(pth):
        with open(pth, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("</body>\n</html>", "").replace("</body></html>", "")
        with open(pth, "w", encoding="utf-8") as f:
            f.write(content + html)
    else:
        with open(pth, "a", encoding="utf-8") as f:
            f.write(html)