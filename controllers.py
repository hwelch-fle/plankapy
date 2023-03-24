from plankapy import Planka
import time

OFFSET = 65535
REFRESH = 10 # Seconds

class Controller(object):
    def __init__(self, instance:Planka, **kwargs:dict):
        self.instance:Planka = instance
        self.kwargs:dict = kwargs
        self.template:dict = None
        self.routes:dict = None
        self.active:dict = None
    
    def get_route(self, method:str, action:str) -> str:
        """Gets the routes for the controller
        @return: Routes
        """
        if self.routes == None:
            raise Exception("Routes not loaded")
        if method not in self.routes:
            raise Exception(f"Invalid method {method} for route {action}")
        return self.routes[method][action]

    def parse_route(self, method:str=None, action:str=None ,id:str=None, parent:object=None, req_id:bool=False) -> str:
        """Generates a route string from parameters
        @method: HTTP method
        @action: HTTP action
        @id(optional): ID to use in route
        @parent: Parent controller
        @req_id: Whether or not the route requires an ID
                    (Parent ID will be used if needed)
        @return: Route string
        """
        route = self.get_route(method, action)
        if route.count(":id:") > 1:
            if parent == None:
                raise Exception(f"Parent required for route '{route}'")
            route = route.replace(":id:", str(parent.active()["id"]), 1)
        if req_id:
            route = route.replace(":id:", str(id), 1)
        return route

    def get_active(self) -> dict:
        """Gets the active object for the controller
        @return: Active object
        """
        if self.active:
            return self.active
    
    def set_active(self, active:dict) -> dict:
        """Sets the active object for the controller
        @active: Active object
        @return: Previous active object
        """
        old = self.active
        self.active = active
        return old
    
    def clear_active(self) -> None:
        """Clears the active object for the controller
        @return: None
        """
        self.active = None
        return self.active
    
    def get_template(self) -> dict:
        """Gets the template for the controller
        @return: Template
        """
        raise NotImplementedError("get_template() not implemented")

    def build(self) -> dict:
        """Builds the object to be sent to the Planka API
        @return: Object to be sent to Planka API
        """
        keys = list(self.template.keys())
        for key in self.kwargs:
            if key in self.template:
                self.template[key] = self.kwargs[key]
                keys.remove(key)
        if len(keys) > 0:
            for key in keys:
                self.template[key] = None
        return self.template
    
    def create(self, **kwargs) -> dict:
        """Creates an object in Planka
        @return: Object created in Planka
        """
        self.active = self.instance.request("POST", self.parse_route(method="POST", **kwargs), data=self.build())
        return self.active
       
    def update(self, data:dict=None, **kwargs) -> dict:
        """Patches an object in Planka
        @data: Data to patch
        @return: Object patched in Planka
        """
        return self.instance.request("PATCH", self.parse_route(method="PATCH", **kwargs), data=data)
    
    def delete(self, **kwargs) -> None:
        """Deletes an object in Planka
        @return: None
        """
        return self.instance.request("DELETE", self.parse_route(method="DELETE", **kwargs))
    
    def get(self, **kwargs) -> dict:
        """Gets an object by ID
        @kwargs: Additional arguments passed to _parse_route()
               : @id: ID of object
               : @route_parent(str): The dictionary key for the route parent in planka_routes.json\n
               : @route_key(str): The dictionary key for the route in planka_routes.json\n
               : @parent(Controller): Parent controller object\n
               : @req_id(bool): Whether or not the route requires an ID\n
        @return: Object
        """
        return self.instance.request("GET", self.parse_route(method="GET", **kwargs))
    
class Project(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["project"]
        self.routes = self.instance.routes["project"]
        self.project_dict = None
        self.last_updated = None
        self.active = {"name": None, "id": None, "content": None}

    def create(self) -> dict:
        if self.kwargs['name'] in self.get_project_names():
            self.active=self.get_project_by_name(self.kwargs['name'])
            print(Exception(f"Project '{self.kwargs['name']}' already exists, setting active project to '{self.kwargs['name']}'"))
            return self.active
        project_item = super().create(action="project")['item']
        self.active['name'] = self.kwargs['name']
        self.active['id'] = project_item['id']
        self.active['content'] = None
        self.get_project_dictionary()
        return self.active

    def delete(self, id:str=None) -> None:
        if id == None:
            id = self.active["id"]
        deleted = super().delete(id=id, action="project", req_id=True)
        self.get_project_dictionary()
        return deleted

    def update(self, id:str=None, data:dict=None) -> dict:
        if id == None:
            id = self.active["id"]
        return super().update(id=id, action="project",data=data, req_id=True)

    def set_active(self, name:str) -> dict:
        active = self.get_project_by_name(name)
        return super().set_active(active)

    def get_project(self, id:str=None) -> dict:
        if id == None:
            id = self.active()["id"]
        return super().get(id=id, action="project", req_id=True)['included']

    def get_projects(self) -> list:
        return super().get(action="projects")
    
    def get_project_names(self):
        if self.project_dict == None:
            self.project_dict = self.get_project_dictionary()
        return list(self.project_dict.keys())
    
    def get_project_dictionary(self) -> dict:
        if self.last_updated == None or time.time() - self.last_updated > REFRESH:
            self.last_updated = time.time()
            self.project_dict = self.get_project_dictionary()
        self.project_dict = {project['name']: {"name": project['name'] ,"id": project['id'], "content":self.get_project(project['id'])} for project in self.get_projects()['items']}
        return self.project_dict

    def get_project_by_name(self, name:str=None) -> dict:
        return self.get_project_dictionary()[name]
    
    def get_project_boards(self, name:str=None) -> list:
        if name == None:
            name = self.active["name"]
        return self.get_project_dictionary()[name]["content"]['boards']
    
    def get_project_users(self, name:str=None) -> list:
        if name == None:
            name = self.active["name"]
        return self.get_project_dictionary()[name]["content"]['users']
    
    def get_project_board_memberships(self, name:str=None) -> list:
        if name == None:
            name = self.active["name"]
        return self.get_project_dictionary()[name]["content"]['boardMemberships']
    
    def get_project_managers(self, name:str=None) -> list:
        if name == None:
            name = self.active["name"]
        return self.get_project_dictionary()[name]["content"]['projectManagers']
    
    def get_project_board_names(self, name:str=None) -> list:
        if name == None:
            name = self.active["name"]
        return [board['name'] for board in self.get_project_boards(name)]
        
class Board(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["board"]
        self.routes = self.instance.routes["board"]
        self.board_dict = None
        self.active = {"name": None, "id": None, "project": None, "content": None}
    
    def set_project(self, project:str) -> dict:
        self.active['project'] = project
        return self.active
    
    def set_active(self, active: dict) -> dict:
        self.active["name"] = active["name"]
        self.active["id"] = active["id"]
        self.active["project"] = active["project"]
        self.active["content"] = active["content"]
        return self.active

    def get_board(self, name:str=None, projectName:str=None, projectController:Project=None) -> dict:
        if name == None and self.active["name"] != None:
            name = self.active["name"]
            if name == None:
                raise Exception("No board provided")
        if projectController == None:
            projectController = Project(instance=self.instance)
        if projectName == None and projectController.active["name"] != None:
            projectName = projectController.active["name"]
            if projectName == None:
                raise Exception("No project provided")
        valid_names = projectController.get_project_board_names(projectName)
        if name not in valid_names:
            raise Exception(f"Board '{name}' not found in project '{projectName}'")
        board_id = [board for board in projectController.get_project_boards(projectName) if board['name'] == name][0]['id']
        board =  super().get(id=board_id, action="board", req_id=True)['item']
        return self.get(id=board_id, action="board", req_id=True)

    def get_boards(self, projectController:Project=None, name:str=None) -> list:
        if name == None and projectController.active["name"] != None:
            name = projectController.active["name"]
        projectController.get_project_boards(name)

class List(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["list"]
        self.routes = self.instance.routes["list"]
        self.active = {"name": None, "id": None, "board": None ,"content": None}

class Stopwatch(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["stopwatch"]
        self.active = {"name": None, "id": None, "project": None, "board": None , "card": None ,"content": None}

class Card(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["card"]
        self.routes = self.instance.routes["card"]
        self.active = {"name": None, "id": None, "project": None, "board": None , "list": None ,"content": None}
        
class Label(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["label"]
        self.routes = self.instance.routes["label"]
        self.active = {"name": None, "id": None, "project": None, "board": None , "list": None , "card": None ,"content": None}
        
class Task(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["task"]
        self.routes = self.instance.routes["task"]
        self.active = {"name": None, "id": None, "project": None, "board": None , "list": None , "card": None ,"content": None}

class CommentAction(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["comment-action"]
        self.routes = self.instance.routes["comment-action"]
        self.active = {"name": None, "id": None, "project": None, "board": None , "list": None , "card": None ,"content": None}
       
class Attachment(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["attachment"]
        self.routes = self.instance.routes["attachment"]
        
class User(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["user"]
        self.routes = self.instance.routes["user"]
        self.active = {"name": None, "id": None, "content": None}
        
class CardMembership(Controller):
    def __init__(self,instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["card-membership"]
        self.routes = self.instance.routes["card-membership"]
        self.active = {"name": None, "id": None, "project": None, "board": None , "list": None , "card": None ,"content": None}
        
class BoardMembership(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["board-membership"]
        self.routes = self.instance.routes["board-membership"]
        self.active = {"name": None, "id": None, "project": None, "board": None , "content": None}
            
class CardLabel(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["card-label"]
        self.routes = self.instance.routes["label"]
        self.active = {"name": None, "id": None, "project": None, "board": None , "list": None , "card": None ,"content": None}
        
class ProjectManager(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.template = self.instance.templates["project-manager"]
        self.routes = self.instance.routes["project-manager"]
        self.active = {"name": None, "id": None, "user": None ,"project": None, "content": None}

class Background(Controller):
    def __init__(self, instance:Planka=None, **kwargs):
        self.instance:Planka = instance
        self.kwargs:dict = kwargs
        self.template:dict = self.instance.templates["background"]
        self.gradients:list = self.instance.templates["gradients"]

planka = Planka("http://planka.corp.finelines-engineering.com", "hwelch", "Fiber4u!")

projectController = Project(planka)

projectController.set_active("Management API")

boardController = Board(planka)

boards = projectController.get_project_boards()

boardController.get_board(name=boards[0]['name'], projectController=projectController)