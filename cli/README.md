# Submodule for Plankapy CLI tools implemented in `click`

## Proposals

### REPL CLI
```bash
$ planka
Welcome to plankapy {version}, type `help` for a list of commands
>>> help
commands:
  - help    : show this message
  - connect : connect to a planka server

>>> connect
Enter the server URL: http://localhost:3000
Enter your username: demo
Enter your password: ****
Connected to http://localhost:3000 as demo

>>> projects
1. Project 1
2. Project 2
3. Project 3

>>> 1
>>> help
project commands:
  - help     : show this message
  - context  : show the current context
  - info     : show project information
  - boards   : show boards
  - users    : show users in this project
  - managers : show managers in this project
  - exit     : exit the current project
  
  ---Modify---
  - add      : add a new [board, manager]
  - remove   : remove a [board, manager]
  - modify   : modify a [board, manager]

>>> context
Current User: demo
Current Project: Project 1

>>> boards
1. Board 1
2. Board 2
3. Board 3

>>> 1
>>> help
board commands:
  - help     : show this message
  - context  : show the current context
  - info     : show board information
  - lists    : show lists in this board
  - users    : show users in this board
  - labels   : show labels in this board
  - exit     : exit the current board

  ---Modify---
  - add      : add a new [label, list, user {editor, viewer}]
  - remove   : remove a [label, list, user]
  - modify   : modify a [label, list, user]

>>> context
Current User: demo
Current Project: Project 1
Current Board: Board 1

>>> add user user1
Multiple users found, please select one:
1. user1 [John Doe]
2. user1 [Jane Doe]
>>> 1
enter the role [editor, viewer]: editor

user 1 [John Doe] added to Board 1 as editor

>>> exit all\
Disconnected from http://localhost:3000

$
```

### UNIX Style CLI
```bash
$ planka connect http://localhost:3000 demo ****
Connected to http://localhost:3000 as demo

$ planka projects
1. Project 1
2. Project 2
3. Project 3

$ planka project 1 boards
1. Board 1
2. Board 2
3. Board 3

$ planka -add-user --board='Board 1' --username='user1' --role='editor'
Multiple users found, please select one:
Username [Full Name]
user1 [John Doe]
user1 [Jane Doe]

$ planka -add-user --board='Board 1' --username='user1' --fullname 'John Doe' --role='editor'

$ planka -exit
Disconnected from http://localhost:3000
```

