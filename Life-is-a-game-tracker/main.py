import json
import os
from datetime import datetime

SAVE_FILE = "save.json"

# ---------- LOAD / SAVE ----------
def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            print("⚠️ Save corrupted. Resetting.")
    
    return {
        "xp": 0,
        "actions": {},   # stored actions with XP
        "log": [],
        "streak": 0,
        "last_date": ""
    }

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- LOGIC ----------
def level(xp):
    return xp // 100

def update_streak(data):
    today = datetime.now().date()

    if data["last_date"]:
        last = datetime.fromisoformat(data["last_date"]).date()
        diff = (today - last).days

        if diff == 1:
            data["streak"] += 1
        elif diff > 1:
            data["streak"] = 1
    else:
        data["streak"] = 1

    data["last_date"] = today.isoformat()

# ---------- DISPLAY ----------
def show_stats(data):
    lvl = level(data["xp"])
    next_xp = (lvl + 1) * 100

    print("\n" + "="*40)
    print(f"✨ LEVEL: {lvl}")
    print(f"⚡ XP: {data['xp']} / {next_xp}")
    print(f"🔥 STREAK: {data['streak']} days")
    print("="*40)

# ---------- MAIN ----------
def main():
    data = load_data()

    print("🎮 LIFE RPG")

    while True:
        show_stats(data)

        print("\nMENU:")
        print("1 → Add New Action (set XP)")
        print("2 → Do Action (log your day)")
        print("3 → View Log")
        print("4 → Exit")

        choice = input("\nChoose: ").strip()

        # ---------- ADD NEW ACTION ----------
        if choice == "1":
            name = input("Action name: ").strip().lower()

            if not name:
                print("⚠️ Empty name.")
                continue

            xp_input = input("XP for this action (default 10): ").strip()

            if xp_input.isdigit():
                xp = int(xp_input)
            else:
                xp = 10

            data["actions"][name] = xp
            save_data(data)

            print(f"✅ Saved '{name}' with {xp} XP")

        # ---------- DO ACTION ----------
        elif choice == "2":
            if not data["actions"]:
                print("⚠️ No actions saved yet.")
                continue

            print("\nAvailable actions:")
            for act, xp in data["actions"].items():
                print(f"- {act} ({xp} XP)")

            done = input("\nWhat did you do: ").strip().lower()

            if done in data["actions"]:
                xp_gain = data["actions"][done]
            else:
                print("⚠️ Action not found. Defaulting to 10 XP.")
                xp_gain = 10

            data["xp"] += xp_gain
            update_streak(data)

            data["log"].append(f"{done} (+{xp_gain} XP)")

            print(f"💥 Gained {xp_gain} XP!")

            save_data(data)

        # ---------- VIEW LOG ----------
        elif choice == "3":
            print("\n📜 LOG:")
            for item in data["log"][-10:]:
                print("-", item)

        # ---------- EXIT ----------
        elif choice == "4":
            save_data(data)
            print("Saved. Keep leveling up.")
            break

        else:
            print("Invalid choice")

# ---------- RUN ----------
if __name__ == "__main__":
    main()