from typing import Literal, get_args

ActionEvent = Literal['actionCreate']
ActionEvents: tuple[ActionEvent, ...] = get_args(ActionEvent)

AttachmentEvent = Literal['attachmentCreate', 'attachmentUpdate', 'attachmentDelete'] 
AttachmentEvents: tuple[AttachmentEvent, ...] = get_args(AttachmentEvent)

BackgroundImageEvent = Literal['backgroundImageCreate', 'backgroundImageDelete'] 
BackgroundImageEvents: tuple[BackgroundImageEvent, ...] = get_args(BackgroundImageEvent)

BaseCustomFieldGroupEvent = Literal['baseCustomFieldGroupCreate', 'baseCustomFieldGroupUpdate', 'baseCustomFieldGroupDelete'] 
BaseCustomFieldGroupEvents: tuple[BaseCustomFieldGroupEvent, ...] = get_args(BaseCustomFieldGroupEvent)

BoardEvent = Literal['boardCreate', 'boardUpdate', 'boardDelete']
BoardEvents: tuple[BoardEvent, ...] = get_args(BoardEvent)

BoardMembershipEvent = Literal['boardMembershipCreate', 'boardMembershipUpdate', 'boardMembershipDelete'] 
BoardMembershipEvents: tuple[BoardMembershipEvent, ...] = get_args(BoardMembershipEvent)

CardEvent = Literal['cardCreate', 'cardUpdate', 'cardDelete'] 
CardEvents: tuple[CardEvent, ...] = get_args(CardEvent)

CardLabelEvent = Literal['cardLabelCreate', 'cardLabelDelete']
CardLabelEvents: tuple[CardLabelEvent, ...] = get_args(CardLabelEvent)

CardMembershipEvent = Literal['cardMembershipCreate', 'cardMembershipDelete'] 
CardMembershipEvents: tuple[CardMembershipEvent, ...] = get_args(CardMembershipEvent)

CommentEvent = Literal['commentCreate', 'commentUpdate', 'commentDelete'] 
CommentEvents: tuple[CommentEvent, ...] = get_args(CommentEvent)

ConfigEvent = Literal['configUpdate']
ConfigEvents: tuple[ConfigEvent, ...] = get_args(ConfigEvent)

CustomFieldEvent = Literal['customFieldCreate', 'customFieldUpdate', 'customFieldDelete'] 
CustomFieldEvents: tuple[CustomFieldEvent, ...] = get_args(CustomFieldEvent)

CustomFieldGroupEvent = Literal['customFieldGroupCreate', 'customFieldGroupUpdate', 'customFieldGroupDelete'] 
CustomFieldGroupEvents: tuple[CustomFieldGroupEvent, ...] = get_args(CustomFieldGroupEvent) 

CustomFieldValueEvent = Literal['customFieldValueUpdate', 'customFieldValueDelete']
CustomFieldValueEvents: tuple[CustomFieldValueEvent, ...] = get_args(CustomFieldValueEvent)

LabelEvent = Literal['labelCreate', 'labelUpdate', 'labelDelete'] 
LabelEvents: tuple[LabelEvent, ...] = get_args(LabelEvent)

ListEvent = Literal['listCreate', 'listUpdate', 'listClear', 'listDelete'] 
ListEvents: tuple[ListEvent, ...] = get_args(ListEvent)

NotificationEvent = Literal['notificationCreate', 'notificationUpdate'] 
NotificationEvents: tuple[NotificationEvent, ...] = get_args(NotificationEvent)

NotificationServiceEvent = Literal['notificationServiceCreate', 'notificationServiceUpdate', 'notificationServiceDelete'] 
NotificationServiceEvents: tuple[NotificationServiceEvent, ...] = get_args(NotificationServiceEvent)

ProjectEvent = Literal['projectCreate', 'projectUpdate', 'projectDelete']
ProjectEvents: tuple[ProjectEvent, ...] = get_args(ProjectEvent)

ProjectManagerEvent =  Literal['projectManagerCreate', 'projectManagerDelete'] 
ProjectManagerEvents: tuple[ProjectManagerEvent, ...] = get_args(ProjectManagerEvent)

TaskEvent = Literal['taskCreate', 'taskUpdate', 'taskDelete'] 
TaskEvents: tuple[TaskEvent, ...] = get_args(TaskEvent)

TaskListEvent = Literal['taskListCreate', 'taskListUpdate', 'taskListDelete'] 
TaskListEvents: tuple[TaskListEvent, ...] = get_args(TaskListEvent)

UserEvent = Literal['userCreate', 'userUpdate', 'userDelete'] 
UserEvents: tuple[UserEvent, ...] = get_args(UserEvent)

WebhookEvent =  Literal['webhookCreate', 'webhookUpdate', 'webhookDelete']
WebhookEvents: tuple[WebhookEvent, ...] = get_args(WebhookEvent)

PlankaEvent = (
    ActionEvent | AttachmentEvent | BackgroundImageEvent | BaseCustomFieldGroupEvent |
    BoardEvent | BoardMembershipEvent | CardEvent | CardLabelEvent | CardMembershipEvent |
    CommentEvent | ConfigEvent | CustomFieldEvent | CustomFieldGroupEvent | 
    CustomFieldValueEvent | LabelEvent | ListEvent | NotificationEvent | NotificationServiceEvent | 
    ProjectEvent | ProjectManagerEvent | TaskEvent | TaskListEvent | UserEvent | WebhookEvent
)

PlankaEvents: tuple[PlankaEvent, ...] = tuple(e for et in get_args(PlankaEvent) for e in get_args(et))