import json

import main


def run_console():
    console = main.Main()

    file_verified = False
    while not file_verified:
        file_verified = console.read_file(input("\nSave Game: "))

    running = True
    while running:
        cmd = input("\n\n(L)ist Wars, (V)iew a War, or (E)xit\nCommand: ")
        match cmd.upper():
            case 'L':
                headings = input("\n(A)ctive, (P)revious, or (B)oth?: ")
                match headings.upper():
                    case 'A':
                        headings = ["active_war"]
                    case 'P':
                        headings = ["previous_war"]
                    case 'B':
                        headings = ["active_war", "previous_war"]
                print(json.dumps(console.list_wars(headings), indent=4))

            case 'V':
                war = input("\nName of War?: ")
                print(json.dumps(console .view_war(war), indent=4))

            case 'E':
                running = False


if __name__ == "__main__":
    run_console()
