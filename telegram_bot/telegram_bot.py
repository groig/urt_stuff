import sqlite3
import os
from pyquake3 import PyQuake3

from telegram.ext import CommandHandler, Updater

CURSOR = sqlite3.connect("data.sqlite", check_same_thread=False).cursor()

server = PyQuake3("127.0.0.1:27960", rcon_password=os.getenv("RCON_PASSWORD"))

def main():
    updater = Updater(token=os.getenv("TELEGRAM_TOKEN"), use_context=True)

    start_handler = CommandHandler("start", start)
    stats_handler = CommandHandler("stats", stats)
    most_kills_handler = CommandHandler("most_kills", most_kills)
    most_deaths_handler = CommandHandler("most_deaths", most_deaths)
    most_headshots_handler = CommandHandler("most_headshots", most_headshots)
    max_streak_handler = CommandHandler("max_streak", max_streak)
    most_suicides_handler = CommandHandler("most_suicides", most_suicides)
    best_ratio_handler = CommandHandler("best_ratio", best_ratio)
    most_played_handler = CommandHandler("most_played", most_played)
    top_ten_kills_handler = CommandHandler("top_ten_kills", top_ten_kills)
    top_ten_ratio_handler = CommandHandler("top_ten_ratio", top_ten_ratio)
    player_count_handler = CommandHandler("player_count", player_count)
    kills_per_round_handler = CommandHandler("kills_per_round", kills_per_round)
    deaths_per_round_handler = CommandHandler("deaths_per_round", deaths_per_round)
    suicides_per_round_handler = CommandHandler("suicides_per_round", suicides_per_round)
    headshots_per_round_handler = CommandHandler("headshots_per_round", headshots_per_round)
    server_status_handler = CommandHandler("server_status", server_status)
    stream_handler = CommandHandler("stream", stream)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(stats_handler)
    updater.dispatcher.add_handler(most_kills_handler)
    updater.dispatcher.add_handler(most_headshots_handler)
    updater.dispatcher.add_handler(most_deaths_handler)
    updater.dispatcher.add_handler(max_streak_handler)
    updater.dispatcher.add_handler(most_suicides_handler)
    updater.dispatcher.add_handler(best_ratio_handler)
    updater.dispatcher.add_handler(most_played_handler)
    updater.dispatcher.add_handler(top_ten_kills_handler)
    updater.dispatcher.add_handler(top_ten_ratio_handler)
    updater.dispatcher.add_handler(player_count_handler)
    updater.dispatcher.add_handler(kills_per_round_handler)
    updater.dispatcher.add_handler(deaths_per_round_handler)
    updater.dispatcher.add_handler(suicides_per_round_handler)
    updater.dispatcher.add_handler(headshots_per_round_handler)
    updater.dispatcher.add_handler(server_status_handler)
    updater.dispatcher.add_handler(stream_handler)

    updater.start_polling()


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="UrT stats")


def stats(update, context):
    if not context.args or len(context.args) > 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Give me a player name")
    else:
        CURSOR.execute(
            "SELECT name, rounds, kills, deaths, headshots, max_kill_streak, suicides, ratio, rounds FROM xlrstats WHERE name=?",
            context.args,
        )
        result = CURSOR.fetchall()
        if result:
            data = result[0]
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Name: {data[0]}\nRounds: {data[1]}\nKills: {data[2]}\nDeaths: {data[3]}\nHeadshots: {data[4]}\nMax Kill Streak: {data[5]}\nSuicides: {data[6]}\nRatio: {data[7]}",
            )
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No player found")


def kills_per_round(update, context):
    if not context.args or len(context.args) > 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Give me a player name")
    else:
        CURSOR.execute(
            "SELECT name, round(CAST(kills AS FLOAT)/rounds,2) FROM xlrstats WHERE name=?",
            context.args,
        )
        result = CURSOR.fetchall()
        if result:
            data = result[0]
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Name: {data[0]}\nKills/Round: {data[1]}",
            )
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No player found")


def deaths_per_round(update, context):
    if not context.args or len(context.args) > 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Give me a player name")
    else:
        CURSOR.execute(
            "SELECT name, round(CAST(deaths AS FLOAT)/rounds,2) FROM xlrstats WHERE name=?",
            context.args,
        )
        result = CURSOR.fetchall()
        if result:
            data = result[0]
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Name: {data[0]}\nDeaths/Round: {data[1]}",
            )
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No player found")
            
def suicides_per_round(update, context):
    if not context.args or len(context.args) > 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Give me a player name")
    else:
        CURSOR.execute(
            "SELECT name, round(CAST(suicides AS FLOAT)/rounds,2) FROM xlrstats WHERE name=?",
            context.args,
        )
        result = CURSOR.fetchall()
        if result:
            data = result[0]
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Name: {data[0]}\nSuicides/Round: {data[1]}",
            )
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No player found")
            
def headshots_per_round(update, context):
    if not context.args or len(context.args) > 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Give me a player name")
    else:
        CURSOR.execute(
            "SELECT name, round(CAST(headshots AS FLOAT)/rounds,2) FROM xlrstats WHERE name=?",
            context.args,
        )
        result = CURSOR.fetchall()
        if result:
            data = result[0]
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Name: {data[0]}\nHeadshots/Round: {data[1]}",
            )
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No player found")


def most_kills(update, context):
    CURSOR.execute(
        "SELECT name, kills FROM xlrstats WHERE kills = ( SELECT MAX(kills) FROM xlrstats )",
        context.args,
    )
    data = CURSOR.fetchall()[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data[0]}: {data[1]} kills")


def most_headshots(update, context):
    CURSOR.execute(
        "SELECT name, headshots FROM xlrstats WHERE headshots = ( SELECT MAX(headshots) FROM xlrstats )",
        context.args,
    )
    data = CURSOR.fetchall()[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data[0]}: {data[1]} headshots")


def most_deaths(update, context):
    CURSOR.execute(
        "SELECT name, deaths FROM xlrstats WHERE deaths = ( SELECT MAX(deaths) FROM xlrstats )",
        context.args,
    )
    data = CURSOR.fetchall()[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data[0]}: {data[1]} deaths")


def most_suicides(update, context):
    CURSOR.execute(
        "SELECT name, suicides FROM xlrstats WHERE suicides = ( SELECT MAX(suicides) FROM xlrstats )",
        context.args,
    )
    data = CURSOR.fetchall()[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data[0]}: {data[1]} suicides")


def max_streak(update, context):
    CURSOR.execute(
        "SELECT name, max_kill_streak FROM xlrstats WHERE max_kill_streak = ( SELECT MAX(max_kill_streak) FROM xlrstats )",
        context.args,
    )
    data = CURSOR.fetchall()[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data[0]}: {data[1]} kills")

def best_ratio(update, context):
    CURSOR.execute(
        "SELECT name, ratio FROM xlrstats WHERE ratio = ( SELECT MAX(ratio) FROM xlrstats )",
        context.args,
    )
    data = CURSOR.fetchall()[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data[0]}: {data[1]} k/d ratio")

def most_played(update, context):
    CURSOR.execute(
        "SELECT name, rounds FROM xlrstats WHERE rounds = ( SELECT MAX(rounds) FROM xlrstats )",
        context.args,
    )
    data = CURSOR.fetchall()[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data[0]}: {data[1]} games played")

def top_ten_kills(update, context):
    CURSOR.execute(
        "SELECT name, kills FROM xlrstats ORDER BY kills DESC LIMIT 10",
        context.args,
    )
    data = CURSOR.fetchall()
    players = [f"{player[0]}: {player[1]}" for player in data]
    context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(players))

def top_ten_ratio(update, context):
    CURSOR.execute(
        "SELECT name, ratio FROM xlrstats ORDER BY ratio DESC LIMIT 10",
        context.args,
    )
    data = CURSOR.fetchall()
    players = [f"{player[0]}: {player[1]}" for player in data]
    context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(players))

def player_count(update, context):
    CURSOR.execute(
        "SELECT COUNT(guid) FROM xlrstats;",
        context.args,
    )
    data = CURSOR.fetchall()[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data[0]} players have pulled the trigger")

def server_status(update, context):
    server.update()
    server_data = f"running map {server.values[b'mapname'].decode()} with {len(server.players)} player(s)."
    players_data = "\n".join([f"{player.name} with {player.frags} frags and a {player.ping} ms ping" for player in server.players])
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{server_data}\n{players_data}")

def stream(update, context):
    filename = "telegram-stream"
    if not context.args:
        msg = "Stream is off"
        if os.path.exists("telegram-stream"):
            msg = "Stream is on"
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    elif len(context.args) > 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong args")
    else:
        operation = context.args[0].lower()
        if operation == "on":
            if not os.path.exists(filename):
                open(filename, "a").close()
            context.bot.send_message(chat_id=update.effective_chat.id, text="Stream is on")
        elif operation == "off":
            if os.path.exists(filename):
                os.remove(filename)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Stream is off")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="u dumb")

if __name__ == "__main__":
    main()
