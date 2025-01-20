import sys
sys.path.append('..')

import plankapy as pk

if __name__ == '__main__':
    auth = pk.PasswordAuth(username_or_email='demo', password='demo')
    planka = pk.Planka('http://localhost:3000', auth=auth)
    
    # Create a new project
    project = planka.create_project(name='Test Project')
    
    # Create a new board
    board = project.create_board(name='Test Board', position=1)
    
    # Create a new list
    _list = board.create_list(name='Test List 1', position=3)
    
    # Label Options
    labels_options: list[tuple[str, pk.LabelColor]] = [
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