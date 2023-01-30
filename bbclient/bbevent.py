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
        self.pid: int = data["pid"]

    def __str__(self: "BBEventBase") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

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
        super().__init__(event_name)
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

    def __str__(self: "TaskFailedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class TaskFailedEvent(TaskBase):
    EVENT_NAME: str = "bb.build.TaskFailed"

    def __init__(self: "TaskFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.is_err_printed = data.get("errprinted")

    def __str__(self: "TaskFailedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class TaskProgressEvent(BBEventBase):
    EVENT_NAME: str = "bb.build.TaskProgress"

    def __init__(self: "TaskProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.progress: int = data["progress"]
        self.rate: str = data["rate"]

    def __str__(self: "TaskProgressEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        return f"pid:{self.pid} progress:{self.progress} rate:{self.rate}"

class TaskStartedEvent(TaskBase):
    EVENT_NAME: str = "bb.build.TaskStarted"

    def __init__(self: "TaskStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.taskflags: Any = data["taskflags"]

    def __str__(self: "TaskStartedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class TaskSucceededEvent(TaskBase):
    EVENT_NAME: str = "bb.build.TaskSucceeded"

    def __init__(self: "TaskSucceededEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "TaskSucceededEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class CommandCompletedEvent(BBEventBase):
    EVENT_NAME: str = "bb.command.CommandCompleted"

    def __init__(self: "CommandCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "CommandCompletedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class CommandExitEvent(BBEventBase):
    EVENT_NAME: str = "bb.command.CommandExit"

    def __init__(self: "CommandExitEvent", data: Mapping[str, Any], event_name: str = EVENT_NAME) -> None:
        super().__init__(event_name, data)
        self.exitcode: str = data["exitcode"]

    def __str__(self: "CommandExitEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class CommandFailedEvent(CommandExitEvent):
    EVENT_NAME: str = "bb.command.CommandFailed"

    def __init__(self: "CommandFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(data, self.EVENT_NAME)
        self.error: str = data["error"]

    def __str__(self: "CommandFailedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class OperationStarted(BBEventBase):
    EVENT_NAME: str = "bb.event.OperationStarted"

    def __init__(self: "OperationStarted", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.msg = data["msg"]

    def __str__(self: "OperationStarted") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class OperationProgress(BBEventBase):
    EVENT_NAME: str = "bb.event.OperationProgress"

    def __init__(self: "OperationProgress", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.current = data["current"]
        self.total = data["total"]
        self.msg = data["msg"]

    def __str__(self: "OperationProgress") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class OperationCompletedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.OperationCompletedEvent"

    def __init__(self: "CacheLoadCompletedEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.total = data["total"]
        self.msg = data["msg"]

    def __str__(self: "CacheLoadCompletedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class CacheLoadCompletedEvent(OperationCompletedEvent):
    EVENT_NAME: str = "bb.event.CacheLoadCompleted"

    def __init__(self: "CacheLoadCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.num_entries: int = data["num_entries"]

    def __str__(self: "CacheLoadCompletedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class CacheLoadProgressEvent(OperationProgress):
    EVENT_NAME: str = "bb.event.CacheLoadProgress"

    def __init__(self: "CacheLoadProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "CacheLoadProgressEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        return f"pid:{self.pid} current:{self.current} total:{self.total} msg:{self.msg}"

class CacheLoadStartedEvent(OperationStarted):
    EVENT_NAME: str = "bb.event.CacheLoadStarted"

    def __init__(self: "CacheLoadStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.total: int = data["total"]

    def __str__(self: "CacheLoadStartedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class ConfigFilePathFoundEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ConfigFilePathFound"

    def __init__(self: "ConfigFilePathFoundEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.path: str = data["_path"]

    def __str__(self: "ConfigFilePathFoundEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class ConfigFilesFoundEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ConfigFilesFound"

    def __init__(self: "ConfigFilesFoundEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.variable: str = data["_variable"]
        self.values: List[str] = data["_values"]

    def __str__(self: "ConfigFilesFoundEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class ConfigParsedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ConfigParsed"

    def __init__(self: "ConfigParsedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "ConfigParsedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class DepTreeGeneratedEvent(OperationCompletedEvent):
    EVENT_NAME: str = "bb.event.DepTreeGenerated"

    def __init__(self: "DepTreeGeneratedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        # TODO: _depgraph has complex content.
        self.depgraph : Mapping[str, Any] = data["_depgraph"]

    def __str__(self: "DepTreeGeneratedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class FilesMatchingFoundEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.FilesMatchingFound"

    def __init__(self: "FilesMatchingFoundEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.pattern: str = data["_pattern"]
        self.matches: List[str] = data["_matches"]

    def __str__(self: "FilesMatchingFoundEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class ProcessFinishedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ProcessFinished"

    def __init__(self: "ProcessFinishedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.processname: str = data["processname"]

    def __str__(self: "ProcessFinishedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class ProcessProgressEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ProcessProgress"

    def __init__(self: "ProcessProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.processname: int = data["processname"]
        self.progress: float = data["progress"]

    def __str__(self: "ProcessProgressEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        return f"pid:{self.pid} processname:{self.processname} progress:{self.progress}"

class ProcessStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ProcessStarted"

    def __init__(self: "ProcessStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.processname: int = data["processname"]
        self.total: int = data["total"]

    def __str__(self: "ProcessStartedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class ReachableStampsEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ReachableStamps"

    def __init__(self: "ReachableStampsEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        # TODO: define more detail
        self.stamps: Mapping[str, str] = data["stamps"]

    def __str__(self: "ReachableStampsEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class RecipeEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.RecipeEvent"

    def __init__(self: "RecipeEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.fn: str = data["fn"]

    def __str__(self: "RecipeEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class RecipeParsedEvent(RecipeEvent):
    EVENT_NAME: str = "bb.event.RecipeParsed"

    def __init__(self: "RecipeParsedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "RecipeParsedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class RecipePostKeyExpansionEvent(RecipeEvent):
    EVENT_NAME: str = "bb.event.RecipePostKeyExpansion"

    def __init__(self: "RecipePostKeyExpansionEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "RecipePostKeyExpansionEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class RecipePreFinaliseEvent(RecipeEvent):
    EVENT_NAME: str = "bb.event.RecipePreFinalise"

    def __init__(self: "RecipePreFinaliseEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "RecipePreFinaliseEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class RecipeTaskPreProcessEvent(RecipeEvent):
    EVENT_NAME: str = "bb.event.RecipeTaskPreProcess"

    def __init__(self: "RecipeTaskPreProcessEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.tasklist: List[str] = data["tasklist"]

    def __str__(self: "RecipeTaskPreProcessEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class TargetsTreeGeneratedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.TargetsTreeGenerated"

    def __init__(self: "TargetsTreeGeneratedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.model: Mapping[str, Any] = data["_model"]

    def __str__(self: "TargetsTreeGeneratedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class TreeDataPreparationCompletedEvent(OperationCompletedEvent):
    EVENT_NAME: str = "bb.event.TreeDataPreparationCompleted"

    def __init__(self: "TreeDataPreparationCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "TreeDataPreparationCompletedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class TreeDataPreparationProgressEvent(OperationProgress):
    EVENT_NAME: str = "bb.event.TreeDataPreparationProgress"

    def __init__(self: "TreeDataPreparationProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "TreeDataPreparationProgressEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class TreeDataPreparationStartedEvent(OperationStarted):
    EVENT_NAME: str = "bb.event.TreeDataPreparationStarted"

    def __init__(self: "TreeDataPreparationStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "TreeDataPreparationStartedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

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

    def __str__(self: "runQueueEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError
    
class runQueueTaskFailedEvent(runQueueEvent):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskFailed"

    def __init__(self: "runQueueTaskFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.exitcode = data["exitcode"]

    def __str__(self: "runQueueTaskFailedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class runQueueTaskStartedEvent(runQueueEvent):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskStarted"

    def __init__(self: "runQueueTaskStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.noexec: bool = data["noexec"]

    def __str__(self: "runQueueTaskStartedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class runQueueTaskSkippedEvent(runQueueEvent):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskSkipped"

    def __init__(self: "runQueueTaskSkippedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.reason: str = data["reason"]

    def __str__(self: "runQueueTaskSkippedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class sceneQueueEvent(runQueueEvent):
    EVENT_NAME: str = "bb.runqueue.sceneQueueEvent"

    def __init__(self: "sceneQueueEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.taskstring = data["taskstring"]
        self.taskname = data["taskname"]
        self.taskfile = data["taskfile"]
        self.taskhash = data["taskhash"]

    def __str__(self: "sceneQueueEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class sceneQueueCompleteEvent(sceneQueueEvent):
    EVENT_NAME: str = "bb.runqueue.sceneQueueComplete"

    def __init__(self: "sceneQueueCompleteEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.stats: Any = data["stats"]

    def __str__(self: "sceneQueueCompleteEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class runQueueTaskCompletedEvent(runQueueEvent):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskCompleted"

    def __init__(self: "runQueueTaskCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "runQueueTaskCompletedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class BuildBaseEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.BuildBase"

    def __init__(self: "BuildBaseEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name, data)
        self.name = data["_name"]
        self.pkgs = data["_pkgs"]
        self.failures = data["_failures"]

    def __str__(self: "BuildBaseEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class BuildInitEvent(BuildBaseEvent):
    EVENT_NAME: str = "bb.event.BuildInit"

    def __init__(self: "BuildInitEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)

    def __str__(self: "BuildInitEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class BuildStartedEvent(BuildBaseEvent, OperationStarted):
    EVENT_NAME: str = "bb.event.BuildStarted"

    def __init__(self: "BuildStartedEvent", data: Mapping[str, Any]) -> None:
        BuildBaseEvent.__init__(self, self.EVENT_NAME, data)
        OperationStarted.__init__(self, self.EVENT_NAME, data)

    def __str__(self: "BuildStartedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class HeartbeatEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.HeartbeatEvent"

    def __init__(self: "HeartbeatEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.time: float = data["time"]

    def __str__(self: "HeartbeatEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class NoProviderEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.NoProvider"

    def __init__(self: "NoProviderEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.item: int = data["_item"]
        self.runtime: bool = data["_runtime"]
        self.dependees: List[Any] = data["_dependees"]
        self.reasons: List[Any] = data["_reasons"]
        self.close_matches: List[Any] = data["_close_matches"]
        
    def __str__(self: "NoProviderEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError


class MonitorDiskEventEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.MonitorDiskEvent"

    def __init__(self: "MonitorDiskEventEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME, data)
        self.disk_usage: Mapping[str, Any] = data["disk_usage"]

    def __str__(self: "MonitorDiskEventEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class LogRecord(BBEventBase):
    EVENT_NAME: str = "logging.LogRecord"

    def __init__(self: "LogRecord", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.log: Mapping[str, Any] = data

    def __str__(self: "LogRecord") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        return "[LOG EVENT]" + self.log["msg"] % self.log["args"]


class UnknownEvent(BBEventBase):

    def __init__(self: "UnknownEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name)
        self.data: Mapping[str, Any] = data

    def __str__(self: "UnknownEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

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