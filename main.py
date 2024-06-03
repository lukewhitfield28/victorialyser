import json


class Main:
    def __init__(self):
        self.history = ""
        self.heading_dict = {"active_war": False, "previous_war": False}

    def read_file(self, file):
        # Retrieve history
        try:
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

        except FileNotFoundError:
            return False

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

        self.history = json.loads(history, object_pairs_hook=merge_duplicates_keys)
        for h in ["active_war", "previous_war"]:
            self.heading_dict[h] = True if type(self.history[h]) is dict else False

        return True

    def list_wars(self, heading):
        wars = {}
        for h in heading:
            wars[h] = []
            if self.heading_dict[h]:
                wars[h].append(self.history[h]["name"])
            else:
                for i in self.history[h]:
                    wars[h].append(i["name"])
        return wars

    def view_war(self, war):
        def search(heading):
            record = ""
            if self.heading_dict[heading]:
                if self.history[heading]["name"].find(war) != -1:
                    record = self.history[heading]
            else:
                for i in self.history[heading]:
                    if i["name"].find(war) != -1:
                        record = i
                        break
            return record

        searched_record = search("active_war")
        if searched_record == "":
            searched_record = search("previous_war")

        return searched_record


if __name__ == "__main__":
    main = Main()
