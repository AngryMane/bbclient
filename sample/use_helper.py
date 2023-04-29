#!/usr/bin/python3

from bbclient import *

def main() -> None:
    project_path: str = "tests/dunfell"
    init_command: str = ". oe-init-build-env"
    client: BBClient = BBClient(project_path, init_command)
    if not client.start_server():
        print("bbclient command uses current path as your project path. If the parent dir of current dir isn't your project path, please use --project_path option.")
        return

    package: BBPackage = BBPackage.from_name(client, "python3")

    # you can get package information like this
    #print(package.package_name)
    #print(package.summary)
    #print(package.description)
    #print(package.license)
    #for i in package.source_uris:
    #    print(i)
    #print(package.package_epoch)
    #print(package.package_version)
    #print(package.package_revision)
    #for i in package.depends:
    #    print(i)
    #for i in package.runtime_depends:
    #    print(i)
    #for i in package.install_files:
    #    print(i)
    #for i in package.conf_files:
    #    print(i)
    #for i in package.bbclass_files:
    #    print(i)
    #for i in package.recipe_files:
    #    print(i)
    #for i in package.all_variable_names:
    #    print(i)
    #for i in package.tasks:
    #    print(i)

    # you can get any other variables like this
    #Ret: Any = package.get_var("HOMEPAGE") 
    #Print(ret)

    # you can run task like This. 
    # If you want to receive callback info, please use client.register_callback and client.unregister_callback
    #package.run_task("patch")
    #project: BBProject = BBProject(client)
    #print(project.image_packages)
    #print(project.toolchain_packages)

    networkx.nx_agraph.to_agraph(package.package_depends_graph).draw('package_depends.pdf',prog='circo')
    networkx.nx_agraph.to_agraph(package.package_runtime_depends_graph).draw('runtime_package_depends.pdf',prog='circo')
    #networkx.nx_agraph.to_agraph(package.task_depends_graph).draw('task_depends.pdf',prog='circo')
    
    client.stop_server()

if __name__ == "__main__":
    main()
