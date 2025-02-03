import pandas as pd

# Načtení CSV souboru
def load_csv(file_path):
    df = pd.read_csv(file_path, delimiter=',', header=None, names=["Predmet", "Ucitel", "Den", "Zacatek", "Konec", "Typ"])
    return df

# Unikátní časy v setříděném pořadí
def fill_schedule(df):
    casovy_rozvrh = sorted(set(df["Zacatek"].tolist() + df["Konec"].tolist()), key=lambda x: tuple(map(int, x.split(':'))))

    dny_tydne = ["Po", "Út", "St", "Čt", "Pá"]
    rozvrh = {den: {cas: "" for cas in casovy_rozvrh} for den in dny_tydne}
    colspan_map = {den: {cas: 1 for cas in casovy_rozvrh} for den in dny_tydne}

    # Naplnění rozvrhu daty
    for _, row in df.iterrows():
        predmet = f"<b>{row['Predmet']}</b>" if row["Typ"].strip() == "P" else row['Predmet']
        ucitel = f"<i>{row['Ucitel']}</i>"
        den = row["Den"].strip()
        if den in rozvrh:
            start = row["Zacatek"]
            end = row["Konec"]
            start_index = casovy_rozvrh.index(start)
            end_index = casovy_rozvrh.index(end)
            colspan_map[den][start] = end_index - start_index
            rozvrh[den][start] = f"{predmet}<br>{ucitel}"
            for i in range(start_index + 1, end_index):
                rozvrh[den][casovy_rozvrh[i]] = None  # Značí, že tento slot je překrytý
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
                if colspan > 1:
                    html += f"        <td colspan='{colspan}'>{rozvrh[den][cas]}</td>\n"
                else:
                    html += f"        <td>{rozvrh[den][cas]}</td>\n"
        html += "    </tr>\n"

    html += """
        </table>
    </body>
    </html>
    """
    return html

def save_html(html, pth):
    with open(pth, "a", encoding="utf-8") as f:
        f.write(html)