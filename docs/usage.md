# Usage

## Configuration

`micromanager` uses a configuration file that is located at
`$HOME/.config/micromanager/config.json`. The configuration file defines the
systems to be managed.  
The expected schema of the configuration file is as follows:

```json
{
  "systems": {
    "system-name-1": {
      "default": "true",
      "projects": {
        "project-name-1": {"compose_file_path": "path/to/compose/file"},
        "project-name-2": {"compose_file_path": "path/to/compose/file"}
      }
    },
    "system-name-2": {
      "projects": {
        "project-name-3": {"compose_file_path": "path/to/compose/file"}
      }
    }
  }
}
```

If only one system is defined, then that is regarded as the default. If multiple
systems are defined however, one must be assigned to be the default.

## Commands

### start

```sh
micromanager start [PROJECTS]
```

Start the given projects by running compose up. If the projects argument is empty
starts all projects of the current system.

### use

```sh
micromanager use SYSTEM
```

Set the given system as your current working system.

### config

```sh
micromanager config
```

Display the current configuration.

### stop

```sh
micromanager stop [PROJECTS]
```

Stop the given projects by running compose down. If the projects argument is empty,
stops all projects of the current system.

### status

```sh
micromanager status
```

Print the status of all configured projects in the current system.

```sh
micromanager restart
```

Restart the given projects by running compose restart. If the projects argument
is empty, restarts all projects of the current system.
