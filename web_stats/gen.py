import sqlite3
import jinja2
from time import sleep

def main():
    print("generating")
    conn = sqlite3.connect("data.sqlite")
    c = conn.cursor()
    c.execute("SELECT name, num_played, kills, deaths, headshots, max_kill_streak, suicides, ratio, rounds FROM xlrstats")
    data = c.fetchall()
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("index.j2")
    output_text = template.render(data=data)
    with open("index.html", "w") as fh:
        fh.write(output_text)

if __name__ == "__main__":
    while True:
        main()
        print("sleeping")
        sleep(300)
