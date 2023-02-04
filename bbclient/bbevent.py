""" 
This file provides definition for events from bitbake server
"""

from typing import Mapping, Any, List, Type, Callable, Optional, Iterable

class BBEventBase:
    """Base class for all the events

    Attributes:
        event_name (str): event name like "bb.build.TaskProgress"
    """
    EVENT_NAME: str = "bb.build.TaskFailed"

    def __init__(self: "BBEventBase", event_name: str, data: Mapping[str, Any]) -> None:
        """init

        Args:
            self (BBEventBase): none
            event_name (str): event name like "bb.build.TaskProgress"
        """
        self.event_name: str = event_name
        self.pid: int = data.get("pid", "")

    def __str__(self: "BBEventBase") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        return self.__class__.__name__ + ": " + str(vars(self))

    @classmethod
    def is_target(cls, event_name: str) -> bool:
        """Determine if the event is a target event.

        Args:
            event_name (str): event name like "bb.build.TaskProgress"

        Returns:
            bool: whether the event is a target or not
        """
        return cls.EVENT_NAME == event_name

class TaskBase(BBEventBase):
    EVENT_NAME: str = "bb.build.TaskBase"

    def __init__(self: "TaskFailedEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.task = data.get("_task")
        self.fn = data.get("_fn")
        self.package = data.get("_package")
        self.mc = data.get("_mc")
        self.taskfile = data.get("taskfile")
        self.taskname = data.get("taskname")
        self.logfile = data.get("logfile")
        self.time = data.get("time")
        self.pn = data.get("pn")
        self.pv = data.get("pv")
        self.message = data.get("_message")

class TaskFailedEvent(TaskBase):
    EVENT_NAME: str = "bb.build.TaskFailed"

    def __init__(self: "TaskFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.is_err_printed = data.get("errprinted")

class TaskProgressEvent(BBEventBase):
    EVENT_NAME: str = "bb.build.TaskProgress"

    def __init__(self: "TaskProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.progress: int = data["progress"]
        self.rate: str = data["rate"]

class TaskStartedEvent(TaskBase):
    EVENT_NAME: str = "bb.build.TaskStarted"

    def __init__(self: "TaskStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.taskflags: Any = data["taskflags"]

class TaskSucceededEvent(TaskBase):
    EVENT_NAME: str = "bb.build.TaskSucceeded"

    def __init__(self: "TaskSucceededEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class CommandCompletedEvent(BBEventBase):
    EVENT_NAME: str = "bb.command.CommandCompleted"

    def __init__(self: "CommandCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class CommandExitEvent(BBEventBase):
    EVENT_NAME: str = "bb.command.CommandExit"

    def __init__(self: "CommandExitEvent", data: Mapping[str, Any], event_name: str = EVENT_NAME) -> None:
        super().__init__(event_name, data)
        self.exitcode: str = data["exitcode"]

class CommandFailedEvent(CommandExitEvent):
    EVENT_NAME: str = "bb.command.CommandFailed"

    def __init__(self: "CommandFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(data, self.EVENT_NAME)
        self.error: str = data["error"]

class OperationStarted(BBEventBase):
    EVENT_NAME: str = "bb.event.OperationStarted"

    def __init__(self: "OperationStarted", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.msg = data["msg"]

class OperationProgress(BBEventBase):
    EVENT_NAME: str = "bb.event.OperationProgress"

    def __init__(self: "OperationProgress", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.current = data["current"]
        self.total = data["total"]
        self.msg = data["msg"]

class OperationCompletedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.OperationCompletedEvent"

    def __init__(self: "CacheLoadCompletedEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.total = data.get("total", "")
        self.msg = data.get("msg", "")

class CacheLoadCompletedEvent(OperationCompletedEvent):
    EVENT_NAME: str = "bb.event.CacheLoadCompleted"

    def __init__(self: "CacheLoadCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.num_entries: int = data["num_entries"]

class CacheLoadProgressEvent(OperationProgress):
    EVENT_NAME: str = "bb.event.CacheLoadProgress"

    def __init__(self: "CacheLoadProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class CacheLoadStartedEvent(OperationStarted):
    EVENT_NAME: str = "bb.event.CacheLoadStarted"

    def __init__(self: "CacheLoadStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.total: int = data["total"]

class ConfigFilePathFoundEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ConfigFilePathFound"

    def __init__(self: "ConfigFilePathFoundEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.path: str = data["_path"]

class ConfigFilesFoundEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ConfigFilesFound"

    def __init__(self: "ConfigFilesFoundEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.variable: str = data["_variable"]
        self.values: List[str] = data["_values"]

class ConfigParsedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ConfigParsed"

    def __init__(self: "ConfigParsedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class DepTreeGeneratedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.DepTreeGenerated"

    def __init__(self: "DepTreeGeneratedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        # TODO: _depgraph has complex content.
        self.depgraph : Mapping[str, Any] = data["_depgraph"]

class FilesMatchingFoundEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.FilesMatchingFound"

    def __init__(self: "FilesMatchingFoundEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.pattern: str = data["_pattern"]
        self.matches: List[str] = data["_matches"]

class ProcessFinishedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ProcessFinished"

    def __init__(self: "ProcessFinishedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.processname: str = data["processname"]

class ProcessProgressEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ProcessProgress"

    def __init__(self: "ProcessProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.processname: int = data["processname"]
        self.progress: float = data["progress"]

class ProcessStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ProcessStarted"

    def __init__(self: "ProcessStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.processname: int = data["processname"]
        self.total: int = data["total"]

class ReachableStampsEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ReachableStamps"

    def __init__(self: "ReachableStampsEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        # TODO: define more detail
        self.stamps: Mapping[str, str] = data["stamps"]

class RecipeEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.RecipeEvent"

    def __init__(self: "RecipeEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.fn: str = data["fn"]

class RecipeParsedEvent(RecipeEvent):
    EVENT_NAME: str = "bb.event.RecipeParsed"

    def __init__(self: "RecipeParsedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class RecipePostKeyExpansionEvent(RecipeEvent):
    EVENT_NAME: str = "bb.event.RecipePostKeyExpansion"

    def __init__(self: "RecipePostKeyExpansionEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class RecipePreFinaliseEvent(RecipeEvent):
    EVENT_NAME: str = "bb.event.RecipePreFinalise"

    def __init__(self: "RecipePreFinaliseEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class RecipeTaskPreProcessEvent(RecipeEvent):
    EVENT_NAME: str = "bb.event.RecipeTaskPreProcess"

    def __init__(self: "RecipeTaskPreProcessEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.tasklist: List[str] = data["tasklist"]

class TargetsTreeGeneratedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.TargetsTreeGenerated"

    def __init__(self: "TargetsTreeGeneratedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.model: Mapping[str, Any] = data["_model"]

class TreeDataPreparationCompletedEvent(OperationCompletedEvent):
    EVENT_NAME: str = "bb.event.TreeDataPreparationCompleted"

    def __init__(self: "TreeDataPreparationCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class TreeDataPreparationProgressEvent(OperationProgress):
    EVENT_NAME: str = "bb.event.TreeDataPreparationProgress"

    def __init__(self: "TreeDataPreparationProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class TreeDataPreparationStartedEvent(OperationStarted):
    EVENT_NAME: str = "bb.event.TreeDataPreparationStarted"

    def __init__(self: "TreeDataPreparationStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class runQueueEvent(BBEventBase):
    EVENT_NAME: str = "bb.runqueue.runQueueEvent"

    def __init__(self: "runQueueEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.taskid = data["taskid"]
        self.taskstring = data["taskstring"]
        self.taskname = data["taskname"]
        self.taskfile = data["taskfile"]
        self.taskhash = data["taskhash"]
        self.stats = data["stats"].__dict__

class runQueueTaskFailedEvent(runQueueEvent):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskFailed"

    def __init__(self: "runQueueTaskFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.exitcode = data["exitcode"]

class runQueueTaskStartedEvent(runQueueEvent):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskStarted"

    def __init__(self: "runQueueTaskStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.noexec: bool = data["noexec"]

class runQueueTaskSkippedEvent(runQueueEvent):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskSkipped"

    def __init__(self: "runQueueTaskSkippedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.reason: str = data["reason"]

class sceneQueueEvent(runQueueEvent):
    EVENT_NAME: str = "bb.runqueue.sceneQueueEvent"

    def __init__(self: "sceneQueueEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.taskstring = data["taskstring"]
        self.taskname = data["taskname"]
        self.taskfile = data["taskfile"]
        self.taskhash = data["taskhash"]

class sceneQueueCompleteEvent(sceneQueueEvent):
    EVENT_NAME: str = "bb.runqueue.sceneQueueComplete"

    def __init__(self: "sceneQueueCompleteEvent", data: Mapping[str, Any]) -> None:
        #because of bug in bitbake
        #super().__init__(self.EVENT_NAME, data)
        BBEventBase.__init__(self, self.EVENT_NAME, data)
        self.stats: Any = data["stats"]

class runQueueTaskCompletedEvent(runQueueEvent):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskCompleted"

    def __init__(self: "runQueueTaskCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class BuildBaseEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.BuildBase"

    def __init__(self: "BuildBaseEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.name = data["_name"]
        self.pkgs = data["_pkgs"]
        self.failures = data["_failures"]

class BuildInitEvent(BuildBaseEvent):
    EVENT_NAME: str = "bb.event.BuildInit"

    def __init__(self: "BuildInitEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

class BuildStartedEvent(BuildBaseEvent, OperationStarted):
    EVENT_NAME: str = "bb.event.BuildStarted"

    def __init__(self: "BuildStartedEvent", data: Mapping[str, Any]) -> None:
        BuildBaseEvent.__init__(self, self.EVENT_NAME, data)
        OperationStarted.__init__(self, self.EVENT_NAME, data)

class HeartbeatEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.HeartbeatEvent"

    def __init__(self: "HeartbeatEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.time: float = data["time"]

class NoProviderEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.NoProvider"

    def __init__(self: "NoProviderEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.item: int = data["_item"]
        self.runtime: bool = data["_runtime"]
        self.dependees: List[Any] = data["_dependees"]
        self.reasons: List[Any] = data["_reasons"]
        self.close_matches: List[Any] = data["_close_matches"]
        

class MonitorDiskEventEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.MonitorDiskEvent"

    def __init__(self: "MonitorDiskEventEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.disk_usage: Mapping[str, Any] = data["disk_usage"]

class LogRecord(BBEventBase):
    EVENT_NAME: str = "logging.LogRecord"

    def __init__(self: "LogRecord", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.log: Mapping[str, Any] = data

class UnknownEvent(BBEventBase):

    def __init__(self: "UnknownEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.data: Mapping[str, Any] = data

ALL_BB_EVENTS: List[Type[BBEventBase]] = [
    TaskFailedEvent,
    TaskProgressEvent,
    TaskStartedEvent,
    TaskSucceededEvent,
    CommandCompletedEvent,
    CommandFailedEvent,
    CommandExitEvent,
    CacheLoadCompletedEvent,
    CacheLoadProgressEvent,
    CacheLoadStartedEvent,
    ConfigFilePathFoundEvent,
    ConfigFilesFoundEvent,
    ConfigParsedEvent,
    DepTreeGeneratedEvent,
    FilesMatchingFoundEvent,
    ProcessFinishedEvent,
    ProcessProgressEvent,
    ProcessStartedEvent,
    ReachableStampsEvent,
    RecipeParsedEvent,
    RecipePostKeyExpansionEvent,
    RecipePreFinaliseEvent,
    RecipeTaskPreProcessEvent,
    TargetsTreeGeneratedEvent,
    TreeDataPreparationCompletedEvent,
    TreeDataPreparationProgressEvent,
    TreeDataPreparationStartedEvent,
    runQueueTaskFailedEvent,
    runQueueTaskStartedEvent,
    runQueueTaskSkippedEvent,
    sceneQueueCompleteEvent,
    runQueueTaskCompletedEvent,
    BuildInitEvent,
    BuildStartedEvent,
    HeartbeatEvent,
    NoProviderEvent,
    MonitorDiskEventEvent,
    LogRecord,
]