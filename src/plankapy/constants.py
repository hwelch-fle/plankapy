from dataclasses import dataclass
from typing import Literal

# From https://github.com/plankanban/planka/blob/master/server/api/models/Action.js
ActionType = Literal[
    'createCard',
    'moveCard',
    'commentCard',
]

# From https://github.com/plankanban/planka/blob/master/server/api/models/BoardMembership.js
BoardRole = Literal[
    'editor',
    'viewer',
]

# From https://github.com/plankanban/planka/blob/master/server/api/models/Project.js
Gradient = Literal[
'old-lime',
  'ocean-dive',
  'tzepesch-style',
  'jungle-mesh',
  'strawberry-dust',
  'purple-rose',
  'sun-scream',
  'warm-rust',
  'sky-change',
  'green-eyes',
  'blue-xchange',
  'blood-orange',
  'sour-peel',
  'green-ninja',
  'algae-green',
  'coral-reef',
  'steel-grey',
  'heat-waves',
  'velvet-lounge',
  'purple-rain',
  'blue-steel',
  'blueish-curve',
  'prism-light',
  'green-mist',
  'red-curtain',
]

@dataclass
class Background:
    name: Gradient
    type: str = 'gradient'

@dataclass
class BackgroundImage:
    url: str
    coverUrl: str

# From https://github.com/plankanban/planka/blob/master/server/api/models/Label.js
LabelColor = Literal[
  'berry-red',
  'pumpkin-orange',
  'lagoon-blue',
  'pink-tulip',
  'light-mud',
  'orange-peel',
  'bright-moss',
  'antique-blue',
  'dark-granite',
  'lagune-blue',
  'sunny-grass',
  'morning-sky',
  'light-orange',
  'midnight-blue',
  'tank-green',
  'gun-metal',
  'wet-moss',
  'red-burgundy',
  'light-concrete',
  'apricot-red',
  'desert-sand',
  'navy-blue',
  'egg-yellow',
  'coral-green',
  'light-cocoa',
]

ListSorts = {
    'Name': 'name_asc',
    'Due date': 'dueDate_asc',
    'Oldest First': 'createdAt_asc',
    'Newest First': 'createdAt_desc',
}

ListColors = Literal[
  'berry-red',
  'pumpkin-orange',
  'lagoon-blue',
  'pink-tulip',
  'light-mud',
  'orange-peel',
  'bright-moss',
  'antique-blue',
  'dark-granite',
  'turquoise-sea',
]

SortOption = Literal[
    'Name',
    'Due date',
    'Oldest First',
    'Newest First',
]

LabelColorHexMap = {
    'berry-red':'#e04556',
    'pumpkin-orange':'#f0982d',
    'lagoon-blue':'#109dc0',
    'pink-tulip':'#f97394',
    'light-mud':'#c7a57b',
    'orange-peel':'#fab623',
    'bright-moss':'#a5c261',
    'antique-blue':'#6c99bb',
    'dark-granite':'#8b8680',
    'lagune-blue':'#00b4b1',
    'sunny-grass':'#bfca02',
    'morning-sky':'#52bad5',
    'light-orange':'#ffc66d',
    'midnight-blue':'#004d73',
    'tank-green':'#8aa177',
    'gun-metal':'#355263',
    'wet-moss':'#4a8753',
    'red-burgundy':'#ad5f7d',
    'light-concrete':'#afb0a4',
    'apricot-red':'#fc736d',
    'desert-sand':'#edcb76',
    'navy-blue':'#166a8f',
    'egg-yellow':'#f7d036',
    'coral-green':'#2b6a6c',
    'light-cocoa':'#87564a',
}

GradientCSSMap = {
    'ocean-dive':'linear-gradient(to top, #062e53, #1ad0e0)',
    'old-lime':'linear-gradient(to bottom, #7b920a, #add100)',
    'tzepesch-style':'linear-gradient(to bottom, #190a05, #870000)',
    'jungle-mesh':'linear-gradient(to bottom, #727a17, #414d0b)',
    'blue-danube':'radial-gradient(circle, rgba(9, 9, 121, 1) 0%, rgba(2, 0, 36, 1) 0%, rgba(2, 29, 66, 1) 0%, rgba(2, 41, 78, 1) 0%, rgba(2, 57, 95, 1) 0%, rgba(1, 105, 144, 1) 100%, rgba(1, 151, 192, 1) 100%, rgba(0, 212, 255, 1) 100%)',
    'sundown-stripe':'linear-gradient(22deg, rgba(31, 30, 30, 1) 0%, rgba(255, 128, 0, 1) 10%, rgba(255, 128, 0, 1) 41%, rgba(0, 0, 0, 1) 41%, rgba(0, 102, 204, 1) 89%)',
    'magical-dawn':'radial-gradient(circle, rgba(0, 107, 141, 1) 0%, rgba(0, 69, 91, 1) 90%)',
    'strawberry-dust':'linear-gradient(180deg, rgba(172, 79, 115, 1) 0%, rgba(254, 158, 150, 1) 66%)',
    'purple-rose':'linear-gradient(128deg, rgba(116, 43, 62, 1) 19%, rgba(192, 71, 103, 1) 90%)',
    'sun-scream':'linear-gradient(112deg, rgba(251, 221, 19, 1) 19%, rgba(255, 153, 1, 1) 62%)',
    'warm-rust':'linear-gradient(141deg, rgba(255, 90, 8, 1) 0%, rgba(88, 0, 0, 1) 96%)',
    'sky-change':'linear-gradient(135deg, rgba(0, 52, 89, 1) 0%, rgba(0, 168, 232, 1) 90%)',
    'green-eyes':'linear-gradient(138deg, rgba(19, 170, 82, 1) 0%, rgba(0, 102, 43, 1) 90%)',
    'blue-xchange':'radial-gradient(circle, #294f83, #162c4a)',
    'blood-orange':'linear-gradient(360deg, #d64759 10%, #da7352 360%)',
    'sour-peel':'linear-gradient(360deg, #fd6f46 10%, #fb9832 360%)',
    'green-ninja':'linear-gradient(360deg, #224e4d 10%, #083023 360%)',
    'ice-blue':'linear-gradient(360deg, #38aecc 10%, #347fb9 360%)',
    'epic-green':'linear-gradient(360deg, #01a99c 10%, #0698b1 360%)',
    'algae-green':'radial-gradient(circle farthest-corner at 10% 20%, rgba(0, 95, 104, 1) 0%, rgba(15, 156, 168, 1) 90%)',
    'coral-reef':'linear-gradient(110.3deg, rgba(238, 179, 123, 1) 8.7%, rgba(216, 103, 77, 1) 47.5%, rgba(114, 43, 54, 1) 89.1%)',
    'steel-grey':'radial-gradient(circle farthest-corner at -4% -12.9%, rgba(74, 98, 110, 1) 0.3%, rgba(30, 33, 48, 1) 90.2%)',
    'heat-waves':'linear-gradient(to right, #12c2e9, #c471ed, #f64f59)',
    'wow-blue':'linear-gradient(111.8deg, rgba(0, 104, 155, 1) 19.8%, rgba(0, 173, 239, 1) 92.1%)',
    'velvet-lounge':'radial-gradient(circle farthest-corner at 10% 20%, rgba(151, 10, 130, 1) 0%, rgba(33, 33, 33, 1) 100.2%)',
    'lagoon':'radial-gradient(circle farthest-corner at 10% 20%, rgba(0, 107, 141, 1) 0%, rgba(0, 69, 91, 1) 90%)',
    'purple-rain':'linear-gradient(91.7deg, rgba(50, 25, 79, 1) -4.3%, rgba(122, 101, 149, 1) 101.8%)',
    'blue-steel':'linear-gradient(to top, #09203f 0%, #537895 100%)',
    'blueish-curve':'linear-gradient(171.8deg, rgba(5, 111, 146, 1) 13.5%, rgba(6, 57, 84, 1) 78.6%)',
    'prism-light':'linear-gradient(111.7deg, rgba(251, 198, 6, 1) 2.4%, rgba(224, 82, 95, 1) 28.3%, rgba(194, 78, 154, 1) 46.2%, rgba(32, 173, 190, 1) 79.4%, rgba(22, 158, 95, 1) 100.2%)',
    'the-bow':'radial-gradient(circle farthest-corner at -8.9% 51.2%, rgba(255, 124, 0, 1) 0%, rgba(255, 124, 0, 1) 15.9%, rgba(255, 163, 77, 1) 15.9%, rgba(255, 163, 77, 1) 24.4%, rgba(19, 30, 37, 1) 24.5%, rgba(19, 30, 37, 1) 66%)',
    'green-mist':'linear-gradient(180.5deg, rgba(0, 128, 128, 1) 8.5%, rgba(174, 206, 100, 1) 118.2%)',
    'red-curtain':'radial-gradient(circle 371px at 2.9% 14.3%, rgba(255, 0, 102, 1) 0%, rgba(80, 5, 35, 1) 100.7%)'
}
