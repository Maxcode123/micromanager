# micromanager

CLI application to manage microservices with docker-compose

Built with [Typer](https://typer.tiangolo.com/)

`micromanager` is a wrapper around compose, it allows you to define and manage multiple
systems, each with a multitude of compose projects.

## Documentation

The documentation for `micromanager` is hosted on [maxcode123.github.io/micromanager/](https://maxcode123.github.io/micromanager/)

## Installation

```bash
pip install compose-micromanager
```

Run `micromanager --help` to make sure you've successfully installed micromanager.

## Quick start

After you've installed `micromanager` you'd want to create a configuration file at
`$HOME/.config/micromanager/config.json`:

```bash
mkdir -p $HOME/.config/micromanager/
touch $HOME/.config/micromanager/config.json
```

Edit the `config.json` file as per your needs.  
You can consult the [config.json.example](config.json.example) file to understand the format.

Once you're done with the configuration you can run `micromanager --help` to
see all the available commands.
