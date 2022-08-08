""" 
This file provides definition for events from bitbake server
"""

from typing import Mapping, Any, List, Type

class BBEventBase:
    """Base class for all the events

    Attributes:
        event_name (str): event name like "bb.build.TaskProgress"
    """
    EVENT_NAME: str = "bb.build.TaskFailed"

    def __init__(self: "BBEventBase", event_name: str) -> None:
        """init

        Args:
            self (BBEventBase): none
            event_name (str): event name like "bb.build.TaskProgress"
        """
        self.event_name: str = event_name

    @classmethod
    def is_target(cls, event_name: str) -> bool:
        """Determine if the event is a target event.

        Args:
            event_name (str): event name like "bb.build.TaskProgress"

        Returns:
            bool: whether the event is a target or not
        """
        return cls.EVENT_NAME == event_name

class TaskFailedEvent(BBEventBase):
    EVENT_NAME: str = "bb.build.TaskFailed"

    def __init__(self: "TaskFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        # TODO

class TaskProgressEvent(BBEventBase):
    EVENT_NAME: str = "bb.build.TaskProgress"

    def __init__(self: "TaskProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.progress: int = data["progress"]
        self.rate: str = data["rate"]

class TaskStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.build.TaskStarted"

    def __init__(self: "TaskStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.task: str = data["_task"]
        self.fn: str = data["_fn"]
        self.package: str = data["_package"]
        self.mc: str = data["_mc"]
        self.taskfile: str = data["taskfile"]
        self.taskname: str = data["taskname"]
        self.logfile: str = data["logfile"]
        self.time: float = data["time"]
        self.pn: str = data["pn"]
        self.pv: str = data["pv"]
        self.message: str = data["_message"]
        self.taskflags: Any = data["taskflags"]

class TaskSucceededEvent(BBEventBase):
    EVENT_NAME: str = "bb.build.TaskSucceeded"

    def __init__(self: "TaskSucceededEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.task: str = data["_task"]
        self.fn: str = data["_fn"]
        self.package: str = data["_package"]
        self.mc: str = data["_mc"]
        self.taskfile: str = data["taskfile"]
        self.taskname: str = data["taskname"]
        self.logfile: str = data["logfile"]
        self.time: float = data["time"]
        self.pn: str = data["pn"]
        self.pv: str = data["pv"]
        self.message: str = data["_message"]

class CommandCompletedEvent(BBEventBase):
    EVENT_NAME: str = "bb.command.CommandCompleted"

    def __init__(self: "CommandCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]

class CommandFailedEvent(BBEventBase):
    EVENT_NAME: str = "bb.command.CommandFailed"

    def __init__(self: "CommandFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.error: str = data["error"]
        self.exitcode: str = data["exitcode"]

class CommandExitEvent(BBEventBase):
    EVENT_NAME: str = "bb.command.CommandExit"

    def __init__(self: "CommandExitEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        # TODO

class CacheLoadCompletedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.CacheLoadCompleted"

    def __init__(self: "CacheLoadCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.total: int = data["total"]
        self.msg: str = data["msg"]
        self.num_entries: int = data["num_entries"]

class CacheLoadProgressEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.CacheLoadProgress"

    def __init__(self: "CacheLoadProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.current: int = data["current"]
        self.total: int = data["total"]
        self.msg: str = data["msg"]

class CacheLoadStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.CacheLoadStarted"

    def __init__(self: "CacheLoadStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: str = data["pid"]
        self.msg: str = data["msg"]
        self.total: int = data["total"]

class ConfigFilePathFoundEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ConfigFilePathFound"

    def __init__(self: "ConfigFilePathFoundEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.path: str = data["_path"]

class ConfigFilesFoundEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ConfigFilesFound"

    def __init__(self: "ConfigFilesFoundEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.variable: str = data["_variable"]
        self.values: List[str] = data["_values"]

class ConfigParsedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ConfigParsed"

    def __init__(self: "ConfigParsedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]

class DepTreeGeneratedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.DepTreeGenerated"

    def __init__(self: "DepTreeGeneratedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        # TODO: _depgraph has complex content.
        self.depgraph : Mapping[str, Any] = data["_depgraph"]

class FilesMatchingFoundEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.FilesMatchingFound"

    def __init__(self: "FilesMatchingFoundEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.pattern: str = data["_pattern"]
        self.matches: List[str] = data["_matches"]

class ProcessFinishedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ProcessFinished"

    def __init__(self: "ProcessFinishedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.processname: str = data["processname"]

class ProcessProgressEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ProcessProgress"

    def __init__(self: "ProcessProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.processname: int = data["processname"]
        self.progress: float = data["progress"]

class ProcessStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ProcessStarted"

    def __init__(self: "ProcessStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.processname: int = data["processname"]
        self.total: int = data["total"]

class ReachableStampsEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ReachableStamps"

    def __init__(self: "ReachableStampsEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        # TODO: define more detail
        self.stamps: Mapping[str, str] = data["stamps"]

class RecipeParsedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.RecipeParsed"

    def __init__(self: "RecipeParsedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.fn: str = data["fn"]

class RecipePostKeyExpansionEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.RecipePostKeyExpansion"

    def __init__(self: "RecipePostKeyExpansionEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.fn: str = data["fn"]

class RecipePreFinaliseEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.RecipePreFinalise"

    def __init__(self: "RecipePreFinaliseEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.fn: str = data["fn"]

class RecipeTaskPreProcessEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.RecipeTaskPreProcess"

    def __init__(self: "RecipeTaskPreProcessEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.fn: str = data["fn"]
        self.tasklist: List[str] = data["tasklist"]

class TargetsTreeGeneratedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.TargetsTreeGenerated"

    def __init__(self: "TargetsTreeGeneratedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.model: Mapping[str, Any] = data["_model"]

class TreeDataPreparationCompletedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.TreeDataPreparationCompleted"

    def __init__(self: "TreeDataPreparationCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.total: int = data["total"]
        self.msg: str = data["msg"]

class TreeDataPreparationProgressEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.TreeDataPreparationProgress"

    def __init__(self: "TreeDataPreparationProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        {'pid': 0, 'current': 1, 'total': 1, 'msg': 'Preparing tree data: 1/1'}
        self.pid: int = data["pid"]
        self.current: int = data["current"]
        self.total: int = data["total"]
        self.msg: str = data["msg"]

class TreeDataPreparationStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.TreeDataPreparationStarted"

    def __init__(self: "TreeDataPreparationStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.msg: str = data["msg"]

class runQueueTaskFailedEvent(BBEventBase):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskFailed"

    def __init__(self: "runQueueTaskFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        # TODO

class runQueueTaskStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskStarted"

    def __init__(self: "runQueueTaskStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.taskid: str = data["taskid"]
        self.taskstring: str = data["taskstring"]
        self.taskname: str = data["taskname"]
        self.taskfile: str = data["taskfile"]
        self.taskhash: str = data["taskhash"]
        self.stats: Any = data["stats"].__dict__
        self.noexec: bool = data["noexec"]

class runQueueTaskSkippedEvent(BBEventBase):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskSkipped"

    def __init__(self: "runQueueTaskSkippedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.taskid: str = data["taskid"]
        self.taskstring: str = data["taskstring"]
        self.taskname: str = data["taskname"]
        self.taskfile: str = data["taskfile"]
        self.taskhash: str = data["taskhash"]
        self.stats: Any = data["stats"]
        self.reason: str = data["reason"]

class sceneQueueCompleteEvent(BBEventBase):
    EVENT_NAME: str = "bb.runqueue.sceneQueueComplete"

    def __init__(self: "sceneQueueCompleteEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.stats: Any = data["stats"]

class runQueueTaskCompletedEvent(BBEventBase):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskCompleted"

    def __init__(self: "runQueueTaskCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.taskid: str = data["taskid"]
        self.taskstring: str = data["taskstring"]
        self.taskname: str = data["taskname"]
        self.taskfile: str = data["taskfile"]
        self.taskhash: str = data["taskhash"]
        self.stats: Any = data["stats"]

class BuildInitEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.BuildInit"

    def __init__(self: "BuildInitEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.name: str = data["_name"]
        self.pkgs: List[Any] = data["_pkgs"]
        self.pid: int = data["pid"]
        self.failures: int = data["_failures"]

class BuildStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.BuildStarted"

    def __init__(self: "BuildStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.msg: str = data["msg"]
        self.name: str = data["_name"]
        self.pkgs: List[str] = data["_pkgs"]
        self.failures: int = data["_failures"]

class HeartbeatEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.HeartbeatEvent"

    def __init__(self: "HeartbeatEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.time: float = data["time"]

class NoProviderEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.NoProvider"

    def __init__(self: "NoProviderEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.item: int = data["_item"]
        self.runtime: bool = data["_runtime"]
        self.dependees: List[Any] = data["_dependees"]
        self.reasons: List[Any] = data["_reasons"]
        self.close_matches: List[Any] = data["_close_matches"]
        

class MonitorDiskEventEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.MonitorDiskEvent"

    def __init__(self: "MonitorDiskEventEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.disk_usage: Mapping[str, Any] = data["disk_usage"]

class LogRecord(BBEventBase):
    EVENT_NAME: str = "logging.LogRecord"

    def __init__(self: "LogRecord", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.log: Mapping[str, Any] = data


class UnknownEvent(BBEventBase):

    def __init__(self: "UnknownEvent", event_name: str, data: Mapping[str, Any]) -> None:
        super().__init__(event_name)
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