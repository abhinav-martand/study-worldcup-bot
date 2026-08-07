        import os
import telebot

TOKEN = "8931443042:AAGZkYIwKSLkOhBtc_uPDVw4YRstm1opbAg"
bot = telebot.TeleBot(TOKEN)

# Updated Data State
data = {
    "Spain": {
        "flag": "🇪🇸",
        "emoji": "⚽️",
        "players": {
            "Raiii": 48.0,
            "Srishti": 74.0,
            "ELON MUSK": 37.0,
            "Priyanshu": 21.0,
            "Zoe": 21.0,
            "Anwesha": 20.0,
        },
        "extra_notes": {"Srishti": "(+9)"},
    },
    "Portugal": {
        "flag": "🇵🇹",
        "emoji": "⚽️",
        "players": {
            "Positron": 77.0,
            "Ishant": 51.0,
            "Saumya": 23.0,
            "Madhav": 23.0,
            "Tennessine": 18.0,
            "Yuvraj": 11.0,
        },
        "extra_notes": {"Positron": "(+16)"},
    },
    "England": {
        "flag": "🏴",
        "emoji": "⚽️",
        "players": {
            "Xeelzyx": 44.5,
            "Phoenix": 40.0,
            "Hrishabh": 28.0,
            "Kanishk": 26.0,
            "Hanjue": 28.0,
            "Parth": 16.0,
        },
        "extra_notes": {},
    },
    "Argentina": {
        "flag": "🇦🇷",
        "emoji": "⚽️",
        "players": {
            "Sarthak": 53.0,
            "Raunak": 39.0,
            "James": 23.0,
            "A": 17.0,
            "Iota": 28.0,
            "Samosapav": 15.0,
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
            # Format float values nicely (remove .0 if whole number)
            score_val = int(score) if score.is_integer() else score
            note = f" {info['extra_notes'][player]}" if player in info['extra_notes'] else ""
            text += f"- {player} — {score_val}{note}\n"
        
        team_tot_val = int(team_totals[country]) if team_totals[country].is_integer() else team_totals[country]
        text += f"\nTeam Goals: {team_tot_val} ⚽️\n\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    text += "🌍 TEAM STANDINGS\n\n"
    for country, total in sorted_teams:
        tot_val = int(total) if total.is_integer() else total
        text += f"- {country} — {tot_val} ⚽️\n"
    text += "\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    all_players = []
    for country, info in data.items():
        for player, score in info["players"].items():
            all_players.append((player, score))

    all_players.sort(key=lambda x: x[1], reverse=True)
    top_players = all_players[:4]

    text += "👑 GOLDEN BOOT\n\n"
    for player, score in top_players:
        sc_val = int(score) if score.is_integer() else score
        text += f"- {player} — {sc_val}\n"

    return text

@bot.message_handler(commands=['add'])
def add_hours(message):
    thread_id = getattr(message, 'message_thread_id', None)
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
            bot.send_message(message.chat.id, generate_report(), message_thread_id=thread_id)
        else:
            bot.send_message(message.chat.id, f"❌ Player '{player_name}' not found.", message_thread_id=thread_id)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Usage format error. Use like: `/add ELON MUSK 8`", parse_mode="Markdown", message_thread_id=thread_id)

@bot.message_handler(commands=['list', 'start'])
def send_list(message):
    thread_id = getattr(message, 'message_thread_id', None)
    bot.send_message(message.chat.id, generate_report(), message_thread_id=thread_id)

bot.infinity_polling()
