import time
from plankapy import PasswordAuth, Planka

def setup(planka: Planka):
    portal_projects = [p for p in planka.projects if p.name == 'Portal']
    portal_project = portal_projects[0] if portal_projects else None
    if not portal_project:
        planka.create_project('Portal')

    board_a = None
    board_b = None

    to_b = None
    to_a = None
    from_b = None
    from_a = None

    for board in portal_project.boards:
        if board.name == 'Board A':
            board_a = board
        elif board.name == 'Board B':
            board_b = board
    
    if not board_a:
        board_a = portal_project.create_board('Board A')
    if not board_b:
        board_b = portal_project.create_board('Board B')
    
    for list_ in board_a.lists:
        if list_.name == 'To Board B':
            to_b = list_
        elif list_.name == 'From Board B':
            from_b = list_
    
    for list_ in board_b.lists:
        if list_.name == 'To Board A':
            to_a = list_
        elif list_.name == 'From Board A':
            from_a = list_

    if not to_b:
        to_b = board_a.create_list('To Board B')
    if not to_a:
        from_b = board_a.create_list('From Board B')
    if not to_a:
        to_a = board_b.create_list('To Board A')
    if not from_a:
        from_a = board_b.create_list('From Board A')
    
    return to_b, to_a, from_b, from_a

if __name__ == '__main__':
    planka = Planka('http://localhost:3000', PasswordAuth('demo', 'demo'))

    to_b, to_a, from_b, from_a = setup(planka)
        
    while True:
        for card in to_b.cards:
            card.move(from_a)
            print(f'Moved card {card.name} from Board A to Board B')

        for card in to_a.cards:
            card.move(from_b)
            print(f'Moved card {card.name} from Board B to Board A')
        
        time.sleep(1) # Only poll every second