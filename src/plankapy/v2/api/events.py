from typing import Literal

ActionEvent = Literal['actionCreate']
ActionEvents: tuple[ActionEvent] = ('actionCreate', )

AttachmentEvent = Literal['attachmentCreate', 'attachmentUpdate', 'attachmentDelete'] 
AttachmentEvents: tuple[AttachmentEvent] = AttachmentEvent.__args__

BackgroundImageEvent = Literal['backgroundImageCreate', 'backgroundImageDelete'] 
BackgroundImageEvents: tuple[BackgroundImageEvent] = BackgroundImageEvent.__args__

BaseCustomFieldGroupEvent = Literal['baseCustomFieldGroupCreate', 'baseCustomFieldGroupUpdate', 'baseCustomFieldGroupDelete'] 
BaseCustomFieldGroupEvents: tuple[BaseCustomFieldGroupEvent] = BaseCustomFieldGroupEvent.__args__

BoardEvent = Literal['boardCreate', 'boardUpdate', 'boardDelete']
BoardEvents: tuple[BoardEvent] = BoardEvent.__args__

BoardMembershipEvent = Literal['boardMembershipCreate', 'boardMembershipUpdate', 'boardMembershipDelete'] 
BoardMembershipEvents: tuple[BoardMembershipEvent] = BoardMembershipEvent.__args__

CardEvent = Literal['cardCreate', 'cardUpdate', 'cardDelete'] 
CardEvents: tuple[CardEvent] = CardEvent.__args__

CardLabelEvent = Literal['cardLabelCreate', 'cardLabelDelete']
CardLabelEvents: tuple[CardLabelEvent] = CardLabelEvent.__args__

CardMembershipEvent = Literal['cardMembershipCreate', 'cardMembershipDelete'] 
CardMembershipEvents: tuple[CardMembershipEvent] = CardMembershipEvent.__args__

CommentEvent = Literal['commentCreate', 'commentUpdate', 'commentDelete'] 
CommentEvents: tuple[CommentEvent] = CommentEvent.__args__

ConfigEvent = Literal['configUpdate']
ConfigEvents: tuple[ConfigEvent] = ('configUpdate', )

CustomFieldEvent = Literal['customFieldCreate', 'customFieldUpdate', 'customFieldDelete'] 
CustomFieldEvents: tuple[CustomFieldEvent] = CustomFieldEvent.__args__

CustomFieldGroupEvent = Literal['customFieldGroupCreate', 'customFieldGroupUpdate', 'customFieldGroupDelete'] 
CustomFieldGroupEvents: tuple[CustomFieldGroupEvent] = CustomFieldGroupEvent.__args__ 

CustomFieldValueEvent = Literal['customFieldValueUpdate', 'customFieldValueDelete']
CustomFieldValueEvents: tuple[CustomFieldValueEvent] = CustomFieldValueEvent.__args__

LabelEvent = Literal['labelCreate', 'labelUpdate', 'labelDelete'] 
LabelEvents: tuple[LabelEvent] = LabelEvent.__args__

ListEvent = Literal['listCreate', 'listUpdate', 'listClear', 'listDelete'] 
ListEvents: tuple[ListEvent] = ListEvent.__args__

NotificationEvent = Literal['notificationCreate', 'notificationUpdate'] 
NotificationEvents: tuple[NotificationEvent] = NotificationEvent.__args__

NotificationServiceEvent = Literal['notificationServiceCreate', 'notificationServiceUpdate', 'notificationServiceDelete'] 
NotificationServiceEvents: tuple[NotificationServiceEvent] = NotificationServiceEvent.__args__

ProjectEvent = Literal['projectCreate', 'projectUpdate', 'projectDelete']
ProjectEvents: tuple[ProjectEvent] = ProjectEvent.__args__

ProjectManagerEvent =  Literal['projectManagerCreate', 'projectManagerDelete'] 
ProjectManagerEvents: tuple[ProjectManagerEvent] = ProjectManagerEvent.__args__

TaskEvent = Literal['taskCreate', 'taskUpdate', 'taskDelete'] 
TaskEvents: tuple[TaskEvent] = TaskEvent.__args__

TaskListEvent = Literal['taskListCreate', 'taskListUpdate', 'taskListDelete'] 
TaskListEvents: tuple[TaskListEvent] = TaskListEvent.__args__

UserEvent = Literal['userCreate', 'userUpdate', 'userDelete'] 
UserEvents: tuple[UserEvent] = UserEvent.__args__

WebhookEvent =  Literal['webhookCreate', 'webhookUpdate', 'webhookDelete']
WebhookEvents: tuple[WebhookEvent] = WebhookEvent.__args__

PlankaEvent = (
    ActionEvent | AttachmentEvent | BackgroundImageEvent | BaseCustomFieldGroupEvent |
    BoardEvent | BoardMembershipEvent | CardEvent | CardLabelEvent | CardMembershipEvent |
    CommentEvent | ConfigEvent | CustomFieldEvent | CustomFieldGroupEvent | 
    CustomFieldValueEvent | LabelEvent | ListEvent | NotificationEvent | NotificationServiceEvent | 
    ProjectEvent | ProjectManagerEvent | TaskEvent | TaskListEvent | UserEvent | WebhookEvent
)

PlankaEvents: tuple[PlankaEvent, ...] = (
    ActionEvents + AttachmentEvents +  BackgroundImageEvents + BaseCustomFieldGroupEvents + 
    BoardEvents + BoardMembershipEvents + CardEvents + CardLabelEvents + CardMembershipEvents + 
    CommentEvents + ConfigEvents + CustomFieldEvents + CustomFieldGroupEvents + 
    CustomFieldValueEvents + LabelEvents + ListEvents + NotificationEvents + NotificationServiceEvents + 
    ProjectEvents + ProjectManagerEvents + TaskEvents + TaskListEvents + UserEvents + WebhookEvents
)