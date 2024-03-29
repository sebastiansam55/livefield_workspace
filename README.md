# Live Field Workspace

Allows you to edit and sync GlobalSearch live fields from your editor of choice to GlobalSearch. 

Supports autocomplete on the `$$inject` object.

## HOWTO
* Go to the releases page and download the version appropriate for you platform.
* Unpack and open the folder in VS Code.
* Copy the `ex_config.json` to `config.json`
* Fill out the `square9api`, `directory`, `user`, `password` and `dbid`
* run `src/dist/livefield init`
* Start editing downloaded Live Field scripts

If you're using VS Code you should be able to complete a sync by running a build (Ctrl+Shift+B)

Otherwise you can sync from the command line;
```
src/dist/livefield sync
```