import time

import sys
sys.path.append('../src')

from plankapy import PasswordAuth, Planka

def place_portals(planka: Planka):
    portal_project = (
        planka.projects.pop_where(name='Portal') or 
        planka.create_project('Portal', background='blueish-curve')
    )
    
    # Set up the test chambers
    chamber_one = (
        portal_project.boards.pop_where(name='Chamber One') or 
        portal_project.create_board('Chamber One')
    )
    
    chamber_two = (
        portal_project.boards.pop_where(name='Chamber Two') or 
        portal_project.create_board('Chamber Two')
    )
    
    # Place the Orange Portal
    orange_enter = (
        chamber_one.lists.pop_where(name=f'To {chamber_two.name}') or 
        chamber_one.create_list(name=f'To {chamber_two.name}', position=9999999999)
    )
    orange_exit = (
        chamber_two.lists.pop_where(name=f'From {chamber_one.name}') or 
        chamber_two.create_list(f'From {chamber_one.name}', position=1)
    )
    
    # Place the Blue Portal
    blue_enter = (
        chamber_two.lists.pop_where(name=f'To {chamber_one.name}') or 
        chamber_two.create_list(f'To {chamber_one.name}', position=9999999999)
    )
    
    blue_exit = (
        chamber_one.lists.pop_where(name=f'From {chamber_two.name}') or 
        chamber_one.create_list(f'From {chamber_two.name}', position=1)
    )
    
    # Place Player
    player = (
        chamber_one.cards.pop_where(name='Chell') or 
        chamber_two.cards.pop_where(name='Chell') or 
        orange_exit.create_card('Chell').add_member(planka.me)
    )
    
    return orange_enter, orange_exit, blue_enter, blue_exit, player

if __name__ == '__main__':
    planka = Planka('http://localhost:3001', PasswordAuth('demo', 'demo'))

    orange_enter, orange_exit, blue_enter, blue_exit, player = place_portals(planka)
    
    while True:
        for card in orange_enter.cards:
            card.move(orange_exit)
            print(f'{card.name} Entered Orange Portal')
            
        for card in blue_enter.cards:
            card.move(blue_exit)
            print(f'{card.name} Entered Blue Portal')
            
        time.sleep(1) # Only poll every second