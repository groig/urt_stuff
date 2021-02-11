import sqlite3
import jinja2
from time import sleep

template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("index.j2")
conn = sqlite3.connect("data.sqlite")
c = conn.cursor()

def main():
    print("generating")

    general_data = c.execute("SELECT name, num_played, kills, deaths, headshots, max_kill_streak, suicides, ratio, rounds FROM xlrstats ORDER BY ratio DESC").fetchall()

    favorite_weapons = c.execute("select fragger, weapon, count(*) as frags from frags group by lower(fragger), lower(weapon) order by lower(fragger) asc, count(*) desc").fetchall()

    frags_repartition = c.execute("select fragger, fragged, count(*) as frags from frags group by lower(fragger), lower(fragged) order by lower(fragger) asc, count(*) desc").fetchall()
    frags_data = {}
    for frag in frags_repartition:
        if not frag[0] in frags_data:
            frags_data[frag[0]] = [(frag[1], frag[2])]
        else:
            frags_data[frag[0]].append((frag[1], frag[2]))

    deaths_repartition = c.execute("select fragged, fragger, count(*) from frags group by lower(fragged), lower(fragger) order by lower(fragged) asc, count(*) desc").fetchall()

    deaths_data = {}
    for frag in deaths_repartition:
        if not frag[0] in deaths_data:
            deaths_data[frag[0]] = [(frag[1], frag[2])]
        else:
            deaths_data[frag[0]].append((frag[1], frag[2]))

    output_text = template.render(general_data=general_data, favorite_weapons=favorite_weapons, frags_repartition=frags_data, deaths_repartition=deaths_data)

    with open("index.html", "w") as fh:
        fh.write(output_text)

if __name__ == "__main__":
        main()

