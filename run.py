import os
import semestr.convertor as convertor

for i in range(4, 6):
    folder = f"semestr/{i}"
    pandoc_cmd = f"pandoc -s -f markdown -t html5 -o {folder}/html.html {folder}/README.md -c ../../theme.css"
    os.system(pandoc_cmd)

    df = convertor.load_csv(folder + "/predmety.csv")
    a,b,c,d = convertor.fill_schedule(df)
    html = convertor.fill_html(a,b,c,d)
    convertor.save_html(html, folder + "/html.html")