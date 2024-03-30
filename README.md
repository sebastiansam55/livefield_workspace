# Live Field Workspace

Allows you to edit and sync GlobalSearch live fields from your editor of choice to GlobalSearch. 

Supports autocomplete on the `$$inject` object via jsdoc (implemented/tested in VS Code).

I strongly recommend that you stick to test environments until I've had some more time to work out any bugs. It all works but there may be some edge cases that could cause an issue etc.

## HOWTO
* Go to the releases page and download the `dev_workspace.zip` file
* Unpack and open the folder in VS Code.
* Fill out the `square9api`, `directory`, `user`, `password` and `dbid` in `config.json`
* run `livefield.exe init`
* Start editing downloaded Live Field scripts
* To Sync/Push your changes back to GlobalSearch use the Build option in VS Code (`Ctrl+Shift+B`)

Otherwise you can sync from the command line;
```
livefield.exe sync
```

### File monitor
Use the `monitor` command and it will watch for any file updates on the javascript files and save the script on file change
```
livefield.exe monitor
```

## livefield
```
usage: livefield [-h] [--config CONFIG] [--version] {mkfield,update,init,sync,ls,rm,monitor} ...

Development Workspace Tool for GlobalSearch Live Fields

positional arguments:
  {mkfield,update,init,sync,ls,rm,monitor}
                        Action to take [init|sync|ls|mkfield|rm|update|monitor]
    mkfield             Make Live Field
    update              Update a single live field
    init                Import from GlobalSearch instance
    sync                Sync workspace to server
    ls                  List Live Fields
    rm                  Delete Live Field (PERMANENT!)
    monitor             Monitor files for changes and sync automatically

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to config file, defaults to ./config.json
  --version             show program's version number and exit
```