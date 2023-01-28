""" 
This file provides definition for events from bitbake server
"""

from typing import Mapping, Any, List, Type, Callable

class BBEventObservatory:
    """Reciver class for BBEvents.

    Attributes:
        TODO:
    """
    def __init__(self: "BBEventCallBack") -> None:
        self.__callbacks: Map[BBEventBase, Callable[[BBEventBase], bool]] = {}

    def notify(self: "BBEventCallBack", event_raw_data: Any) -> bool:
        event: Optional[BBEventBase] = self.__convert(event_raw_data)
        event_type: Type = type(event)
        if not event_type in self.__callbacks.keys():
            return True
        return self.__callbacks[type(event)](event)

    def __register_callback(self: "BBEventCallBack", target: Type[BBEventBase], callback: Callable[[BBEventBase], bool]) -> None:
        pass

    def __convert(self: "BBClient", event_raw_data: Any) -> Optional[BBEventBase]:
        cur_event_name: str = str(type(event_raw_data))[8:-2]
        itr: Iterable = filter(lambda x: x.is_target(cur_event_name), ALL_BB_EVENTS)
        event_class: Optional[Type[BBEventBase]] = next(itr, None) # type: ignore
        ret: BBEventBase = event_class(cur_event.__dict__) if event_class else UnknownEvent(cur_event_name, cur_event.__dict__)
        return ret


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

class TaskFailedEvent(BBEventBase):
    EVENT_NAME: str = "bb.build.TaskFailed"

    def __init__(self: "TaskFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        # TODO

    def __str__(self: "TaskFailedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class TaskProgressEvent(BBEventBase):
    EVENT_NAME: str = "bb.build.TaskProgress"

    def __init__(self: "TaskProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.progress: int = data["progress"]
        self.rate: str = data["rate"]

    def __str__(self: "TaskProgressEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

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

    def __str__(self: "TaskStartedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

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

    def __str__(self: "TaskSucceededEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class CommandCompletedEvent(BBEventBase):
    EVENT_NAME: str = "bb.command.CommandCompleted"

    def __init__(self: "CommandCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]

    def __str__(self: "CommandCompletedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class CommandFailedEvent(BBEventBase):
    EVENT_NAME: str = "bb.command.CommandFailed"

    def __init__(self: "CommandFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.error: str = data["error"]
        self.exitcode: str = data["exitcode"]

    def __str__(self: "CommandFailedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class CommandExitEvent(BBEventBase):
    EVENT_NAME: str = "bb.command.CommandExit"

    def __init__(self: "CommandExitEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        # TODO

    def __str__(self: "CommandExitEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class CacheLoadCompletedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.CacheLoadCompleted"

    def __init__(self: "CacheLoadCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.total: int = data["total"]
        self.msg: str = data["msg"]
        self.num_entries: int = data["num_entries"]

    def __str__(self: "CacheLoadCompletedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class CacheLoadProgressEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.CacheLoadProgress"

    def __init__(self: "CacheLoadProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.current: int = data["current"]
        self.total: int = data["total"]
        self.msg: str = data["msg"]

    def __str__(self: "CacheLoadProgressEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class CacheLoadStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.CacheLoadStarted"

    def __init__(self: "CacheLoadStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: str = data["pid"]
        self.msg: str = data["msg"]
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
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
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
        self.pid: int = data["pid"]
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
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]

    def __str__(self: "ConfigParsedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class DepTreeGeneratedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.DepTreeGenerated"

    def __init__(self: "DepTreeGeneratedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
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
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
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
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
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
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.processname: int = data["processname"]
        self.progress: float = data["progress"]

    def __str__(self: "ProcessProgressEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class ProcessStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.ProcessStarted"

    def __init__(self: "ProcessStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
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
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        # TODO: define more detail
        self.stamps: Mapping[str, str] = data["stamps"]

    def __str__(self: "ReachableStampsEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class RecipeParsedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.RecipeParsed"

    def __init__(self: "RecipeParsedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.fn: str = data["fn"]

    def __str__(self: "RecipeParsedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class RecipePostKeyExpansionEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.RecipePostKeyExpansion"

    def __init__(self: "RecipePostKeyExpansionEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.fn: str = data["fn"]

    def __str__(self: "RecipePostKeyExpansionEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class RecipePreFinaliseEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.RecipePreFinalise"

    def __init__(self: "RecipePreFinaliseEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.fn: str = data["fn"]

    def __str__(self: "RecipePreFinaliseEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class RecipeTaskPreProcessEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.RecipeTaskPreProcess"

    def __init__(self: "RecipeTaskPreProcessEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.fn: str = data["fn"]
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
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.model: Mapping[str, Any] = data["_model"]

    def __str__(self: "TargetsTreeGeneratedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class TreeDataPreparationCompletedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.TreeDataPreparationCompleted"

    def __init__(self: "TreeDataPreparationCompletedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.total: int = data["total"]
        self.msg: str = data["msg"]

    def __str__(self: "TreeDataPreparationCompletedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class TreeDataPreparationProgressEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.TreeDataPreparationProgress"

    def __init__(self: "TreeDataPreparationProgressEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        {'pid': 0, 'current': 1, 'total': 1, 'msg': 'Preparing tree data: 1/1'}
        self.pid: int = data["pid"]
        self.current: int = data["current"]
        self.total: int = data["total"]
        self.msg: str = data["msg"]

    def __str__(self: "TreeDataPreparationProgressEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class TreeDataPreparationStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.TreeDataPreparationStarted"

    def __init__(self: "TreeDataPreparationStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.msg: str = data["msg"]

    def __str__(self: "TreeDataPreparationStartedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class runQueueTaskFailedEvent(BBEventBase):
    EVENT_NAME: str = "bb.runqueue.runQueueTaskFailed"

    def __init__(self: "runQueueTaskFailedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        # TODO

    def __str__(self: "runQueueTaskFailedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

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

    def __str__(self: "runQueueTaskStartedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

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

    def __str__(self: "runQueueTaskSkippedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class sceneQueueCompleteEvent(BBEventBase):
    EVENT_NAME: str = "bb.runqueue.sceneQueueComplete"

    def __init__(self: "sceneQueueCompleteEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.stats: Any = data["stats"]

    def __str__(self: "sceneQueueCompleteEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

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

    def __str__(self: "runQueueTaskCompletedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class BuildInitEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.BuildInit"

    def __init__(self: "BuildInitEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.name: str = data["_name"]
        self.pkgs: List[Any] = data["_pkgs"]
        self.pid: int = data["pid"]
        self.failures: int = data["_failures"]

    def __str__(self: "BuildInitEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class BuildStartedEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.BuildStarted"

    def __init__(self: "BuildStartedEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
        self.msg: str = data["msg"]
        self.name: str = data["_name"]
        self.pkgs: List[str] = data["_pkgs"]
        self.failures: int = data["_failures"]

    def __str__(self: "BuildStartedEvent") -> str:
        """__str__

        Returns:
            str: brief description of the class
        """
        raise NotImplementedError

class HeartbeatEvent(BBEventBase):
    EVENT_NAME: str = "bb.event.HeartbeatEvent"

    def __init__(self: "HeartbeatEvent", data: Mapping[str, Any]) -> None:
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
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
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
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
        super().__init__(self.EVENT_NAME)
        self.pid: int = data["pid"]
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
        raise NotImplementedError


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