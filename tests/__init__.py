import sys
sys.path.append('..')

import asyncio
import time
import plankapy as ppy

async def async_range(count):
    for i in range(count):
        yield(i)
        await asyncio.sleep(0.0)

async def async_create_card(i, _list: ppy.List):
    _list.create_card(name=f"Card {i}", position=i+1)

async def async_create_cards(n: int, _list: ppy.List):
    start = time.time()
    async for i in async_range(n):
        await async_create_card(i, _list)
    end = time.time()
    print(f"Done in {end - start:.2f} seconds (asynchronously)")

if __name__ == '__main__':
    auth = ppy.PasswordAuth(username_or_email='demo', password='demo')
    planka = ppy.Planka('http://localhost:3000', auth=auth)
    
    # Create a new project
    project = planka.create_project(name='Test Project')
    
    # Create a new board
    board = project.create_board(name='Test Board', position=1)
    
    # Create a new list
    _list = board.create_list(name='Test List 1', position=0)
    _list2 = board.create_list(name='Test List 2', position=1)

    # Label Options
    labels_options: list[tuple[str, ppy.LabelColor]] = [
        ('Label 1', 'antique-blue'), 
        ('Label 2', 'coral-green'), 
        ('Label 3', 'berry-red')
    ]
    
    # Generate and capture labels
    labels = [
        label := board.create_label(name=label_name, color=color, position=0) 
        for label_name, color in labels_options
    ]
    
    # Create a new card
    card = _list.create_card(name='Test Card 1', position=2)
    
    # Add Comment to Card
    comment = card.add_comment(comment='Test Comment 1')
    
    # Add User to card
    membership = card.add_member(user=planka.me)
    
    # Added user
    user = membership.user
    
    # Add Label to card
    for label in labels:
        card.add_label(label)
    
    # Add Description to card
    with card.editor():
        import this
        card.description = this.s

    # Add Checklist to card
    for task in ['Task 1', 'Task 2', 'Task 3']:
        card.add_task(name=task)

    # Duplicate Card
    card2 = card.duplicate()

    # Move Card
    card2.move(_list2)

    # Stress test with async
    print("Creating 100 cards asynchronously")
    t = asyncio.create_task(async_create_cards(100, _list2))

    # Create 100 cards synchronously
    print("Creating 100 cards synchronously")
    start = time.time()
    for i in range(100):
        _list.create_card(name=f"Card {i}", position=i+1)
    end = time.time()
    print(f"Done in {end - start:.2f} seconds (syncronously)")
    
    
    project = \
    {
        board : 
            {
                _list: _list.cards
                for _list in board.lists
            }
        for board in project.boards
    }