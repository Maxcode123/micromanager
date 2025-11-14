# Installation

You'll need Python installed to install `micromanager`.

## pipx (recommended)

You can find instructions on how to install pipx [here](https://github.com/pypa/pipx)  

```sh
pipx install compose-micromanager
```

The above command should install the `micromanager` executable in your environment.  
Try it out by running `micromanager` in the terminal:

```sh
> micromanager
Usage: micromanager [OPTIONS] COMMAND [ARGS]...                                                                                                                                              
                                                                                                                                                                                              
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                    │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                             │
│ --help                        Show this message and exit.                                                                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ start     Start the given projects by running compose up. If the projects argument is empty, starts all projects of the current system.                                                    │
│ use       Set the given system as your current working system.                                                                                                                             │
│ config    Display the current configuration.                                                                                                                                               │
│ stop      Stop the given projects by running compose down. If the projects argument is empty, stops all projects of the current system.                                                    │
│ status    Print the status of all configured projects in the current system.                                                                                                               │
│ restart   Restart the given projects by running compose restart. If the projects argument is empty, restarts all projects of the current system.                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## pip

It is recommended to use virtual environments when installing Python packages. If
you're not sure how to use them, opt for the first option (pipx).  
If you want to know more about virtual environments you can read [this](https://docs.astral.sh/uv/pip/environments/).  

```sh
pip install compose-micromanager
```

The above will install the `micromanager` executable in your current
Python environment.  
To validate that micromanager is installed you have to activate the environment in which micromanager is installed and run `micromanager`.  

```sh
> micromanager
Usage: micromanager [OPTIONS] COMMAND [ARGS]...                                                                                                                                              
                                                                                                                                                                                              
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                    │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                             │
│ --help                        Show this message and exit.                                                                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ start     Start the given projects by running compose up. If the projects argument is empty, starts all projects of the current system.                                                    │
│ use       Set the given system as your current working system.                                                                                                                             │
│ config    Display the current configuration.                                                                                                                                               │
│ stop      Stop the given projects by running compose down. If the projects argument is empty, stops all projects of the current system.                                                    │
│ status    Print the status of all configured projects in the current system.                                                                                                               │
│ restart   Restart the given projects by running compose restart. If the projects argument is empty, restarts all projects of the current system.                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
