import os
import telebot

TOKEN = "8931443042:AAGZkYIwKSLkOhBtc_uPDVw4YRstm1opbAg"
bot = telebot.TeleBot(TOKEN)

data = {
    "Portugal": {
        "flag": "🇵🇹",
        "emoji": "⚽️",
        "players": {
            "Ishant": 0.0,
            "Iota": 0.0,
            "Xeelzyx": 0.0,
            "Madhav": 0.0,
            "Ananjan": 0.0,
        },
        "extra_notes": {"Ishant": "(Captain 🇨)"},
    },
    "France": {
        "flag": "🇫🇷",
        "emoji": "⚽️",
        "players": {
            "Positron": 0.0,
            "Hrishabh": 0.0,
            "Phoenix": 0.0,
            "Parth": 0.0,
            "Khasim": 0.0,
        },
        "extra_notes": {"Positron": "(Captain 🇨)"},
    },
    "Argentina": {
        "flag": "🇦🇷",
        "emoji": "⚽️",
        "players": {
            "Raunak": 0.0,
            "Samosapav": 0.0,
            "Saumya": 0.0,
            "Hanjue": 0.0,
            "Yuvraj": 0.0,
        },
        "extra_notes": {"Raunak": "(Captain 🇨)"},
    },
    "England": {
        "flag": "🏴",
        "emoji": "⚽️",
        "players": {
            "Sarthak": 0.0,
            "James": 0.0,
            "Tennessine": 0.0,
            "Kanishk": 0.0,
            "A": 0.0,
        },
        "extra_notes": {"Sarthak": "(Captain 🇨)"},
    },
    "Spain": {
        "flag": "🇪🇸",
        "emoji": "⚽️",
        "players": {
            "Raiii": 0.0,
            "Srishti": 0.0,
            "ELON MUSK": 0.0,
            "Zoe": 0.0,
            "Anwesha": 0.0,
        },
        "extra_notes": {},
    },
}

def generate_report():
    team_totals = {}
    for country, info in data.items():
        team_totals[country] = sum(info["players"].values())

    sorted_teams = sorted(team_totals.items(), key=lambda x: x[1], reverse=True)

    text = "🏆 STUDY WORLD CUP — S3\n\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    for country, info in data.items():
        text += f"{info['flag']} {country}\n"
        for player, score in info["players"].items():
            score_val = int(score) if score.is_integer() else score
            # Check for captain label or extra notes
            note_str = ""
            if player in info["extra_notes"]:
                note_str = f" {info['extra_notes'][player]}"
            
            text += f"- {player} — {score_val}{note_str}\n"
        
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

@bot.message_handler(commands=['addplayer'])
def add_player(message):
    thread_id = getattr(message, 'message_thread_id', None)
    try:
        parts = message.text.split(maxsplit=1)[1]
        *name_parts, target_country = parts.rsplit(maxsplit=1)
        player_name = " ".join(name_parts).strip()

        matched_country = None
        for country in data.keys():
            if country.lower() == target_country.lower():
                matched_country = country
                break

        if not matched_country:
            bot.send_message(message.chat.id, f"❌ Country '{target_country}' not found.", message_thread_id=thread_id)
            return

        exists = False
        for country, info in data.items():
            for p_name in info["players"]:
                if p_name.lower() == player_name.lower():
                    exists = True
                    break
            if exists:
                break

        if exists:
            bot.send_message(message.chat.id, f"⚠️ Player '{player_name}' already exists! Use /shift to move them.", message_thread_id=thread_id)
            return

        data[matched_country]["players"][player_name] = 0.0
        bot.send_message(message.chat.id, generate_report(), message_thread_id=thread_id)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Usage format error. Use like: `/addplayer John Spain`", parse_mode="Markdown", message_thread_id=thread_id)

@bot.message_handler(commands=['subtract'])
def subtract_hours(message):
    thread_id = getattr(message, 'message_thread_id', None)
    try:
        parts = message.text.split(maxsplit=1)[1]
        *name_parts, hours_str = parts.rsplit(maxsplit=1)
        player_name = " ".join(name_parts).strip()
        hours_to_sub = float(hours_str)

        found = False
        for country, info in data.items():
            for p_name in info["players"]:
                if p_name.lower() == player_name.lower():
                    info["players"][p_name] -= hours_to_sub
                    found = True
                    break
            if found:
                break

        if found:
            bot.send_message(message.chat.id, generate_report(), message_thread_id=thread_id)
        else:
            bot.send_message(message.chat.id, f"❌ Player '{player_name}' not found.", message_thread_id=thread_id)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Usage format error. Use like: `/subtract ELON MUSK 5`", parse_mode="Markdown", message_thread_id=thread_id)

@bot.message_handler(commands=['shift'])
def shift_player(message):
    thread_id = getattr(message, 'message_thread_id', None)
    try:
        parts = message.text.split(maxsplit=1)[1]
        *name_parts, target_country = parts.rsplit(maxsplit=1)
        player_name = " ".join(name_parts).strip()

        matched_country = None
        for country in data.keys():
            if country.lower() == target_country.lower():
                matched_country = country
                break

        if not matched_country:
            bot.send_message(message.chat.id, f"❌ Country '{target_country}' not found.", message_thread_id=thread_id)
            return

        found_player = None
        player_score = 0
        player_note = None

        for country, info in data.items():
            for p_name in list(info["players"].keys()):
                if p_name.lower() == player_name.lower():
                    found_player = p_name
                    player_score = info["players"].pop(p_name)
                    if p_name in info["extra_notes"]:
                        player_note = info["extra_notes"].pop(p_name)
                    break
            if found_player:
                break

        if not found_player:
            bot.send_message(message.chat.id, f"❌ Player '{player_name}' not found anywhere.", message_thread_id=thread_id)
            return

        data[matched_country]["players"][found_player] = player_score
        if player_note:
            data[matched_country]["extra_notes"][found_player] = player_note

        bot.send_message(message.chat.id, generate_report(), message_thread_id=thread_id)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Usage format error. Use like: `/shift ELON MUSK Argentina`", parse_mode="Markdown", message_thread_id=thread_id)

@bot.message_handler(commands=['remove'])
def remove_player(message):
    thread_id = getattr(message, 'message_thread_id', None)
    try:
        player_name = message.text.split(maxsplit=1)[1].strip()

        found = False
        for country, info in data.items():
            for p_name in list(info["players"].keys()):
                if p_name.lower() == player_name.lower():
                    info["players"].pop(p_name)
                    if p_name in info["extra_notes"]:
                        info["extra_notes"].pop(p_name)
                    found = True
                    break
            if found:
                break

        if found:
            bot.send_message(message.chat.id, generate_report(), message_thread_id=thread_id)
        else:
            bot.send_message(message.chat.id, f"❌ Player '{player_name}' not found.", message_thread_id=thread_id)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Usage format error. Use like: `/remove ELON MUSK`", parse_mode="Markdown", message_thread_id=thread_id)

@bot.message_handler(commands=['reset'])
def reset_scores(message):
    thread_id = getattr(message, 'message_thread_id', None)
    try:
        for country, info in data.items():
            for p_name in info["players"]:
                info["players"][p_name] = 0.0

        bot.send_message(message.chat.id, "🔄 Season 3 scores reset to 0!\n\n" + generate_report(), message_thread_id=thread_id)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Error resetting scores.", message_thread_id=thread_id)

@bot.message_handler(commands=['list', 'start'])
def send_list(message):
    thread_id = getattr(message, 'message_thread_id', None)
    bot.send_message(message.chat.id, generate_report(), message_thread_id=thread_id)

bot.infinity_polling()
    
