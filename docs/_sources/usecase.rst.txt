Use case
================

This page introduce typical use cases for bbclient. Please do setup like below before each use cases.

.. code-block:: python

    import bbclient
    client: BBClient = BBClient(project_path, init_command)
    client.start_server(server_adder, server_port)
    ret = client.parse_configuration()
    ret = client.parse_files()
    # wainting for parse files
    # TODO: use client.get_event
    sleep(3)

Use cases for whole project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build package
--------------

You can build a package like below.
Please note that this command will kick all the tasks target depends, so it maybe taks so much time.

.. code-block:: python

    client.build_targets(["busybox"], "compile")
    # TODO: use client.get_event
    sleep(3600)

There are no means to notify complete task because bb.command.CommandCompleted event will occurs many times, and we can't distinguish which event notifys complete.

Get all recipes in layers
--------------------------

You can get all recipe files for every package like below.

.. code-block:: python

    ret: List[GetRecipesResult] = client.get_recipes()
    for i in ret:
        print(i.package_name)
        print(i.recipe_files)

You can also get all recipe files with version info like below.

.. code-block:: python

    ret: List[GetRecipeVersionsResult] = client.get_recipe_versions()
    for i in ret:
        print(i.recipe_file_path)
        print(i.pe)
        print(i.pv)
        print(i.pr)

There are many other commands to get all recipes in layers.

Get all recipes that inherits specific recipe
------------------------------------------------

If you want to get all recipes that inherits specific core-image.bbclass, you can do it like below.

.. code-block:: python

    ret: List[GetRecipeInheritsResult] = client.get_recipe_inherits()
    imatges = [i for i in ret if "/PATH/TO/poky/meta/classes/core-image.bbclass" in i.inherit_file_paths]
    for i in imatges:
        print(i.recipe_file_path)

Get all recipes that provides specific package
------------------------------------------------

If you want to get all recipes that provides gcc, you can do it like below.

.. code-block:: python

    ret: List[FindProvidersResult] = client.find_providers()
    imatges = [i for i in ret if "gcc" in i.package_name]
    for i in imatges:
        print(i.latest_recipe_file_path)
        print(i.latest_pe)
        print(i.latest_pv)
        print(i.latest_pr)
        print(i.latest_recipe_file_path)
        print(i.preffered_pe)
        print(i.preffered_pv)
        print(i.preffered_pr)
        print(i.preffered_recipe_file_path)
        print(i.required_version)

Get global variable
--------------------

If you want to get MACHINE variable value, you can do it like below.

.. code-block:: python
    
    ret: str = client.get_variable("MACHINE")
    print(ret)

Get all layers
---------------

If you want to get all layers, you can do it like below.

.. code-block:: python

    ret: List[GetLayerPrioritiesResult] = client.get_layer_priorities()
    for i in ret:
        print(i.name)
        print(i.path)
        print(i.priority)

If you need only layer paths, following means is also fine.

.. code-block:: python

    ret: str = client.get_variable("BBLAYERS")
    print(ret)


Generate dependency dot file
------------------------------

| You can get task-depends.dot and pn-depends file like below.
| These files will be writtene at the root of the yocto porject.

.. code-block:: python

    client.generate_dot_graph(["gcc"], "build")
    # TODO: use client.get_event
    sleep(10)

task-depends provides dependency info between recipes. See `here <https://docs.yoctoproject.org/current/dev-manual/common-tasks.html?highlight=task+depends+dot#viewing-task-variable-dependencies>`_


Use cases for one specific recipe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get one specific variable in one specific recipe
-------------------------------------------------

You can get one specific variable in one specific recipe like below.

.. code-block:: python

    data_store_index: int = client.parse_recipe_file("/PATH/TO/RECIPE/gcc_11.3.bb")
    ret: Any = client.data_store_connector_cmd(data_store_index, "getVar", "FILE")
    print(ret)


Get all variables in one specific recipe
-----------------------------------------

| bitbake IPC Interface does not provide any means to get all the variables in one specific recipe.
| Use can only get this info by bitbak -e command because this command outputs this info to stdo on the server process.

Get all appends files for one specific recipe
----------------------------------------------

Get all inherit files for one specific recipe
----------------------------------------------

Get all inherit files for one specific recipe
----------------------------------------------


Run a task
------------


Others
^^^^^^^

Set event mask
---------------

Get event
----------




