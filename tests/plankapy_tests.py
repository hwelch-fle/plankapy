from plankapy import *
import random

def test_planka():
    planka = Planka(API_URL, API_USER, API_PASS)
    project = Project(planka)
    board = Board(planka)
    lst = List(planka)
    card = Card(planka)
    label = Label(planka)
    task = Task(planka)
    attachment = Attachment(planka)
    stopwatch = Stopwatch(planka)
    background = Background(planka)
    comment = Comment(planka)
    user = User(planka)

    if "Plankapy Test Project" in [prj["name"] for prj in project.get()["items"]]:
        project.delete("Plankapy Test Project")


    project.build(name="Plankapy Test Project")
    project.create()
    print("Created Test Project")

    next_pos = OFFSET
    for i in range(1,5):
        board.build(name=f"Test Board {i}", type="kanban", position=next_pos)
        board.create("Plankapy Test Project")
        next_pos += OFFSET
        print(f"Created Test Board {i}")

    new_labels = {}
    for b in board.get("Plankapy Test Project"):
        new_labels[b['name']] = []
        next_pos = OFFSET
        for color in label.colors():
            label.build(name=f"{color} label", color=color, position=next_pos)
            new_labels[b['name']].append(label.create("Plankapy Test Project", b["name"])["item"])
            next_pos += OFFSET
            print(f"Created {color} Label for Board {b['name']}")

    new_lists = {}
    for b in board.get("Plankapy Test Project"):
        new_lists[b['name']] = []
        next_pos = OFFSET
        for i in range(1,5):
            lst.build(name=f"Test List {i}", position=next_pos)
            new_lists[b['name']].append(lst.create("Plankapy Test Project", b["name"]))
            next_pos += OFFSET
            print(f"Created Test List {i} for Board {b['name']}")

    new_cards={}
    for b in board.get("Plankapy Test Project"):
        new_cards[b['name']] = []
        next_pos = OFFSET
        for i in range(1, 11):
            card.build(name=f"Test Card {i}", description=f"CHANGE ME {i}", position=next_pos)
            next_pos += OFFSET
            new_cards[b['name']].append(card.create("Plankapy Test Project", b['name'], "Test List 1")["item"])
            print(f"Created Test Card {i} for Board {b['name']} in Test List 1")

    for b in board.get("Plankapy Test Project"):
        for cd in new_cards[b['name']]:
            lb = random.choice(new_labels[b['name']])
            label.add(label_id=lb["id"], card_id=cd["id"])
        print(f"added random labels to cards in board {b['name']}")
        for _ in range(len(new_cards[b['name']]) // 2):
            cd = random.choice(new_cards[b['name']])
            lbs = card.get_labels("Plankapy Test Project", b["name"], oid=cd["id"])
            for lb in lbs:
                label.remove(label_id=lb["labelId"], card_id=lb["cardId"])
                print(f"removed label from {cd['name']}")
        print(f"removed random labels from half the cards in {b['name']}")

    new_tasks={}
    for b in board.get("Plankapy Test Project"):
        new_tasks[b['name']] = []
        for cd in new_cards[b['name']]:
            next_pos=OFFSET
            for i in range(1,5):
                task.build(name=f"Test Task {i}", position=next_pos)
                next_pos += OFFSET
                new_tasks[b['name']].append(task.create(card_id=cd["id"])["item"])
            print(f"Created 4 tasks on {cd['name']}")
    for b in board.get("Plankapy Test Project"):
        for tsk in new_tasks[b['name']]:
            task.build(name=f"Updated Task: {tsk['name']}", isCompleted=True)
            task.update(oid=tsk["id"])
        print("Updated task all tasks")

    for grad in background.gradients():
        grad = grad
        background.build(name=grad, type="gradient")
        background.apply("Plankapy Test Project")
        print(f"Applied gradient {grad} to Test Project")

    background.clear("Plankapy Test Project")
    print("Cleared gradient from Test Project")
    for us in user.get():
        print(f"Username: {us['username']}\nEmail: {us['email']}")
    print("Tests complete")

if __name__ == "__main__":
    test_planka()