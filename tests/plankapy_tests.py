# -*- coding: utf-8 -*-
from plankapy import Planka
from controllers import Project, Board, Card, List, Stopwatch, Label, Task, CommentAction, Attachment, User, CardMembership, BoardMembership, CardLabel, ProjectManager, Background

API_URL = "http://planka.corp.finelines-engineering.com"
API_USER = "hwelch"
API_PASS = "Fiber4u!"

planka = Planka(API_URL, API_USER, API_PASS)

ProjectController = Project(instance=planka, name="Test Project 2", description="Test Project Description")
BoardController = Board(instance=planka)
CardController = Card(instance=planka)
ListController = List(instance=planka)
StopwatchController = Stopwatch(instance=planka)
LabelController = Label(instance=planka)
TaskController = Task(instance=planka)
CommentActionController = CommentAction(instance=planka)
AttachmentController = Attachment(instance=planka)
UserController = User(instance=planka)
CardMembershipController = CardMembership(instance=planka)
BoardMembershipController = BoardMembership(instance=planka)
CardLabelController = CardLabel(instance=planka)
ProjectManagerController = ProjectManager(instance=planka)
BackgroundController = Background(instance=planka, name = "sky-change", type="gradient")

print(f"Project:\n\t{ProjectController.build()}")
print(f"Board:\n\t{BoardController.build()}")
print(f"Card:\n\t{CardController.build()}")
print(f"List:\n\t{ListController.build()}")
print(f"Stopwatch:\n\t{StopwatchController.build()}")
print(f"Label:\n\t{LabelController.build()}")
print(f"Task:\n\t{TaskController.build()}")
print(f"CommentAction:\n\t{CommentActionController.build()}")
print(f"Attachment:\n\t{AttachmentController.build()}")
print(f"User:\n\t{UserController.build()}")
print(f"CardMembership:\n\t{CardMembershipController.build()}")
print(f"BoardMembership:\n\t{BoardMembershipController.build()}")
print(f"CardLabel:\n\t{CardLabelController.build()}")
print(f"ProjectManager:\n\t{ProjectManagerController.build()}")
print(f"Background:\n\t{BackgroundController.build()}")