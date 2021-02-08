import sqlite3
import os

from telegram.ext import CommandHandler, Updater

CURSOR = sqlite3.connect("data.sqlite", check_same_thread=False).cursor()


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

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(stats_handler)
    updater.dispatcher.add_handler(most_kills_handler)
    updater.dispatcher.add_handler(most_headshots_handler)
    updater.dispatcher.add_handler(most_deaths_handler)
    updater.dispatcher.add_handler(max_streak_handler)
    updater.dispatcher.add_handler(most_suicides_handler)
    updater.dispatcher.add_handler(best_ratio_handler)
    updater.dispatcher.add_handler(most_played_handler)

    updater.start_polling()


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="UrT stats")


def stats(update, context):
    if not context.args or len(context.args) > 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Give me a player name")
    else:
        CURSOR.execute(
            "SELECT name, num_played, kills, deaths, headshots, max_kill_streak, suicides, ratio, rounds FROM xlrstats WHERE name=?",
            context.args,
        )
        result = CURSOR.fetchall()
        if result:
            data = result[0]
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Name: {data[0]}\nNum. Played: {data[1]}\nKills: {data[2]}\nDeaths: {data[3]}\nHeadshots: {data[4]}\nMax Kill Streak: {data[5]}\nSuicides: {data[6]}\nRatio: {data[7]}",
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
        "SELECT name, num_played FROM xlrstats WHERE num_played = ( SELECT MAX(num_played) FROM xlrstats )",
        context.args,
    )
    data = CURSOR.fetchall()[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data[0]}: {data[1]} games played")
if __name__ == "__main__":
    main()
