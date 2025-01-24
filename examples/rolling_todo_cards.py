# Written for:
# https://github.com/plankanban/planka/issues/1002

import plankapy as ppy
from plankapy import Planka, PasswordAuth

from datetime import datetime, timedelta, date

def get_project_by_name(planka: Planka, name: str):
    for project in planka.projects:
        if project.name == name:
            return project
    return None

def get_board_by_date(project: ppy.Project, date: date):
    for board in project.boards:
        if board.name == f"{date.year}":
            return board
    return None

def get_card_by_date(list: ppy.List, date: date):
    for card in list.cards:
        if card.name == f"Todo {date.day}/{date.month}/{date.year}":
            return card
    return None

def get_list_by_date(board: ppy.Board, date: date):
    for list in board.lists:
        if list.name == f"{date.strftime('%B')} {date.year}":
            return list
    return None

def main():
    
    # Flag for defaulting to last card in yesterday's list
    # if no card is found for yesterday
    default_to_last_card = True
    
    planka = Planka('http://localhost:3001/', auth=PasswordAuth("demo", "demo"))
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    project = get_project_by_name(planka, "Daily Tasks")
    if not project:
        print("Project not found")
        return

    yesterday_board = get_board_by_date(project, yesterday)
    if not yesterday_board:
        print("Yesterday's Board not found")
        return
    
    yesterday_list = get_list_by_date(yesterday_board, yesterday)
    if not yesterday_list:
        print("Yesterday's List not found")
        return
    
    yesterday_card = get_card_by_date(yesterday_list, yesterday)
    if not yesterday_card:
        if len(yesterday_list.cards) > 0 and default_to_last_card:
            yesterday_card = yesterday_list.cards[0]
        else:
            print("Yesterday's Card not found")
            return
    
    today_board = get_board_by_date(project, today)
    if not today_board:
        today_board = project.create_board(f"{today.year}")
        print(f"Created board for {today.year}")
    
    today_list = get_list_by_date(today_board, today)
    if not today_list:
        today_list = today_board.create_list(f"{today.strftime('%B')} {today.year}")
        print(f"Created List for {today.strftime('%B')} {today.year}")
        
    today_card = get_card_by_date(today_list, today)
    if not today_card:
        print(f"Creating Card for {today.strftime('%d/%m/%Y')}")
        today_card = yesterday_card.duplicate()
        today_card.move(today_list)
        with today_card.editor():
            today_card.name = f"Todo {today.day}/{today.month}/{today.year}"
            today_card.position = 0
            
        for task in today_card.tasks:
            if task.isCompleted:
                print(f"{task.name} completed on {yesterday.strftime('%d/%m/%Y')}, good job!")
                task.delete()
                
    else:
        print("Today's Card already exists!")
    
    print("Created Today's Card")
    
if __name__ == '__main__':
    main()