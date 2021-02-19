import os
import sqlite3
import jinja2
from time import sleep
import datetime
from pyquake3 import PyQuake3
from math import log

server = PyQuake3("127.0.0.1:27960", rcon_password=os.getenv("RCON_PASSWORD"))
template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("index.j2")
conn = sqlite3.connect("data.sqlite")
conn.create_function("log", 1, log)
c = conn.cursor()

def main():
    print("generating")

    general_data = c.execute('WITH tmp00 AS ( SELECT name, rounds, kills, deaths, deaths + suicides AS realdeaths, ratio, headshots, max_kill_streak AS streak, suicides FROM xlrstats ), tmp01 AS ( SELECT SUM(kills) AS sum_kills, MAX(ratio) AS max_ratio FROM tmp00 ), tmp02 AS ( SELECT a.name, a.rounds, a.kills, a.deaths, a.realdeaths, a.headshots, a.streak, a.suicides, CASE WHEN a.kills = 0 THEN 0.0 WHEN a.realdeaths > 0 THEN CAST(a.kills AS REAL) / a.realdeaths ELSE 0.01 + max_ratio END tmp_ratio, COALESCE(100.0 * a.kills / b.sum_kills, 0.0) AS tmp_lethality FROM tmp00 AS a, tmp01 AS b ), tmp03 AS ( SELECT name, rounds, kills, deaths, realdeaths, headshots, streak, suicides, tmp_ratio, tmp_lethality, tmp_ratio * LOG(1.0 + tmp_lethality) AS tmp_score FROM tmp02 ), tmp04 AS ( SELECT SUM(tmp_score) as sum_tmpscore FROM tmp03 ) SELECT a.name, a.rounds, a.kills, a.deaths, a.headshots, a.streak, a.suicides, PRINTF("%.2f", ROUND(tmp_ratio, 2)) AS ratio, PRINTF("%.2f", ROUND(tmp_lethality, 2)) AS lethality, PRINTF("%.2f", COALESCE(ROUND(100.0 * a.tmp_score / b.sum_tmpscore, 2), 0.0)) AS score FROM tmp03 AS a, tmp04 AS b ORDER BY a.tmp_score DESC, a.streak DESC, a.headshots DESC, a.realdeaths ASC, a.suicides ASC, a.rounds ASC, a.name ASC').fetchall()

    favorite_weapons = c.execute("select fragger, weapon, count(*) as frags from frags group by lower(fragger), lower(weapon) order by lower(fragger) asc, count(*) desc").fetchall()

    weapons_data = {}
    for player in favorite_weapons:
        if not player[0] in weapons_data:
            weapons_data[player[0]] = [(player[1].replace('UT_MOD_', ''), player[2])]
        else:
            weapons_data[player[0]].append((player[1].replace('UT_MOD_', ''), player[2]))

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

    server.update()
    server_data = f"Running map {server.values[b'mapname'].decode()} with {len(server.players)} player(s)."
    players_data = [f"{player.name} with {player.frags} frags and a {player.ping} ms ping" for player in server.players]
    output_text = template.render(general_data=general_data, favorite_weapons=weapons_data, frags_repartition=frags_data, deaths_repartition=deaths_data, server_data=server_data, players_data=players_data, dt=datetime.datetime.now())

    with open("index.html", "w") as fh:
        fh.write(output_text)

if __name__ == "__main__":
        main()

