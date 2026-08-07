import os
import telebot

TOKEN = "8931443042:AAGZkYIwKSLkOhBtc_uPDVw4YRstm1opbAg"
bot = telebot.TeleBot(TOKEN)

data = {
    "Spain": {
        "flag": "🇪🇸",
        "emoji": "⚽️",
        "players": {
            "Raiii": 48,
            "Srishti": 74,
            "ELON MUSK": 29,
            "Priyanshu": 21,
            "Zoe": 21,
            "Anwesha": 20,
        },
        "extra_notes": {"Srishti": "(+9)"},
    },
    "Portugal": {
        "flag": "🇵🇹",
        "emoji": "⚽️",
        "players": {
            "Positron": 77,
            "Ishant": 51,
            "Saumya": 23,
            "Madhav": 23,
            "Tennessine": 18,
            "Yuvraj": 11,
        },
        "extra_notes": {"Positron": "(+16)"},
    },
    "England": {
        "flag": "🏴",
        "emoji": "⚽️",
        "players": {
            "Xeelzyx": 44.5,
            "Phoenix": 31,
            "Hrishabh": 28,
            "Kanishk": 26,
            "Hanjue": 21,
            "Parth": 16,
        },
        "extra_notes": {},
    },
    "Argentina": {
        "flag": "🇦🇷",
        "emoji": "⚽️",
        "players": {
            "Sarthak": 53,
            "Raunak": 39,
            "James": 23,
            "A": 17,
            "Iota": 21,
            "Samosapav": 15,
        },
        "extra_notes": {"Sarthak": "(was 31, +22)"},
    },
}

def generate_report():
    team_totals = {}
    for country, info in data.items():
        team_totals[country] = sum(info["players"].values())

    sorted_teams = sorted(team_totals.items(), key=lambda x: x[1], reverse=True)

    text = "🏆 STUDY WORLD CUP — S2\n\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    for country, info in data.items():
        text += f"{info['flag']} {country}\n"
        for player, score in info["players"].items():
            note = f" {info['extra_notes'][player]}" if player in info['extra_notes'] else ""
            text += f"- {player} — {score}{note}\n"
        text += f"\nTeam Goals: {team_totals[country]} ⚽️\n\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    text += "🌍 TEAM STANDINGS\n\n"
    for country, total in sorted_teams:
        text += f"- {country} — {total} ⚽️\n"
    text += "\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    all_players = []
    for country, info in data.items():
        for player, score in info["players"].items():
            all_players.append((player, score))

    all_players.sort(key=lambda x: x[1], reverse=True)
    top_players = all_players[:4]

    text += "👑 GOLDEN BOOT\n\n"
    for player, score in top_players:
        text += f"- {player} — {score}\n"

    return text

@bot.message_handler(commands=['add'])
def add_hours(message):
    try:
        parts = message.text.split(maxsplit=1)[1]
        *name_parts, hours_str = parts.rsplit(maxsplit=1)
        player_name = " ".join(name_parts).strip()
        hours_to_add = float(hours_str)

        found = False
        for country, info in data.items():
            for p_name in info["players"]:
                if p_name.lower() == player_name.lower():
                    info["players"][p_name] += hours_to_add
                    found = True
                    break
            if found:
                break

        if found:
            bot.send_message(message.chat.id, generate_report())
        else:
            bot.send_message(message.chat.id, f"❌ Player '{player_name}' not found.")
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Usage format error. Use like: `/add ELON MUSK 8`", parse_mode="Markdown")

@bot.message_handler(commands=['list', 'start'])
def send_list(message):
    bot.send_message(message.chat.id, generate_report())

bot.infinity_polling()

