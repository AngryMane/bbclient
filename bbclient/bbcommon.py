#!/usr/bin/env python3
""" 
This file provides common definition for ease of understanding in/out of commands
"""

import json
from typing import Mapping, Any, List, Optional
from collections import namedtuple
from enum import Enum

VariableHistory = namedtuple(
    "VariableHistory",
    ["parsing", "variable", "file", "line", "op", "detail", "flag", "func"],
)


class getAllKeysWithFlagsResult:
    """getAllKeysWithFlagsResult

    Attributes:
        name (str): variable name
        value (str): variable value
        histories (List[VariableHistory]): see VariableHistory.
        flags (Mapping[str, str]): flag and value map
    """

    def __init__(
        self: "getAllKeysWithFlagsResult", name: str, data: Mapping[str, Any]
    ) -> None:
        self.name: str = name

        try:
            self.value: str = data["v"]
            self.histories: List[VariableHistory] = [
                self.__load_one_history(hist) for hist in data["history"]
            ]
            self.flags: Mapping[str, str] = {
                key: value
                for key, value in data.items()
                if key != "v" and key != "history"
            }
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


class BBFeature(Enum):
    HOB_EXTRA_CACHES = 0
    BASEDATASTORE_TRACKING = 1
    SEND_SANITYEVENTS = 2


class GetLayerPrioritiesResult:
    """getLayerPriorities Result

    Attributes:
        name (str): variable name
        path (str): variable value
        path2 (str): variable value
        priority (int): see VariableHistory.
    """

    def __init__(self: "GetLayerPrioritiesResult", data: List[Any]) -> None:
        self.name: str = data[0]
        self.path: str = data[1]
        self.path2: str = data[2]
        self.priority: int = data[3]


class GetRecipesResult:
    """getRecipes result

    Attributes:
        package_name (str): package name
        recipe_files (List[str]): recipe file paths
    """
    def __init__(self: "GetRecipesResult", data: List[Any]) -> None:
        self.package_name: str = data[0]
        self.recipe_files: List[str] = data[1]


class GetRecipeDependsResult:
    """getRecipeDepends result

    Attributes:
        recipe_file_path (str): recipe file path
        depend_package_names (List[str]): package names that the recipe file depends on
    """
    def __init__(self: "GetRecipeDependsResult", data: List[Any]) -> None:
        self.recipe_file_path: str = data[0]
        self.depend_package_names: List[str] = data[1]


class GetRecipeVersionsResult:
    """getRecipeVersions result

    Attributes:
        recipe_file_path (str): recipe file path
        pe (str): package epoch
        pv (str): package version
        pr (str): package revision
    """
    def __init__(
        self: "GetRecipeVersionsResult", version: List[str], recipe_file_path: str
    ):
        self.recipe_file_path: str = recipe_file_path
        self.pe: str = version[0]
        self.pv: str = version[1]
        self.pr: str = version[2]


class GetRecipeProvidesResult:
    """getRecipeProvides result

    Attributes:
        recipe_file_path (str): recipe file path
        packages (List[str]): package names that the recipe file provides
    """
    def __init__(
        self: "GetRecipeProvidesResult", recipe_file_path: str, packages: List[str]
    ):
        self.recipe_file_path: str = recipe_file_path
        self.packages: List[str] = packages


class GetRecipePackagesResult:
    """getRecipePackages result

    Attributes:
        package_name (str): package name 
        recipe_file_paths (List[str]): recipe file paths that provides the package
    """
    def __init__(
        self: "GetRecipePackagesResult", package_name: str, recipe_file_paths: List[str]
    ):
        self.package_name: str = package_name
        self.recipe_file_paths: List[str] = recipe_file_paths


class GetRecipePackagesDynamicResult:
    """getRecipePackagesDynamic result

    Attributes:
        dynamic_package_name (str): dynamic package name 
        recipe_file_paths (List[str]): recipe file paths that provides the dynamic package
    """
    def __init__(
        self: "GetRecipePackagesDynamicResult",
        dynamic_package_name: str,
        recipe_file_paths: List[str],
    ):
        self.dynamic_package_name: str = dynamic_package_name
        self.recipe_file_paths: List[str] = recipe_file_paths


class GetRProvidersResult:
    """getRProviders result

    Attributes:
        package_alias_name (str): package alias name 
        recipe_file_paths (List[str]): recipe file paths that provides the alias package 
    """
    def __init__(
        self: "GetRProvidersResult",
        package_alias_name: str,
        recipe_file_paths: List[str],
    ):
        self.package_alias_name: str = package_alias_name
        self.recipe_file_paths: List[str] = recipe_file_paths


class GetRuntimeDependsResult:
    """getRProviders result

    Attributes:
        recipe_file_path (str): recipe file path 
        package_depenedncy (Mapping[str, List[str]]): package names that the recipe file depends on
    """
    def __init__(
        self: "GetRuntimeDependsResult",
        recipe_file_path: str,
        package_depenedncy: Mapping[str, List[str]],
    ) -> None:
        self.recipe_file_path: str = recipe_file_path
        self.package_depenedncy: Mapping[str, List[str]] = package_depenedncy


class GetRecipeInheritsResult:
    """getRecipeInherits result

    Attributes:
        recipe_file_path (str): recipe file path 
        inherit_file_paths (List[str]): inherit recipe file paths that the recipe file inherits
    """
    def __init__(
        self: "GetRecipeInheritsResult",
        recipe_file_path: str,
        inherit_file_paths: List[str],
    ) -> None:
        self.recipe_file_path: str = recipe_file_path
        self.inherit_file_paths: List[str] = inherit_file_paths


class GetBbFilePriorityResult:
    """getBbFilePriority result

    Attributes:
        recipe_file_path (str): recipe file path 
        priority (int): priority of the recipe file
    """
    def __init__(
        self: "GetBbFilePriorityResult", recipe_file_path: str, priority: int
    ) -> None:
        self.recipe_file_path: str = recipe_file_path
        self.priority: int = priority


class GetDefaultPreferenceResult:
    """getDefaultPreference result

    Attributes:
        recipe_file_path (str): recipe file path 
        default_preference_version (int): DEFAULT_PRERENCE for the recipe file.
    """
    def __init__(
        self: "GetDefaultPreferenceResult",
        recipe_file_path: str,
        default_preference_version: int,
    ) -> None:
        self.recipe_file_path: str = recipe_file_path
        self.default_preference_version: int = default_preference_version


class GetSkippedRecipesResult:
    """getSkippedRecipes result

    Attributes:
        recipe_file_path (str): recipe file path 
        pn (str): packages name 
        skipreason (str): skipreason for the recipe file.
        provides (List[str]): package names provided by the recipe file 
        rprovides (List[str]): package alias names provided by the recipe file
    """
    def __init__(
        self: "GetSkippedRecipesResult", recipe_file_path: str, data: Mapping[str, Any]
    ) -> None:
        self.recipe_file_path: str = recipe_file_path
        self.pn: str = data.get("pn", None)
        self.skipreason: str = data.get("skipreason", None)
        self.provides: List[str] = data.get("provides", None)
        self.rprovides: List[str] = data.get("rprovides", None)


class GetAllAppendsResult:
    """getAllAppends result

    Attributes:
        target_recipe_name (str): recipe file name 
        append_file_path (str): append recipe file path for the recipe file name
    """
    def __init__(
        self: "GetAllAppendsResult", target_recipe_name: str, append_file_path: str
    ) -> None:
        self.target_recipe_name = target_recipe_name
        self.append_file_path = append_file_path


class FindProvidersResult:
    """findProviders result

    Attributes:
        package_name (str): recipe file name 
        latest_pe (List[Any]): latest package epoch
        latest_pv (List[Any]): latest package version
        latest_pr (List[Any]): latest package revision
        latest_recipe_file_path (List[Any]): latest package recipe file path
        preffered_pe (List[Any]): preffered package epoch
        preffered_pv (List[Any]): preffered package version
        preffered_pr (List[Any]): preffered package revision
        preffered_recipe_file_path (List[Any]): preffered package recipe file path
        required_version (Optional[bool]): whether required version exists or not. If the yocto version is old, it does not support this and will be None.
    """
    def __init__(
        self: "FindProvidersResult",
        package_name: str,
        latest_version: List[Any],
        perffered_version: List[Any],
        required_version: Optional[bool],
    ) -> None:
        self.package_name: str = package_name
        self.latest_pe: List[Any] = latest_version[0][0]
        self.latest_pv: List[Any] = latest_version[0][1]
        self.latest_pr: List[Any] = latest_version[0][2]
        self.latest_recipe_file_path: List[Any] = latest_version[1]
        self.preffered_pe: List[Any] = perffered_version[0][0]
        self.preffered_pv: List[Any] = perffered_version[0][1]
        self.preffered_pr: List[Any] = perffered_version[0][2]
        self.preffered_recipe_file_path: List[Any] = perffered_version[1]
        self.required_version: Optional[bool] = required_version


class AllProvidersResult:
    """allProviders result

    Attributes:
        package_name (str): package name
        recipes (List[GetRecipeVersionsResult]): recipe file path and its pe, pv, pr
    """
    def __init__(
        self: "AllProvidersResult", package_name: str, recipe_file: List[Any]
    ) -> None:
        self.package_name: str = package_name
        self.recipes: List[GetRecipeVersionsResult] = [
            GetRecipeVersionsResult(*i) for i in recipe_file
        ]


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
