import json


save = ""


def read_file(file):
    # Retrieve history
    with open(file, mode='r', encoding="latin_1") as f:
        content = f.readlines()
        start, end = 0, 0

        for line in content:
            if line.find("active_war") != -1:
                start = content.index(line)
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
                try:
                    int(line[line.find("=") + 1])
                    temp += line[line.find("=") + 1:].strip()
                except ValueError:
                    temp += "\"" + line[line.find("=") + 1:].strip() + "\""
            else:
                temp += line[line.find("=") + 1:].strip()

        if len(line.strip()) > 1:
            history[ln] = temp.strip()

        history[ln] = history[ln].replace("=", ":")
        if history[ln].strip() != "{" and history[ln+1].strip() != "{" and history[ln+1].strip() != "}":
            history[ln] += ","

    # Finish formatting the JSON String
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
    print(json.dumps(history, indent=4))


if __name__ == "__main__":
    read_file(save)
