import requests
import json
import time

API_URL = "http://localhost:3000"
API_USER = "demo@demo.demo"
API_PASS = "demo"
OFFSET = 65535

class Planka:
    """API wrapper class for Planka
    @url: URL of Planka instance
    @username: Username of Planka user
    @password: Password of Planka user
    """
    def __init__(self, url:str, username:str, password:str, api_end="/api", routes="config/planka_routes.json", templates="config/planka_templates.json"):
        self.url = url
        self.username = username
        self.password = password
        self.api_end = api_end
        self.auth = None
        with open(routes) as f:
            self.routes = json.load(f)
        with open(templates) as f:
            self.templates = json.load(f)
        self.authenticate()

    def deauthenticate(self) -> bool:
        """Deletes the auth token from the Planka API
        @return: True if successful, False if not
        """
        try:
            self.request("DELETE", self.get_route("access-token", "DELETE", "active"))
            self.auth = None
            return True
        except:
            return False

    def validate(self) -> bool:
        """Validates the Planka API connection
        @return: True if successful, False if not
        """
        try:
            self.request("GET", "/*")
            return True
        except:
            return False

    def authenticate(self) -> bool:
        """Gets an auth token from the Planka API
        @return: True if successful, False if not
        """
        try:
            request = requests.post(f"{self.url}{self.get_route('access-token', 'POST', 'active')}", data={'emailOrUsername': self.username, 'password': self.password})
            self.auth = request.json()['item']
            if self.auth == None:
                raise Exception("Invalid API credentials")
            return True
        except:
            raise Exception("Invalid API credentials")

    def request(self, method:str, endpoint:str, data:dict=None) -> dict:
        """Makes a request to the Planka API
        @method: HTTP method
        @endpoint: API endpoint
        @data: Data to send with request (default: None)
        @return: JSON response from Planka API
        """
        if self.auth == None:
            self.authenticate()
        headers = \
            { 
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth}"
            }
        url = f"{self.url}{endpoint}"
        response = requests.request(method, url, headers=headers, json=data)

        if response.status_code == 401:
            raise Exception("Invalid API credentials")

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to {method} {url} with status code {response.status_code}")

        try:
            return response.json()
        except:
            raise Exception(f"Failed to parse response from {url}")
    
    def get_route(self, controller:str, method:str, action:str) -> str:
        """Returns a route from the planka_routes.json file
        @controller: Name of controller
        @method: HTTP method
        @action: Name of request action
        @return: Route string
        """
        try:
            return self.routes[controller][method][action]
        except:
            raise Exception(f"Route not found: {controller} {method} {action}")
    
    def get_template(self, template:str) -> dict:
        """Returns a template from the templates.json file
        @template: Name of template to return
        @return: Template dictionary
        """
        try:
            return self.templates[template]
        except:
            raise Exception(f"Template not found: {template}")
        
class Controller():
    def __init__(self, instance:Planka) -> None:
        """Controller class for Planka API
        @instance: Planka API instance
        """
        self.instance = instance
        self.template:dict = None
        self.data:dict = None
        self.response:dict = None

    def __str__(self) -> str:
        """Returns a string representation of the controller object
        @return: String representation of controller object
        """
        return f"{type(self).__name__}:\n{json.dumps(self.data, sort_keys=True, indent=4)}"

    def __repr__(self) -> str:
        """Returns a string representation of the controller object
        @return: String representation of controller object
        """
        return f"<{type(self).__name__}({self.__class__.__bases__[0].__name__})>{self.__str__()}"

    def build(self, **kwargs) -> dict:
        """Builds the controller data
        @return: Controller data dictionary
        """
        if kwargs == {}:
            return kwargs
        data = {}
        valid_keys = self.template.keys()
        for key, value in kwargs.items():
            if key in valid_keys:
                data[key] = value
        self.data = data
        return self.data

    def create(self, route:str, data:dict=None) -> dict:
        """Creates a new controller object (POST)
        @route: Route for controller object POST request
        @return: POST response dictionary
        """
        if not data:
            data = self.data
        if not data:
            raise Exception(f"Please Build a {type(self).__name__} before creating")
        self.response = self.instance.request("POST", route, data)
        return self.response

    def get(self, route:str) -> dict:
        """Gets a controller object (GET)
        @route: Route for controller object GET request
        @return: GET response dictionary
        """
        return self.instance.request("GET", route)

    def update(self, route:str, data:dict=None) -> dict:
        """Updates a controller object (PATCH)
        @route: Route for controller object PATCH request
        @oid: ID of controller object
        @return: PATCH response dictionary
        """
        if not data:
            data = self.data
        if not self.data:
            raise Exception(f"Please Build a {type(self).__name__} before updating")
        self.response = self.instance.request("PATCH", route, data=data)
        return self.response

    def delete(self, route:str) -> dict:
        """Deletes a controller object (DELETE)
        @route: Route for controller object DELETE request
        @oid: ID of controller object
        @return: DELETE response dictionary
        """
        return self.instance.request("DELETE", route)
    
    def last_response(self) -> dict:
        """Returns the last response from the controller object
        @return: Last response dictionary
        """
        return self.response

class Project(Controller):
    def __init__(self, instance:Planka, **kwargs) -> None:
        self.instance = instance
        self.template = instance.get_template("project")
        self.data = self.build(**kwargs)

    def get(self, name:str=None, oid:str=None) -> dict:
        """Gets a project by name
        @oid: ID of project to get (optional)
        @name: Name of project if None returns all projects
        @return: GET response dictionary
        """
        if oid:
            return super().get(f"/api/projects/{oid}")
        prjs = super().get(f"/api/projects")
        if not name:
            return prjs
        prj_names = [prj["name"] for prj in prjs["items"]]
        if name not in prj_names:
            raise Exception(f"Project {name} not found")
        prj_id = [prj for prj in prjs["items"] if prj["name"] == name][0]["id"]
        return super().get(f"/api/projects/{prj_id}")

    def get_project_names(self) -> list:
        """Gets a list of project names
        @return: List of project names
        """
        return [prj["name"] for prj in self.get()['items']]
    
    def create(self) -> dict:
        """Creates a new project
        @return: POST response dictionary
        """
        if not self.data:
            raise Exception(f"Please Build a {type(self).__name__} before creating")
        if self.data["name"] in [prj["name"] for prj in self.get()['items']]:
            raise Exception(f"Project {self.data['name']} already exists")
        return super().create("/api/projects")
    
    def update(self, name:str) -> dict:
        """Updates a project
        @name: Name of project to update
        @return: PATCH response dictionary
        """
        prj_id = prj_id = self.get(name)['item']['id']
        return super().update(f"/api/projects/{prj_id}")

    def delete(self, name:str) -> dict:
        """Deletes a project
        @name: Name of project to delete
        @return: DELETE response dictionary
        """
        prj_id = self.get(name)['item']['id']
        return super().delete(f"/api/projects/{prj_id}")

class Board(Controller):
    def __init__(self, instance:Planka, **kwargs) -> None:
        self.instance = instance
        self.template = instance.get_template("board")
        self.data = self.build(**kwargs)
    
    def get(self, project_name:str=None, board_name:str=None, oid:str=None) -> dict:
        """Gets a board by name
        @oid: ID of board to get (optonal)
        @name: Name of board if None returns all boards
        @project_name: Name of project to get boards from
        @return: GET response dictionary
        """
        if oid:
            return super().get(f"/api/boards/{oid}")
        if not (project_name):
            raise Exception("Please provide a project name")
        prj_con = Project(self.instance)
        prj = prj_con.get(project_name)
        boards = prj["included"]["boards"]
        if not board_name:
            return boards
        board_names = [board["name"] for board in boards]
        if board_name not in board_names:
            raise Exception(f"Board `{board_name}` not found")
        board_id = [board for board in boards if board["name"] == board_name][0]["id"]
        return super().get(f"/api/boards/{board_id}")
    
    def create(self, project_name:str) -> dict:
        """Creates a new board
        @prj_name: Name of project to create board in
        @return: POST response dictionary
        """
        if self.data == None:
            raise Exception(f"Please Build a {type(self).__name__} before creating")
        prj_con = Project(self.instance)
        prj_id = prj_con.get(project_name)['item']['id']
        return super().create(f"/api/projects/{prj_id}/boards")
    
    def update(self, project_name:str=None, board_name:str=None, data:dict=None, oid:str=None) -> dict:
        """Updates a board
        @oid: ID of board to update (optional)
        @project_name: Name of project to update board in
        @board_name: Name of board to update
        @return: PATCH response dictionary
        """
        if not data:
            data = self.data
        if not data:
            raise Exception(f"Please Build a {type(self).__name__} before updating")
        if oid:
            return super().update(f"/api/boards/{oid}", data=data)
        if not (project_name and board_name):
            raise Exception("Please provide project and board names")
        board_id = self.get(project_name, board_name)['item']['id']
        return super().update(f"/api/boards/{board_id}", data=self.data)
    
    def delete(self, project_name:str=None, board_name:str=None, oid:str=None):
        """Deletes a board
        @oid: ID of board to delete (optional)
        @project_name: Name of project to delete board in
        @board_name: Name of board to delete
        @return: DELETE response dictionary
        """
        if oid:
            return super().delete(f"/api/boards/{oid}")
        if project_name == None:
            raise Exception("Please provide a project name")
        if board_name == None:
            raise Exception("Please provide a board name")
        board_id = self.get(project_name, board_name)['item']['id']
        return super().delete(f"/api/boards/{board_id}")

class List(Controller):
    def __init__(self, instance:Planka, **kwargs) -> None:
        self.instance = instance
        self.template = instance.get_template("list")
        self.data = self.build(**kwargs)

    def get(self, project_name:str=None, board_name:str=None, list_name:str=None):
        """Gets a list by name
        NOTE: No GET route for list by ID
        @project_name: Name of project to get list from
        @board_name: Name of board to get list from
        @list_name: Name of list to get
        @return: GET response dictionary
        """
        if not (project_name and board_name):
            raise Exception("Please provide project and board names")
        board_con = Board(self.instance)
        board = board_con.get(project_name, board_name)
        lists = board["included"]["lists"]
        list_names = [lst["name"] for lst in lists]
        if list_name == None:
            return lists
        if list_name not in list_names:
            raise Exception(f"List `{list_name}` not found")
        return [lst for lst in lists if lst["name"] == list_name][0]
    
    def create(self, project_name:str=None, board_name:str=None, data:dict=None):
        """Creates a new list
        @project_name: Name of project to create list in
        @board_name: Name of board to create list in
        @return: POST response dictionary
        """
        if not data:
            data = self.data
        if not data:
            raise Exception(f"Please Build a {type(self).__name__} before creating")
        if not (project_name and board_name):
            raise Exception("Please provide project and board name")
        board_con = Board(self.instance)
        board_id = board_con.get(project_name, board_name)['item']['id']
        return super().create(f"/api/boards/{board_id}/lists")
    
    def update(self, project_name:str=None, board_name:str=None, list_name:str=None, data:dict=None, oid:str=None):
        """Updates a list
        @oid: ID of list to update (optional)
        @project_name: Name of project to update list in
        @board_name: Name of board to update list in
        @list_name: Name of list to update
        @return: PATCH response dictionary
        """        
        if not data:
            data = self.data
        if not data:
            raise Exception(f"Please Build a {type(self).__name__} before updating")
        if oid:
            return super().update(f"/api/lists/{oid}", data=data)
        if not (project_name and board_name and list_name):
            raise Exception("Please provide project, board, and list names")
        lst = self.get(project_name, board_name, list_name)
        return super().update(f"/api/lists/{lst['id']}", data=data)
    
    def delete(self, project_name:str=None, board_name:str=None, list_name:str=None, oid:str=None):
        """Deletes a list
        @oid: ID of list to delete (optional)
        @project_name: Name of project to delete list in
        @board_name: Name of board to delete list in
        @list_name: Name of list to delete
        @return: DELETE response dictionary
        """
        if oid != None:
            return super().delete(f"/api/lists/{oid}")
        if not (project_name and board_name and list_name):
            raise Exception("Please provide a project, board, and list names")
        lst = self.get(project_name, board_name, list_name)
        return super().delete(f"/api/lists/{lst['id']}")

class Card(Controller):
    def __init__(self, instance:Planka, **kwargs) -> None:
        self.instance = instance
        self.template = instance.get_template("card")
        self.data = self.build(**kwargs)

    def get(self, project_name:str=None, board_name:str=None, list_name:str=None, card_name:str=None, oid:str=None):
        """Gets a card by name
        @oid: ID of card to get (optional)
        @project_name: Name of project to get card from
        @board_name: Name of board to get card from
        @list_name: Name of list to get card from
        @card_name: Name of card to get
        @return: GET response dictionary
        """
        if oid != None:
            return super().get(f"/api/cards/{oid}")
        if not (project_name and board_name and list_name):
            raise Exception("Please provide project, board, and list names")
        board_con = Board(self.instance)
        board = board_con.get(project_name, board_name)
        lst_id = [ls for ls in board["included"]["lists"] if ls["name"] == list_name][0]["id"]
        cards = [card for card in board["included"]["cards"] if card["listId"] == lst_id]
        card_names = [card["name"] for card in cards]
        if card_name == None:
            return [self.get(oid=card["id"]) for card in cards]
        if card_name not in card_names:
            raise Exception(f"Card `{card_name}` not found")
        card_id = [card for card in cards if card["name"] == card_name][0]['id']
        return super().get(f"/api/cards/{card_id}")
    
    def create(self, project_name:str=None, board_name:str=None, list_name:str=None, data:dict=None):
        """Creates a new card
        @project_name: Name of project to create card in
        @board_name: Name of board to create card in
        @list_name: Name of list to create card in
        @return: POST response dictionary
        """
        if data == None:
            data = self.data
        if data == None:
            raise Exception(f"Please Build a {type(self).__name__} before creating")
        if not (project_name and board_name and list_name):
            raise Exception("Please provide a project, board and list names")
        board_con = Board(self.instance)
        board = board_con.get(project_name, board_name)
        lst_id = [ls for ls in board["included"]["lists"] if ls["name"] == list_name][0]["id"]
        return super().create(f"/api/lists/{lst_id}/cards")

    def delete(self, project_name:str=None, board_name:str=None, list_name:str=None, card_name:str=None, oid:str=None):
        """Deletes a card
        @oid: ID of card to delete (optional)
        @project_name: Name of project to delete card in
        @board_name: Name of board to delete card in
        @list_name: Name of list to delete card in
        @card_name: Name of card to delete
        @return: DELETE response dictionary
        """
        if oid != None:
            return super().delete(f"/api/cards/{oid}")
        if not (project_name and board_name and list_name and card_name):
            raise Exception("Please provide a project, board, list, and card name")
        card = self.get(project_name, board_name, list_name, card_name)
        return super().delete(f"/api/cards/{card['id']}")
    
    def update(self, project_name:str=None, board_name:str=None, list_name:str=None, card_name:str=None, data:dict=None, oid:str=None):
        """Updates a card
        @oid: ID of card to update (optional)
        @project_name: Name of project to update card in
        @board_name: Name of board to update card in
        @list_name: Name of list to update card in
        @card_name: Name of card to update
        @return: PATCH response dictionary
        """
        if not data:
            data = self.data
        if not data:
            raise Exception(f"Please Build a {type(self).__name__} before updating")
        if oid:
            return super().update(f"/api/cards/{oid}", data=data)
        if not (project_name and board_name and list_name and card_name):
            raise Exception("Please provide a project, board, list, and card name")
        card = self.get(project_name, board_name, list_name, card_name)
        return super().update(f"/api/cards/{card['id']}", data=data)
    
    def get_labels(self, project_name:str=None, board_name:str=None, list_name:str=None, card_name:str=None, oid:str=None):
        """Gets labels for a card
        @oid: ID of card to get labels from (optional)
        @project_name: Name of project to get card from
        @board_name: Name of board to get card from
        @list_name: Name of list to get card from
        @card_name: Name of card to get
        @return: GET response dictionary
        """
        if oid:
            return self.get(oid=oid)['included']['cardLabels']
        if not (project_name and board_name and list_name and card_name):
            raise Exception("Please provide project, board, list, and card names")
        card_id = self.get(project_name, board_name, list_name, card_name)['item']['id']
        return self.get(oid=card_id)['included']['cardLabels']
    
class Label(Controller):
    def __init__(self, instance:Planka, **kwargs) -> None:
        self.instance = instance
        self.template = instance.get_template("label")
        self.options = instance.get_template("colors")
        self.data = self.build(**kwargs)

    def colors(self) -> list:
        return self.options
    
    def get(self, project_name:str=None, board_name:str=None, label_name:str=None) -> dict:
        """Gets a label by name
        @project_name: Name of project to get label from
        @board_name: Name of board to get label from
        @label_name: Name of label to get
        @return: GET response dictionary
        """
        if not (project_name and board_name):
            raise Exception("Please provide project and board names")
        board_con = Board(self.instance)
        board = board_con.get(project_name, board_name)
        labels = board["included"]["labels"]
        label_names = [label["name"] for label in labels]
        if not label_name:
            return labels
        if label_name not in label_names:
            raise Exception(f"Label `{label_name}` not found")
        return [label for label in labels if label["name"] == label_name][0]
    
    def create(self, project_name:str=None, board_name:str=None, data:dict=None):
        """Creates a new label
        @project_name: Name of project to create label in
        @board_name: Name of board to create label in
        @return: POST response dictionary
        """
        if not data:
            data = self.data
        if not data:
            raise Exception(f"Please Build a {type(self).__name__} before creating")
        if not (project_name and board_name):
            raise Exception("Please provide project and board names")
        board_con = Board(self.instance)
        board = board_con.get(project_name, board_name)['item']
        return super().create(f"/api/boards/{board['id']}/labels")
    
    def delete(self, project_name:str=None, board_name:str=None, label_name:str=None, oid:str=None):
        """Deletes a label
        @oid: ID of label to delete (optional)
        @project_name: Name of project to delete label from
        @board_name: Name of board to delete label from
        @label_name: Name of label to delete
        @return: DELETE response dictionary
        """
        if oid:
            return super().delete(f"/api/labels/{oid}")
        if not (project_name and board_name and label_name):
            raise Exception("Please provide project, board, and label names")
        label = self.get(project_name, board_name, label_name)
        return super().delete(f"/api/labels/{label['id']}")
    
    def add(self, project_name:str=None, board_name:str=None, list_name:str=None ,card_name:str=None, label_name:str=None, card_id:str=None, label_id:str=None):
        """Adds a label to a card
        @project_name: Name of project to add label to card in
        @board_name: Name of board to add label to card in
        @label_name: Name of label to add to card
        @card_name: Name of card to add label to
        @list_name: Name of list to add label to card in
        @return: POST response dictionary
        """
        if label_id and card_id:
            return super().create(f"/api/cards/{card_id}/labels", data={"labelId":label_id})
        if not (project_name and board_name and label_name):
            raise Exception("Please provide a project, board, label name")
        if card_id and label_name:
            label = self.get(project_name, board_name, label_name)
            return super().create(f"/api/cards/{card_id}/labels", data={"labelId":label['item']['id']})
        if not (card_name and list_name):
            raise Exception("Please provide a card and list name")
        card_con = Card(self.instance)
        card = card_con.get(project_name, board_name, list_name, card_name)
        label = self.get(project_name, board_name, label_name)
        return super().create(f"/api/cards/{card['item']['id']}/labels", {"labelId":label['item']['id']})

    def remove(self, project_name:str=None, board_name:str=None, list_name:str=None ,card_name:str=None, label_name:str=None, card_id:str=None, label_id:str=None):
        """Removes a label from a card
        @project_name: Name of project to remove label from card in
        @board_name: Name of board to remove label from card in
        @label_name: Name of label to remove from card
        @card_name: Name of card to remove label from
        @list_name: Name of list to remove label from card in
        @return: DELETE response dictionary
        """
        if label_id and card_id:
            return super().delete(f"/api/cards/{card_id}/labels/{label_id}")
        if not (project_name and board_name and label_name):
            raise Exception("Please provide a project, board, label name")
        if card_id and label_name:
            label_id = [label['id'] for label in Card(self.instance).get_labels(oid=card_id) if label['name'] == label_name][0]
            return super().delete(f"/api/cards/{card_id}/labels/{label['item']['id']}")
        if not (card_name and list_name):
            raise Exception("Please provide a card and list name")
        card_con = Card(self.instance)
        card = card_con.get(project_name, board_name, list_name, card_name)
        label = self.get(project_name, board_name, label_name)
        return super().delete(f"/api/cards/{card['item']['id']}/labels/{label['item']['id']}")

class Task(Controller):
    def __init__(self, instance:Planka, **kwargs) -> None:
        self.instance = instance
        self.template = instance.get_template("task")
        self.data = self.build(**kwargs)
    
    def get(self, project_name:str=None, board_name:str=None, list_name:str=None, card_name:str=None, task_name:str=None) -> dict:
        """Gets a task by name
        NOTE: No GET route for tasks by OID
        @project_name: Name of project to get task from
        @board_name: Name of board to get task from
        @list_name: Name of list to get task from
        @card_name: Name of card to get task from
        @task_name: Name of task to get
        @return: GET response dictionary
        """
        if not (project_name and board_name and list_name and card_name):
            raise Exception("Please provide project, board, list, and card names")
        board_con = Board(self.instance)
        board = board_con.get(project_name, board_name)
        list_id = [ls for ls in board["included"]["lists"] if ls["name"] == list_name][0]["id"]
        cards = [card for card in board["included"]["cards"] if card["name"] == card_name and card["listId"] == list_id]
        card_id = [card for card in cards if card["name"] == card_name][0]["id"]
        tasks = [task for task in board["included"]["tasks"] if task["cardId"] == card_id]
        task_names = [task["name"] for task in tasks]
        if task_name == None:
            return tasks
        if task_name not in task_names:
            raise Exception(f"Task `{task_name}` not found")
        return [task for task in tasks if task["name"] == task_name][0]
    
    def create(self, project_name:str=None, board_name:str=None, list_name:str=None, card_name:str=None, data:dict=None, card_id:str=None):
        """Creates a new task
        @card_id: ID of card to create task in (optional)
        @project_name: Name of project to create task in
        @board_name: Name of board to create task in
        @list_name: Name of list to create task in
        @card_name: Name of card to create task in
        @return: POST response dictionary
        """
        if not data:
            data = self.data
        if not data:
            raise Exception(f"Please Build a {type(self).__name__} before creating")
        if card_id:
            return super().create(f"/api/cards/{card_id}/tasks")
        if not (project_name and board_name and list_name and card_name):
            raise Exception("Please provide project, board, list, and card names")
        board_con = Board(self.instance)
        board = board_con.get(project_name, board_name)
        list_id = [ls for ls in board["included"]["lists"] if ls["name"] == list_name][0]["id"]
        cards = [card for card in board["included"]["cards"] if card["name"] == card_name and card["listId"] == list_id]
        card_id = [card for card in cards if card["name"] == card_name][0]["id"]
        return super().create(f"/api/cards/{card_id}/tasks")
    
    def update(self, project_name:str=None, board_name:str=None, list_name:str=None, card_name:str=None, task_name:str=None, data:dict=None, oid:str=None):
        """Updates a task
        @oid: Object ID of task to update (optional)
        @project_name: Name of project to update task in
        @board_name: Name of board to update task in
        @list_name: Name of list to update task in
        @card_name: Name of card to update task in
        @task_name: Name of task to update
        @return: PATCH response dictionary
        """
        if not data:
            data = self.data
        if not data:
            raise Exception(f"Please Build a {type(self).__name__} before updating")
        if oid:
            return super().update(f"/api/tasks/{oid}")
        if not (project_name and board_name and list_name and card_name and task_name):
            raise Exception("Please provide project, board, list, card, and task names")
        task = self.get(project_name, board_name, list_name, card_name, task_name)
        return super().update(f"/api/tasks/{task['id']}")
       
    def delete(self, project_name:str=None, board_name:str=None, list_name:str=None, card_name:str=None, task_name:str=None, oid:str=None):
        """Deletes a task
        @oid: ID of task to delete (Use this if you already have the ID)
        @project_name: Name of project to delete task from
        @board_name: Name of board to delete task from
        @list_name: Name of list to delete task from
        @card_name: Name of card to delete task from
        @task_name: Name of task to delete
        @return: DELETE response dictionary
        """
        if oid:
            return super().delete(f"/api/tasks/{id}")
        if not (project_name and board_name and list_name and card_name and task_name):
            raise Exception("Please provide project, board, list, card, and task names")
        task = self.get(project_name, board_name, list_name, card_name, task_name)
        return super().delete(f"/api/tasks/{task['id']}")

class Attachment(Controller):
    def __init__(self, instance:Planka, **kwargs) -> None:
        self.instance = instance
        self.template = instance.get_template("attachment")
        self.data = self.build(**kwargs)

class Stopwatch(Controller):
    def __init__(self, instance:Planka, **kwargs) -> None:
        self.instance = instance
        self.template = instance.get_template("stopwatch")
        self.data = self.build(**kwargs)

class Background(Controller):
    def __init__(self, instance:Planka, **kwargs) -> None:
        self.instance = instance
        self.template = instance.get_template("background")
        self.options = instance.get_template("gradients")
        self.data = self.build(**kwargs)

    def gradients(self) -> dict:
        """Gets all gradients
        @return: GET response dictionary
        """
        return self.options

    def apply(self, prj_name:str):
        """Applies a gradient to a project
        @project: Name of project to apply gradient to
        @return: PATCH response dictionary
        """
        project = Project(self.instance)
        prj_id = project.get(prj_name)["item"]["id"]
        if "type" not in self.data.keys():
            raise Exception("Please specify a background type: `gradient` | `image`")
        if self.data["type"] == "gradient" and self.data["name"] not in self.options:
            raise Exception(f"Gradient {self.data['name']} not found: please choose from\n{self.options}")
        return super().update(f"/api/projects/{prj_id}", data={"background": self.data})
    
    def clear(self, prj_name:str):
        """Clears a gradient from a project
        @project: Name of project to clear gradient from
        @return: PATCH response dictionary
        """
        project = Project(self.instance)
        prj_id = project.get(prj_name)["item"]["id"]
        return super().update(f"/api/projects/{prj_id}", data={"background": None})

class Comment(Controller):
    def __init__(self, instance:Planka, **kwargs) -> None:
        self.instance = instance
        self.template = instance.get_template("comment-action")
        self.data = self.build(**kwargs)

class User(Controller):
    def __init__(self, instance:Planka, **kwargs) -> None:
        self.instance = instance
        self.template = instance.get_template("user")
        self.data = self.build(**kwargs)

def test_planka():
    import random
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
    
    board.build(name="Test Board", type="kanban", position=OFFSET)
    board.create("Plankapy Test Project")
    print("Created Test Board")
    
    next_pos = OFFSET
    new_labels = []
    for color in label.colors():
        label.build(name=f"{color} label", color=color, position=next_pos)
        new_labels.append(label.create("Plankapy Test Project", "Test Board")["item"])
        next_pos += OFFSET
        print(f"Created {color} Label")
    lst.build(name="Test List", position=0)
    lst.create("Plankapy Test Project", "Test Board")
    print("Created Test List")
    
    new_cards=[]
    next_pos = OFFSET
    for i in range(1, 11):
        card.build(name=f"Test Card {i}", description=f"CHANGE ME {i}", position=next_pos)
        next_pos += OFFSET
        new_cards.append(card.create("Plankapy Test Project", "Test Board", "Test List")["item"])
        print(f"Created Test Card {i}")
    
    for cd in new_cards:
        lb = random.choice(new_labels)
        label.add(label_id=lb["id"], card_id=cd["id"])
    print("added random labels to cards")
        
    for i in range(int(len(new_cards)/2)):
        cd = random.choice(new_cards)
        lbs = card.get_labels("Plankapy Test Project", "Test Board", oid=cd["id"])
        for lb in lbs:
            print(lb)
            label.remove(label_id=lb["labelId"], card_id=lb["cardId"])
            print(f"removed label from {cd['name']}")
    print("removed random labels from half the cards")
    
    new_tasks=[]
    for cd in new_cards:
        next_pos=OFFSET
        for i in range(1,5):
            task.build(name=f"Test Task {i}", position=next_pos)
            next_pos += OFFSET
            print(cd)
            new_tasks.append(task.create(card_id=cd["id"])["item"])
        print(f"Created 4 tasks on {cd['name']}")
    
    for tsk in new_tasks:
        print(tsk)
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
    print("Tests complete")
