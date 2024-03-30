# Setup instructions
* Download and unpack dev_workspace.zip
* Update the `square9api`,`username`,`password` and `dbid` values in `config.json`
* In VS Code use the "open folder" option to open the unpack folder
* Open the VS Code terminal (`Ctrl+Shift+~`)
* Run `livefield[.exe] init` (add or remove .exe depending on platform)
* This will download and create files for each of the Live Fields in the GlobalSearch database. 
* If you have a live field that is using the GET type functionality you can edit this in the "config.json" file
* Edit script/config.json values as needed.
* To push your changes back to the server use "build" command in VS Code (`Ctrl+Shift+B`)
    * alternately you can run `livefield[.exe] sync`
    * or you can activate `livefield[.exe] monitor` mode.
    * this will run and watch the files, when updated it will sync them
