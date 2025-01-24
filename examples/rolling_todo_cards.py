# Written for:
# https://github.com/plankanban/planka/issues/1002

import plankapy as ppy
from plankapy import Planka, PasswordAuth
from typing import Optional

from datetime import datetime, timedelta, date

def get_project_by_name(planka: Planka, name: str) -> Optional[ppy.Project]:
    for project in planka.projects:
        if project.name == name:
            return project

def get_board_by_date(project: ppy.Project, date: date) -> Optional[ppy.Board]:
    for board in project.boards:
        if board.name == f"{date.year}":
            return board

def get_card_by_date(list: ppy.List, date: date) -> Optional[ppy.Card]:
    for card in list.cards:
        if card.name == f"Todo {date.day}/{date.month}/{date.year}":
            return card

def get_list_by_date(board: ppy.Board, date: date) -> Optional[ppy.List]:
    for list in board.lists:
        if list.name == f"{date.strftime('%B')} {date.year}":
            return list

def main():
    
    # Flag for defaulting to last card in yesterday's list
    # if no card is found for yesterday
    default_to_last_card = True
    
    planka = Planka('http://localhost:3001/', auth=PasswordAuth("demo", "demo"))
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    if not (project := get_project_by_name(planka, "Daily Tasks")):
        print("Project not found")
        return

    if not (yesterday_board := get_board_by_date(project, yesterday)):
        print("Yesterday's Board not found")
        return
    
    if not (yesterday_list := get_list_by_date(yesterday_board, yesterday)):
        print("Yesterday's List not found")
        return
    
    if not (yesterday_card := get_card_by_date(yesterday_list, yesterday)):
        if len(yesterday_list.cards) > 0 and default_to_last_card:
            yesterday_card = yesterday_list.cards[0]
        else:
            print("Yesterday's Card not found")
            return
    
    if not (today_board := get_board_by_date(project, today)):
        today_board = project.create_board(f"{today.year}")
        print(f"Created board for {today.year}")
    
    if not (today_list := get_list_by_date(today_board, today)):
        today_list = today_board.create_list(f"{today.strftime('%B')} {today.year}")
        print(f"Created List for {today.strftime('%B')} {today.year}")
        
    if not (today_card := get_card_by_date(today_list, today)):
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
        print(f"Card: {today_card.link}")
        return
    
    print(f"Created Today's Card\n {today_card.link}")
    
if __name__ == '__main__':
    main()