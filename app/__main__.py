from app import cli, __app_name__

import typer

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()