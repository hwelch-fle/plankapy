# Written for:
# https://github.com/plankanban/planka/issues/1002

import plankapy as ppy
from plankapy import Planka, PasswordAuth
from typing import Optional

from datetime import datetime, timedelta, date

def board_name(date: date) -> str:
    return f"{date.year}"

def list_name(date: date) -> str:
    return f"{date.strftime('%B')} {date.year}"

def card_name(date: date) -> str:
    return f"Todo {date.day}/{date.month}/{date.year}"

def main():
    planka = Planka('http://localhost:3001/', auth=PasswordAuth("demo", "demo"))
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    project = planka.projects.pop_where(name="Daily Tasks")
    yesterday_board = project.boards.pop_where(name=board_name(yesterday))
    yesterday_list = yesterday_board.lists.pop_where(name=list_name(yesterday))
    yesterday_card = yesterday_list.cards.pop_where(name=card_name(yesterday)) or yesterday_list.cards.pop()
    
    today_board = (
        project.boards.pop_where(name=board_name(today)) or
        project.create_board(board_name(today))
    )
    
    today_list = (
        today_board.lists.pop_where(name=list_name(today)) or
        today_board.create_list(list_name(today))
    )
        
    today_card = (
        today_list.cards.pop_where(name=card_name(today)) or
        yesterday_card.duplicate()
    )
    if today_card.name == card_name(today):
        print(f"Today's card already exists! {today_card.link}")
        return
        
    today_card.move(today_list)
    
    with today_card.editor():
        today_card.name = card_name(today)
        today_card.position = 0
    
    # Abuse of the QueryableList (for fun)
    #today_card.tasks.filter_where(
    #    isCompleted=True
    #    ).select_where(
    #        lambda task:
    #            task.delete() and
    #            print(f"Task {task.name} complete {yesterday.strftime('%d/%m/%Y')} ,Good Job!") 
    #    )
    
    # Do it this way
    for task in today_card.tasks.filter_where(isCompleted=True):
        task.delete()
        print(f"Task {task.name} complete {yesterday.strftime('%d/%m/%Y')} ,Good Job!")
    
if __name__ == '__main__':
    main()