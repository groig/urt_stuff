import os
import sqlite3
import jinja2
from time import sleep
import datetime
from pyquake3 import PyQuake3
from math import sqrt

server = PyQuake3("127.0.0.1:27960", rcon_password=os.getenv("RCON_PASSWORD"))
template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("index.j2")
conn = sqlite3.connect("data.sqlite")
conn.create_function("sqrt", 1, sqrt)
c = conn.cursor()

def main():
    print("generating")

    general_data = c.execute("WITH tmp01 AS (SELECT SUM(kills) AS sum_kills, SUM(deaths) + SUM(suicides) AS sum_deaths, MAX(ratio) AS max_ratio FROM xlrstats), tmp02 AS (SELECT a.name, a.rounds, a.kills, a.deaths, a.headshots, a.max_kill_streak, a.suicides, CASE WHEN a.kills = 0 THEN 0.0 WHEN a.kills > 0 AND (a.deaths + a.suicides) = 0 THEN max_ratio + 0.01 ELSE CAST(a.kills AS REAL) / (a.deaths + a.suicides) END tmp_ratio, COALESCE(CAST(a.kills AS REAL) * 100 / b.sum_kills, 0) AS tmp_lethality FROM xlrstats AS a, tmp01 AS b), tmp03 AS (SELECT name, rounds, kills, deaths, headshots, max_kill_streak, suicides, ROUND(tmp_ratio, 2) AS ratio, ROUND(tmp_lethality, 2) AS lethality, ROUND(CAST(tmp_ratio AS REAL) * SQRT(tmp_lethality), 3) AS tmp_score FROM tmp02), tmp04 AS (SELECT SUM(tmp_score) as sum_tmpscore FROM tmp03) SELECT a.name, a.rounds, a.kills, a.deaths, a.headshots, a.max_kill_streak, a.suicides, a.ratio, a.lethality, COALESCE(ROUND(CAST(a.tmp_score AS REAL) * 100 / b.sum_tmpscore, 2), 0) AS score FROM tmp03 AS a, tmp04 AS b ORDER BY score DESC, max_kill_streak DESC, headshots DESC, suicides ASC, deaths ASC, rounds ASC, name ASC").fetchall()

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

