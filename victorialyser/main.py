import json
from pathlib import Path


def load_presets():
    with open(Path("%s/data.json" % Path(__file__).parent), 'r') as df:
        data = json.load(df)
        return data["file"], data["folder"]


def try_file(file):
    if Path(file).is_file():
        with open(file, mode='r', encoding="latin_1") as f:
            for line in f.readlines():
                if line.find("active_war") != -1 or line.find("previous_war") != -1:
                    with open(Path("%s/data.json" % Path(__file__).parent), 'r+') as df:
                        data = json.load(df)
                        data["file"] = file
                        df.seek(0)
                        json.dump(data, df)
                        df.truncate()
                    return True
        return False
    else:
        return False


def try_folder(folder):
    if Path("%s/42960_install.vdf" % folder).is_file():
        with open(Path("%s/data.json" % Path(__file__).parent), 'r+') as df:
            data = json.load(df)
            data["folder"] = folder
            df.seek(0)
            json.dump(data, df)
        return True
    else:
        return False


def read_file(file):
    with open(file, mode='r', encoding="latin_1") as f:
        content = f.readlines()
        start, end = 0, 0

        active_wars = False
        for line in content:
            if line.find("active_war") != -1:
                start = content.index(line)
                keys = ["active_war", "previous_war"]
                active_wars = True
                break
        if not active_wars:
            for line in content:
                if line.find("previous_war") != -1:
                    start = content.index(line)
                    keys = ["previous_war"]
                    break

        for line in content[start:]:
            if line.find("invention=") != -1:
                end = content.index(line)
                break

    history = content[start:end]

    # Format line-by-line
    for ln in range(0, len(history)-1):
        line = history[ln]

        temp = "\""
        if line[:-2].find("=") == -1:
            temp += line[:-2].strip() + "\"="
        else:
            temp += line[:line.find("=")].strip() + "\"="
            if line[:-2].find("=\"") == -1:
                try:  # TODO: Consider if try/except statement can be avoided
                    int(line[line.find("=") + 1])
                    temp += line[line.find("=") + 1:].strip()
                except ValueError:
                    temp += "\"" + line[line.find("=") + 1:].strip() + "\""
            else:
                temp += line[line.find("=") + 1:].strip()

        if len(line.strip()) > 1:  # TODO: Consider moving this to the top of the loop to save processing whitespace
            history[ln] = temp.strip()

        history[ln] = history[ln].replace("=", ":")
        if history[ln].strip() != "{" and history[ln+1].strip() != "{" and history[ln+1].strip() != "}":
            history[ln] += ","

    # Finish formatting JSON String
    history.insert(0, "{")
    history.insert(-1, "}")
    history = ''.join(history)

    # Convert JSON String to Dictionary
    def merge_duplicates_keys(key_pair):
        dictionary = {}
        for key, value in key_pair:
            if key in dictionary:
                if type(dictionary[key]) is list:
                    dictionary[key].append(value)
                else:
                    dictionary[key] = [dictionary[key], value]
            else:
                dictionary[key] = value
        return dictionary

    history = json.loads(history, object_pairs_hook=merge_duplicates_keys)
    return history, keys


def _key_dict(dictionary, key):
    return True if type(dictionary[key]) is dict else False


def get_wars(history, keys):
    wars = {}
    for key in keys:
        wars[key] = []
        if _key_dict(history, key):
            wars[key].append(history[key]["name"])
        else:
            for war in history[key]:
                wars[key].append(war["name"])
    return wars


def get_record(history, war, key):
    record = {}
    if _key_dict(history, key):
        if history[key]["name"].find(war) != -1:
            record = history[key]
    else:
        for w in history[key]:
            if w["name"].find(war) != -1:
                record = w
                break
    return record


def get_tags(history, keys):
    tags = []

    def parse_record(record):
        def parse_event(event):
            if next(iter(event)) in ["add_attacker", "add_defender", "rem_attacker", "rem_defender"]:
                if event[next(iter(event))] not in tags:
                    tags.append(event[next(iter(event))])

        for date, item in record["history"].items():
            if type(item) is dict:
                parse_event(item)
            else:
                for subitem in item:
                    parse_event(subitem)

    for key in keys:
        if _key_dict(history, key):
            parse_record(history[key])
        else:
            for war in history[key]:
                parse_record(get_record(history, war["name"], key))

    return tags


def read_tags(folder, tags):
    all_tags = {}
    with open(Path("%s/common/countries.txt" % folder), 'r+') as f:
        content = f.readlines()
        for line in content:
            if line[5:8] == "= \"":
                all_tags[line[18:line.find(".txt")]] = line[:3]
            elif line[5:7] == "=\"":
                all_tags[line[17:line.find(".txt")]] = line[:3]
        for tag in tags:
            if tag not in all_tags.values():
                all_tags[tag] = tag
    return all_tags


def view_war(history, war, keys):
    if len(keys) == 1:
        record = get_record(history, war, "previous_war")
    else:
        record = get_record(history, war, "active_war")
        if record == {}:
            record = get_record(history, war, "previous_war")

    belligerents = {"active": {"attacker": [], "defender": []}, "previous": {"attacker": [], "defender": []}}
    battles = {}

    def parse(event, date):
        def amend_belligerents(key, add, remove, side):
            belligerents[add][side].append(event[key])
            if event[key] in belligerents[remove][side]:
                belligerents[remove][side].remove(event[key])

        if date == "battle":  # Battles in previous wars have no date, hence this confusing syntax
            battles[event["name"]] = event
        else:
            match next(iter(event)):
                # Belligerents
                case "add_attacker":
                    amend_belligerents(next(iter(event)), "active", "previous", "attacker")
                case "add_defender":
                    amend_belligerents(next(iter(event)), "active", "previous", "defender")
                case "rem_attacker":
                    amend_belligerents(next(iter(event)), "previous", "active", "attacker")
                case "rem_defender":
                    amend_belligerents(next(iter(event)), "previous", "active", "defender")
                # Battle
                case "battle":
                    battles[event["battle"]["name"] + " on " + date] = event["battle"]

    for d, item in record["history"].items():
        if type(item) is dict:
            parse(item, d)
        else:
            for subitem in item:
                parse(subitem, d)

    return belligerents, battles  # TODO: Return war goals


if __name__ == "__main__":
    pass
