import sys
sys.path.append('..')

from prompt_toolkit import prompt
from dataclasses import dataclass

import plankapy as ppy


@dataclass
class Context:
    # Instance
    planka: ppy.Planka = None
    auth: ppy.BaseAuth = None

    # Active objects
    project: ppy.Project = None
    user: ppy.User = None
    board: ppy.Board = None
    list: ppy.List = None
    card: ppy.Card = None

def get_auth(context: Context, url: str=None):
    if not url:
        url = prompt("Enter your Planka URL: ")

    method = prompt("Enter your authentication method (password, token): ")
    if method == "password":
        email = prompt("Enter your username or email: ")
        password = prompt("Enter your password: ", is_password=True)
        context.auth = ppy.PasswordAuth(email, password)

    elif method == "token":
        token = prompt("Enter your token: ")
        context.auth = ppy.TokenAuth(token)

    elif method == "help":
        print("Available authentication methods: 'password' | 'token', 'exit' to quit")

    elif method ==  "exit":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid authentication method")
        get_auth(context)

    context.planka = ppy.Planka(url, context.auth)

def get_next_input(input: str, context: Context):

    if input == "help" and not context.project:
        print("Available commands: 'projects', 'exit' to quit")
        get_next_input(prompt("> "), context)
    
    elif input == "projects" and not context.project:
        set_project(context)
        get_next_input(prompt("> "), context)

    elif input == "help" and context.project:
        print("Available commands: 'boards', 'exit' to quit")
        get_next_input(prompt("> "), context)

    elif input == "boards" and context.project:
        set_board(context)
        get_next_input(prompt("> "), context)

    elif input == "help" and context.board:
        print("Available commands: 'lists', 'users', 'labels', 'exit' to quit")
        get_next_input(prompt("> "), context)

    elif input == "exit":
        print("Exiting...")
        sys.exit(0)
    
    else:
        print("Invalid command")
        get_next_input(prompt("> "), context)

def set_project(context: Context):
    projects = context.planka.projects
    for i, project in enumerate(projects):
        print(f"{i+1}. {project.name}")
    
    project_id = int(prompt("Enter the project number: ")) - 1
    context.project = projects[project_id]

def set_board(context: Context):
    boards = context.project.boards
    for i, board in enumerate(boards):
        print(f"{i+1}. {board.name}")
    
    board_id = int(prompt("Enter the board number: ")) - 1
    context.board = boards[board_id]

def set_list(context: Context):
    lists = context.board.lists
    for i, list in enumerate(lists):
        print(f"{i+1}. {list.name}")
    
    list_id = int(prompt("Enter the list number: ")) - 1
    context.list = lists[list_id]

def set_card(context: Context):
    cards = context.list.cards
    for i, card in enumerate(cards):
        print(f"{i+1}. {card.name}")
    
    card_id = int(prompt("Enter the card number: ")) - 1
    context.card = cards[card_id]

def main(context: Context = Context()):
    print(f"Welcome to Plankapy v{ppy.__version__}\n")
    if not context.planka:
        get_auth(context)
    
    print(f"Logged in as {context.planka.me.name} {'(Admin)' if context.planka.me.isAdmin else ''}")
    print("Type 'help' for a list of commands")
    get_next_input(prompt("> "), context)

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue