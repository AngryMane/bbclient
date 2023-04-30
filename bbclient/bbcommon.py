#!/usr/bin/env python3
""" 
This file provides common definition for ease of understanding in/out of commands
"""

import json
from typing import Mapping, Any, List, Optional, Union, Type
from collections import namedtuple
from enum import Enum

VariableHistory = namedtuple(
    "VariableHistory",
    ["parsing", "variable", "file", "line", "op", "detail", "flag", "func"],
)


class BBFeature(Enum):
    HOB_EXTRA_CACHES = 0
    BASEDATASTORE_TRACKING = 1
    SEND_SANITYEVENTS = 2


class DataStoreFunctions(Enum):
    CREATE_COPY: str = "createCopy"
    DEL_VAR: str = "delVar"
    DEL_VAR_FLAG: str = "delVarFlag"
    DEL_VAR_FLAGS: str = "delVarFlags"
    DISABLE_TRACKING: str = "disableTracking"
    ENABLE_TRACKING: str = "enableTracking"
    EXPAND: str = "expand"
    EXPAND_VARREF: str = "expandVarref"
    EXPAND_WITH_REFS: str = "expandWithRefs"
    FINALIZE: str = "finalize"
    GET: str = "get"
    GET_VAR: str = "getVar"
    GET_VAR_FLAG: str = "getVarFlag"
    GET_VAR_FLAGS: str = "getVarFlags"
    GET_HASH: str = "get_hash"
    HAS_OVERRIDES: str = "hasOverrides"
    INITVAR: str = "initVar"
    INTERNAL_FINALIZE: str = "internal_finalize"
    ITEMS: str = "items"
    KEYS: str = "keys"
    LOCAL_KEYS: str = "localkeys"
    NEED_OVERRIDES: str = "need_overrides"
    POP: str = "pop"
    POP_ITEM: str = "popitem"
    PREPEND_VAR: str = "prependVar"
    PREPEND_VAR_FLAG: str = "prependVarFlag"
    RENAME_VAR: str = "renameVar"
    SET_VAR: str = "setVar"
    SET_VAR_FLAG: str = "setVarFlag"
    SET_VAR_FLAGS: str = "setVarFlags"
    SET_DEFAULT: str = "setdefault"
    UPDATE: str = "update"
    VALUES: str = "values"


class BBProjectNotFoundError(Exception):
    """BBProjectNotFoundError"""

    def __init__(self, project_path: str):
        self.__project_path: str = project_path
        """__project_path (str): project path provided by user"""

    def __str__(self):
        return f"bbclient failed to find bitbake library or init_script_path in project_abs_path(={self.__project_path}). init_script_path and project_abs_path were set at BBClient constructor."


class getAllKeysWithFlagsResult:
    """getAllKeysWithFlagsResult"""

    def __init__(
        self: "getAllKeysWithFlagsResult", name: str, data: Mapping[str, Any]
    ) -> None:
        self.name: str = name
        """name (str): variable name"""
        try:
            self.value: str = data["v"]
            """value (str): variable value"""
            self.histories: List[VariableHistory] = [
                self.__load_one_history(hist) for hist in data["history"]
            ]
            """histories (List[VariableHistory]): see VariableHistory."""
            self.flags: Mapping[str, str] = {
                key: value
                for key, value in data.items()
                if key != "v" and key != "history"
            }
            """flags (Mapping[str, str]): flag and value map"""
        except:
            raise Exception

    @staticmethod
    def __truncate(string, length):
        ellipsis = "..."
        return string[:length] + (ellipsis if string[length:] else "")

    @staticmethod
    def __load_one_history(hist_data: Mapping) -> VariableHistory:
        parsing = hist_data.get("parsing", None)
        variable = hist_data.get("variable", None)
        file = hist_data.get("file", None)
        line = hist_data.get("line", None)
        op = hist_data.get("op", None)
        detail = hist_data.get("detail", None)
        flag = hist_data.get("flag", None)
        func = hist_data.get("func ", None)
        error = {
            key: value
            for key, value in hist_data.items()
            if not key
            in ["parsing", "variable", "file", "line", "op", "detail", "flag", "func"]
        }
        if error:
            print(error)
        return VariableHistory(parsing, variable, file, line, op, detail, flag, func)


class GetLayerPrioritiesResult:
    """getLayerPriorities Result"""

    def __init__(self: "GetLayerPrioritiesResult", data: List[Any]) -> None:
        self.name: str = data[0]
        """name (str): layer name"""
        self.path: str = data[1]
        """path (str): layer path"""
        self.path2: str = data[2]
        """path2 (str): layer path2"""
        self.priority: int = data[3]
        """priority (int): layer priority"""


class GetRecipesResult:
    """getRecipes result"""
    def __init__(self: "GetRecipesResult", data: List[Any]) -> None:
        self.package_name: str = data[0]
        """package_name (str): package name"""
        self.recipe_files: List[str] = data[1]
        """recipe_files (List[str]): recipe file paths"""


class GetRecipeDependsResult:
    """getRecipeDepends result"""
    def __init__(self: "GetRecipeDependsResult", data: List[Any]) -> None:
        self.recipe_file_path: str = data[0]
        """recipe_file_path (str): recipe file path"""
        self.depend_package_names: List[str] = data[1]
        """depend_package_names (List[str]): package names that the recipe file depends on"""


class GetRecipeVersionsResult:
    """getRecipeVersions result"""
    def __init__(
        self: "GetRecipeVersionsResult", version: List[str], recipe_file_path: str
    ):
        self.recipe_file_path: str = recipe_file_path
        """recipe_file_path (str): recipe file path"""
        self.pe: str = version[0]
        """pe (str): package epoch"""
        self.pv: str = version[1]
        """pv (str): package version"""
        self.pr: str = version[2]
        """pr (str): package revision"""


class GetRecipeProvidesResult:
    """getRecipeProvides result"""
    def __init__(
        self: "GetRecipeProvidesResult", recipe_file_path: str, packages: List[str]
    ):
        self.recipe_file_path: str = recipe_file_path
        """recipe_file_path (str): recipe file path"""
        self.packages: List[str] = packages
        """packages (List[str]): package names that the recipe file provides"""


class GetRecipePackagesResult:
    """getRecipePackages result"""
    def __init__(
        self: "GetRecipePackagesResult", package_name: str, recipe_file_paths: List[str]
    ):
        self.package_name: str = package_name
        """package_name (str): package name"""
        self.recipe_file_paths: List[str] = recipe_file_paths
        """recipe_file_paths (List[str]): recipe file paths that provides the package"""


class GetRecipePackagesDynamicResult:
    """getRecipePackagesDynamic result"""
    def __init__(
        self: "GetRecipePackagesDynamicResult",
        dynamic_package_name: str,
        recipe_file_paths: List[str],
    ):
        self.dynamic_package_name: str = dynamic_package_name
        """dynamic_package_name (str): dynamic package name"""
        self.recipe_file_paths: List[str] = recipe_file_paths
        """recipe_file_paths (List[str]): recipe file paths that provides the dynamic package"""


class GetRProvidersResult:
    """getRProviders result"""
    def __init__(
        self: "GetRProvidersResult",
        package_alias_name: str,
        recipe_file_paths: List[str],
    ):
        self.package_alias_name: str = package_alias_name
        """package_alias_name (str): package alias name"""
        self.recipe_file_paths: List[str] = recipe_file_paths
        """recipe_file_paths (List[str]): recipe file paths that provides the alias package"""


class GetRuntimeDependsResult:
    """getRProviders result"""
    def __init__(
        self: "GetRuntimeDependsResult",
        recipe_file_path: str,
        package_depenedncy: Mapping[str, List[str]],
    ) -> None:
        self.recipe_file_path: str = recipe_file_path
        """recipe_file_path (str): recipe file path"""
        self.package_depenedncy: Mapping[str, List[str]] = package_depenedncy
        """package_depenedncy (Mapping[str, List[str]]): package names that the recipe file depends on"""


class GetRecipeInheritsResult:
    """getRecipeInherits result"""
    def __init__(
        self: "GetRecipeInheritsResult",
        recipe_file_path: str,
        inherit_file_paths: List[str],
    ) -> None:
        self.recipe_file_path: str = recipe_file_path
        """recipe_file_path (str): recipe file path"""
        self.inherit_file_paths: List[str] = inherit_file_paths
        """inherit_file_paths (List[str]): inherit recipe file paths that the recipe file inherits"""


class GetBbFilePriorityResult:
    """getBbFilePriority result"""
    def __init__(
        self: "GetBbFilePriorityResult", recipe_file_path: str, priority: int
    ) -> None:
        self.recipe_file_path: str = recipe_file_path
        """recipe_file_path (str): recipe file path"""
        self.priority: int = priority
        """priority (int): priority of the recipe file"""


class GetDefaultPreferenceResult:
    """getDefaultPreference result"""
    def __init__(
        self: "GetDefaultPreferenceResult",
        recipe_file_path: str,
        default_preference_version: int,
    ) -> None:
        self.recipe_file_path: str = recipe_file_path
        """recipe_file_path (str): recipe file path"""
        self.default_preference_version: int = default_preference_version
        """default_preference_version (int): DEFAULT_PRERENCE for the recipe file."""


class GetSkippedRecipesResult:
    """getSkippedRecipes result"""
    def __init__(
        self: "GetSkippedRecipesResult", recipe_file_path: str, data: Union[Mapping[str, Any], "SkippedPackage"]
    ) -> None:
        self.recipe_file_path: str = recipe_file_path
        """recipe_file_path (str): recipe file path"""

        if isinstance(data, dict):
            self.pn: str = data.get("pn", None)
            """pn (str): packages name"""
            self.skipreason: str = data.get("skipreason", None)
            """skipreason (str): skipreason for the recipe file."""
            self.provides: List[str] = data.get("provides", None)
            """provides (List[str]): package names provided by the recipe file"""
            self.rprovides: List[str] = data.get("rprovides", None)
            """rprovides (List[str]): package alias names provided by the recipe file"""
            return

        self.pn: str = data.pn if getattr(data, "pn") else None
        self.skipreason: str =  data.skipreason if getattr(data, "skipreason") else None
        self.provides: List[str] =  data.provides if getattr(data, "provides") else None
        self.rprovides: List[str] =  data.rprovides if getattr(data, "rprovides") else None

class GetAllAppendsResult:
    """getAllAppends result"""
    def __init__(
        self: "GetAllAppendsResult", target_recipe_name: str, append_file_path: str
    ) -> None:
        self.target_recipe_name = target_recipe_name
        """target_recipe_name (str): recipe file name"""
        self.append_file_path = append_file_path
        """append_file_path (str): append recipe file path for the recipe file name"""


class FindProvidersResult:
    """findProviders result"""
    def __init__(
        self: "FindProvidersResult",
        package_name: str,
        latest_version: List[Any],
        perffered_version: List[Any],
        required_version: Optional[bool],
    ) -> None:
        self.package_name: str = package_name
        """package_name (str): recipe file name """
        self.latest_pe: List[Any] = latest_version[0][0]
        """latest_pe (List[Any]): latest package epoch"""
        self.latest_pv: List[Any] = latest_version[0][1]
        """latest_pv (List[Any]): latest package version"""
        self.latest_pr: List[Any] = latest_version[0][2]
        """latest_pr (List[Any]): latest package revision"""
        self.latest_recipe_file_path: List[Any] = latest_version[1]
        """latest_recipe_file_path (List[Any]): latest package recipe file path"""
        self.preffered_pe: List[Any] = perffered_version[0][0]
        """preffered_pe (List[Any]): preffered package epoch"""
        self.preffered_pv: List[Any] = perffered_version[0][1]
        """preffered_pv (List[Any]): preffered package version"""
        self.preffered_pr: List[Any] = perffered_version[0][2]
        """preffered_pr (List[Any]): preffered package revision"""
        self.preffered_recipe_file_path: List[Any] = perffered_version[1]
        """preffered_recipe_file_path (List[Any]): preffered package recipe file path"""
        self.required_version: Optional[bool] = required_version
        """required_version (Optional[bool]): whether required version exists or not. If the yocto version is old, it does not support this and will be None."""


class AllProvidersResult:
    """allProviders result"""
    def __init__(
        self: "AllProvidersResult", package_name: str, recipe_file: List[Any]
    ) -> None:
        self.package_name: str = package_name
        """package_name (str): package name"""
        self.recipes: List[GetRecipeVersionsResult] = [
            GetRecipeVersionsResult(*i) for i in recipe_file
        ]
        """recipes (List[GetRecipeVersionsResult]): recipe file path and its pe, pv, pr"""


GetRuntimeRecommendsResult = GetRuntimeDependsResult

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, getAllKeysWithFlagsResult):
            return obj.__dict__
        if isinstance(obj, GetLayerPrioritiesResult):
            return obj.__dict__
        if isinstance(obj, GetRecipesResult):
            return obj.__dict__
        if isinstance(obj, GetRecipeDependsResult):
            return obj.__dict__
        if isinstance(obj, GetRecipeVersionsResult):
            return obj.__dict__
        if isinstance(obj, GetRecipeProvidesResult):
            return obj.__dict__
        if isinstance(obj, GetRecipePackagesResult):
            return obj.__dict__
        if isinstance(obj, GetRecipePackagesDynamicResult):
            return obj.__dict__
        if isinstance(obj, GetRProvidersResult):
            return obj.__dict__
        if isinstance(obj, GetRuntimeDependsResult):
            return obj.__dict__
        if isinstance(obj, GetRuntimeRecommendsResult):
            return obj.__dict__
        if isinstance(obj, GetRecipeInheritsResult):
            return obj.__dict__
        if isinstance(obj, GetBbFilePriorityResult):
            return obj.__dict__
        if isinstance(obj, GetDefaultPreferenceResult):
            return obj.__dict__
        if isinstance(obj, GetSkippedRecipesResult):
            return obj.__dict__
        if isinstance(obj, GetAllAppendsResult):
            return obj.__dict__
        if isinstance(obj, FindProvidersResult):
            return obj.__dict__
        if isinstance(obj, AllProvidersResult):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
