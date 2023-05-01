from plankapy import Planka
from plankapy import build_card
from plankapy import OFFSET


API_URL = None
API_USER = None
API_PASS = None

default_tasks = \
        [
        "LLD",
        "LLD Invoiced",
        "CD",
        "CD Invoiced",
        "PD",
        "PD Invoiced",
        "Constructed"
        ]

prj = input("Project: ")
brd = input("Board: ")
lst = input("List: ")
mkt = input("Market: ")
state = input("State: ")
phase = input("Phase: ")
fdas = input("FDAs (comma seperated or - for range): ")
stage = input("Stage (HLD | LLD | PD | CD) enter to match board: ")
labels = input("Labels (comma seperated) enter to match board: ")
print("Default Tasks: HLD, HLD Invoiced, LLD, LLD Invoiced, CD, CD Invoiced, PD, PD Invoiced, Constructed")
tasks = input("Tasks (comma seperated) enter for default: ")
print(f"cards will be created in\n\t{prj} \n\t   |-> {brd} \n\t      |-> {lst}")

if tasks == "":
    tasks = default_tasks
else:
    tasks = tasks.split(",")

if fdas.__contains__("-"):
    fdas = fdas.split("-")
    fdas = list(range(int(fdas[0]), int(fdas[1])+1))
else:
    fdas = fdas.split(",")

if labels == "":
    labels = [brd]
else:
    labels = labels.split(",")

if stage == "":
    stage = brd

desc = f"|Billable Footage | Stage | City |\n| -------- | -------- | -------- |\n| NA| {stage}     | {mkt}, {state}    |"

instance = Planka(API_URL, API_USER, API_PASS)
next_pos = OFFSET
for fda in fdas:
    build_card(instance, project=prj, board=brd, list=lst, name=f"{mkt} {phase}.{fda}", description=desc, tasks=tasks, labels=labels, position=next_pos)
    next_pos += OFFSET