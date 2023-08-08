#!/usr/bin/python3

from bbclient import *

def main() -> None:
    project_path: str = "tests/dunfell"
    init_command: str = ". oe-init-build-env"
    client: BBClient = BBClient(project_path, init_command)
    if not client.start_server():
        print(f"bbclient uses project_path(={project_path}) as your project path, but this project_path doesn't seem to include bitbake/lib dir.")
        return

    # project
    project: BBProject = BBProject(client)
    print(project.layers)
    print(project.packages)
    print(project.image_packages)
    print(project.toolchain_packages)

    # package from recipe file path
    llvm_package_names = BBPackage.get_package_names_from_recipe_file(client, "/home/yosuke/work/git/bbclient/tests/dunfell/meta/recipes-devtools/llvm/llvm_git.bb")
    llvm_package: BBPackage = BBPackage.from_name(client, llvm_package_names[0])
    print_package_info(llvm_package)

    # you can get any other variables like this
    #Ret: Any = package.get_var("HOMEPAGE") 
    #Print(ret)

    # you can run task like This. 
    # If you want to receive callback info, please use client.register_callback and client.unregister_callback
    #package.run_task("patch")
    #project: BBProject = BBProject(client)
    #print(project.image_packages)
    #print(project.toolchain_packages)

    #networkx.nx_agraph.to_agraph(package.package_depends_graph).draw('package_depends.pdf',prog='circo')
    #networkx.nx_agraph.to_agraph(package.package_runtime_depends_graph).draw('runtime_package_depends.pdf',prog='circo')
    #networkx.nx_agraph.to_agraph(package.task_depends_graph).draw('task_depends.pdf',prog='circo')
    
    client.stop_server()

def print_package_info(package: BBPackage) -> None:
    # you can get package information like this
    print(package.package_name)
    print(package.summary)
    print(package.description)
    print(package.license)
    for i in package.source_uris:
        print(i)
    print(package.package_epoch)
    print(package.package_version)
    print(package.package_revision)
    for i in package.package_depends:
        print(i)
    for i in package.package_runtime_depends:
        print(i)
    for i in package.install_files:
        print(i)
    for i in package.conf_files:
        print(i)
    for i in package.bbclass_files:
        print(i)
    for i in package.recipe_files:
        print(i)
    for i in package.all_variable_names:
        print(i)
    for i in package.tasks:
        print(i)

    # you can get any other variables like this
    ret: Any = package.get_var("HOMEPAGE") 
    print(ret)

    # you can run task like This. 
    # If you want to receive callback info, please use client.register_callback and client.unregister_callback
    # package.run_task("patch")

    # you can output dependency graph.
    # networkx.nx_agraph.to_agraph(package.package_depends_graph).draw('package_depends.pdf',prog='circo')
    # networkx.nx_agraph.to_agraph(package.package_runtime_depends_graph).draw('runtime_package_depends.pdf',prog='circo')
    # networkx.nx_agraph.to_agraph(package.task_depends_graph).draw('task_depends.pdf',prog='circo')

if __name__ == "__main__":
    main()
