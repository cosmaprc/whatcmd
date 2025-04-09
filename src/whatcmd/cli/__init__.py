import os
import re
import sys

import click

from whatcmd.__about__ import __version__
from whatcmd.constants import CATEGORIES
from whatcmd.utils import CategoryMenu, MainMenu


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="whatcmd")
def whatcmd():
    """A command line tool to find out what command to use."""

    for category, commands in CATEGORIES.items():
        # Sort the commands in each category alphabetically
        CATEGORIES[f"{category}"] = dict(
            sorted(commands.items(), key=lambda x: x[0].lower())
        )

    # Create the main menu
    main_menu = MainMenu(CATEGORIES)

    # Create a list of CategoryMenu objects for each category
    # This will be used to store the category menus
    category_menus = []
    for category, commands in CATEGORIES.items():
        category_menu = CategoryMenu(category, commands)
        category_menus.append(category_menu)

    # This will be used to store the command selected by the user
    selected_command = None

    while not main_menu.exit:
        # Show the main menu
        main_sel = main_menu.terminal_menu.show()

        if main_sel == len(main_menu.items) - 1 or main_sel is None:
            # If the user selected "Quit" or pressed Esc, exit the program
            main_menu.exit = True
        else:
            category_menu = category_menus[main_sel]
            while not category_menu.back and not main_menu.exit:
                # Show the category menu
                cat1_sel = category_menu.terminal_menu.show()
                if (
                    cat1_sel == len(category_menu.items) - 1
                    or cat1_sel is None
                ):
                    # If the user selected "Back to Main Menu" or pressed Esc,
                    # exit the program
                    category_menu.back = True
                else:
                    selected_command = category_menu.cmd[cat1_sel]
                    # If the user selected a command, exit the main menu
                    main_menu.exit = True

            # Reset the category menu back to its initial state
            category_menu.back = False

    if selected_command is None:
        # If no command was selected, exit the program
        sys.exit(0)

    cmd_args = [
        word for word in selected_command.split() if word.startswith("${}")
    ]
    cmd_args = re.findall(r"\${.*}\$", selected_command)
    if cmd_args:
        for cmd_arg in cmd_args:
            arg_value = click.prompt(
                f"Please enter {cmd_arg} value:",
                default=cmd_arg.replace("${", "").replace("}$", ""),
            )
            click.echo(f"Value for {cmd_arg} is {arg_value}")
            selected_command = selected_command.replace(cmd_arg, arg_value)

    # Print the selected command
    click.echo(f"Executing command: {selected_command}")

    # Execute the selected command
    os.system(selected_command)
