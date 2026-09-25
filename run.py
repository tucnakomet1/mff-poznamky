import os
import re
import unicodedata
import argparse
import semestr.convertor as convertor

ALERT_MAP = {
    'note': ('alert-note', 'ℹ️ Poznámka'),
    'poznamka': ('alert-note', 'ℹ️ Poznámka'),
    'tip': ('alert-tip', '💡 Tip'),
    'important': ('alert-important', '❗ Důležité'),
    'dulezite': ('alert-important', '❗ Důležité'),
    'warning': ('alert-warning', '⚠️ Varování'),
    'varovani': ('alert-warning', '⚠️ Varování'),
    'upozorneni': ('alert-warning', '⚠️ Upozornění'),
    'caution': ('alert-caution', '🛑 Pozor'),
    'pozor': ('alert-caution', '🛑 Pozor'),
}


def process_alerts(html_content):
    """Převede GitHub-style callouty (> [!IMPORTANT], > [!WARNING], atd.) na stylované bloky s emoji."""
    def replacer(match):
        raw_type = match.group(1)
        norm = unicodedata.normalize('NFKD', raw_type).encode('ASCII', 'ignore').decode('utf-8').lower()
        if norm in ALERT_MAP:
            cls_name, title_text = ALERT_MAP[norm]
            return f'<blockquote class="alert {cls_name}">\n<div class="alert-title">{title_text}</div>\n<p>'
        return match.group(0)

    pattern = re.compile(
        r'<blockquote>\s*<p>\s*\[!([a-zA-Z\u00C0-\u017F]+)\]\s*(?:<br\s*/?>|</p>\s*<p>)?\s*',
        re.IGNORECASE
    )
    res = pattern.sub(replacer, html_content)
    res = re.sub(r'(<div class="alert-title">[^<]+</div>\s*)<p>\s*</p>', r'\1', res)
    return res


def get_available_semesters():
    """Vrátí seznam čísel dostupných semestrů ze složky semestr/."""
    semesters = []
    if os.path.exists("semestr"):
        for name in os.listdir("semestr"):
            path = os.path.join("semestr", name)
            if name.isdigit() and os.path.isdir(path):
                semesters.append(int(name))
    return sorted(semesters)


def convert_semester(i):
    """Konvertuje zadaný semestr (README.md -> html.html a přidá rozvrh)."""
    folder = f"semestr/{i}"
    readme_path = f"{folder}/README.md"
    html_path = f"{folder}/html.html"
    csv_path = f"{folder}/predmety.csv"

    if not os.path.exists(folder):
        print(f"Chyba: Složka '{folder}' neexistuje.")
        return False

    if not os.path.exists(readme_path):
        print(f"Chyba: Soubor '{readme_path}' neexistuje.")
        return False

    print(f"Konvertuji semestr {i} ({readme_path} -> {html_path})...")
    pandoc_cmd = f'pandoc -s -f markdown -t html5 --metadata pagetitle="{i}.semestr" -o {html_path} {readme_path} -c ../../theme.css'
    os.system(pandoc_cmd)

    # Zpracování alertů (> [!IMPORTANT], > [!WARNING], atd.)
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = process_alerts(content)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)

    if os.path.exists(csv_path):
        try:
            df = convertor.load_csv(csv_path)
            a, b, c, d = convertor.fill_schedule(df)
            html = convertor.fill_html(a, b, c, d)
            convertor.save_html(html, html_path)
        except Exception as e:
            print(f"Upozornění při zpracování rozvrhu pro semestr {i}: {e}")

    print(f"Semestr {i} hotov.")
    return True


def convert_main():
    """Konvertuje hlavní stránku (README.md -> index.html) s hlavičkou, alerty a tlačítkem zpět."""
    print("Konvertuji hlavní stránku (README.md -> index.html)...")
    pandoc_cmd = 'pandoc -s -f markdown -t html5 --metadata pagetitle="MFF - Poznámky a materiály" -o index.html README.md -c theme.css'
    os.system(pandoc_cmd)

    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        # Zpracování alertů
        content = process_alerts(content)

        # Přidání FontAwesome pro ikony v hlavičce
        fa_link = "<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'>"
        if fa_link not in content:
            content = content.replace(
                '<link rel="stylesheet" href="theme.css" />',
                f"{fa_link}\n  <link rel=\"stylesheet\" href=\"theme.css\" />"
            )

        # Přidání tlačítka zpět a hlavičky s autorem
        header_block = """<a href="https://tucnakomet1.github.io/" class="back-button">← Zpět</a>
<header id="title-block-header">
<h1 class="title" style="text-align: center;">MFF - Poznámky a materiály</h1>
<p class="author" style="text-align: center;">
  <a href="https://github.com/tucnakomet1/"><i class='fa fa-github'></i></a>
    Karel Velička
  <a href="https://tucnakomet1.github.io/"><i class='fa fa-link'></i></a>
</p>
<p class="email" style="text-align: center;"><a href="mailto:karel.velicka@protonmail.com">karel.velicka@protonmail.com</a></p>
</header>"""

        if '<header id="title-block-header">' not in content:
            if "<body>\n" in content:
                content = content.replace("<body>\n", f"<body>\n{header_block}\n")
            elif "<body>" in content:
                content = content.replace("<body>", f"<body>\n{header_block}\n")

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)

    print("Hlavní stránka (index.html) hotova.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Konvertor markdown poznámek do HTML pro MFF Poznámky.")
    parser.add_argument("-p", "--page", type=int, help="Číslo stránky (semestru) ke konverzi, např. -p 5")
    parser.add_argument("-a", "--all", action="store_true", help="Konvertovat všechno (hlavní stránku i všechny semestry)")
    parser.add_argument("-m", "--main", action="store_true", help="Konvertovat jen hlavní stránku")

    args = parser.parse_args()

    if not (args.page is not None or args.all or args.main):
        parser.print_help()
        return

    if args.all:
        convert_main()
        for sem in get_available_semesters():
            convert_semester(sem)
    else:
        if args.main:
            convert_main()
        if args.page is not None:
            convert_semester(args.page)


if __name__ == "__main__":
    main()
