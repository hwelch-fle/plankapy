import sys
sys.path.append('../src')

import time
import asyncio
from pathlib import Path
from plankapy import Planka, PasswordAuth, QueryableList, List, Card, Attachment, Board

planka = Planka('http://localhost:3000', PasswordAuth('demo', 'demo'))

def setup_board_sync(attachment: Path) -> Board:
    project = planka.create_project("Async Test")
    board = project.create_board("Async Board")

    lists: QueryableList[List] = QueryableList()
    for list_name in ("To Do", "Doing", "Done"):
        lists.append(board.create_list(list_name))
    
    for list in lists:
        for i in range(1, 101):
            c = list.create_card(f"Card {i} - {list.name}")
            if attachment:
                c.add_attachment(attachment)
    
    return board

async def create_cards(count: int, lists: list[List], attachment: Path):
    for _ in (
        list.create_card(f"Card {i} - {list.name}").add_attachment(attachment) 
        for i in range(1, count) 
        for list in lists
        if attachment):
        pass

async def setup_board_async(attachment: Path) -> Board:
    project = planka.create_project("Async Test")
    board = project.create_board("Async Board")

    lists: QueryableList[List] = QueryableList()
    for list_name in ("To Do", "Doing", "Done"):
        lists.append(board.create_list(list_name))
    
    await create_cards(101, lists, attachment)
    return board

def batch_attach_sync(cards: list[Card], attachment: Path):
    return [card.add_attachment(attachment) for card in cards if attachment]

async def batch_attach_async(cards: list[Card], attachment: Path):
    tasks = (card.add_attachment(attachment) for card in cards if attachment)
    return await asyncio.gather(*tasks)

def cleanup_project():
    planka.projects.pop_where(name="Async Test").delete()

if __name__ == "__main__":
    attachment = Path('https://upload.wikimedia.org/wikipedia/commons/d/dc/RCA_Indian_Head_test_pattern.png')
    test_type = 'both'

    if test_type == 'async' or 'both':
        try:
            print('Started Async Test')
            t1 = time.time()
            board = asyncio.run(setup_board_async(attachment))
            t2 = time.time()
            print(f"Finished async in {t2-t1:.2f} seconds")
        finally:
            cleanup_project()
    
    if test_type == 'sync' or 'both':
        try:
            print('Started Sync Test')
            t1 = time.time()
            board = setup_board_sync(attachment)
            t2 = time.time()
            print(f"Finished sync in {t2-t1:.2f} seconds")
        finally:
            cleanup_project()


