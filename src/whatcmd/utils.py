import click

from whatcmd.__about__ import __version__
from simple_term_menu import TerminalMenu
import sys
import os
import re

class MainMenu:
    def __init__(self, categories):
        """Initializes the menu with the given items."""
        self.title = "  Main Menu.\n  Press Q or Esc to quit. \n"
        self.items = [*categories.keys()] + ["Quit",]
        self.cursor = "> "
        self.cursor_style = ("fg_red", "bold")
        self.style = ("bg_red", "fg_yellow")
        self.exit = False

        self.terminal_menu = TerminalMenu(
            menu_entries=self.items,
            title=self.title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.style,
            cycle_cursor=True,
            clear_screen=True,
        )
        

class CategoryMenu:
    def __init__(self, category_name, category_commands):
        """Initializes the menu with the given items."""
        self.title = f"  {category_name}.\n  Press Q or Esc to back to main menu. \n"
        self.cmd = [*category_commands.keys()]
        max_cmd_len = max(len(cmd) for cmd in category_commands.keys())
        self.items = [*[f"{CategoryMenu.format_cmd_desc(k, v, max_cmd_len)}" for k,v in category_commands.items()]] + ["Back to Main Menu",]
        self.cursor = "> "
        self.cursor_style = ("fg_red", "bold")
        self.style = ("bg_red", "fg_yellow")
        self.exit = False
        self.back = False
        
        self.terminal_menu = TerminalMenu(
            menu_entries=self.items,
            title=self.title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.style,
            cycle_cursor=True,
            clear_screen=True,
        )

    @staticmethod
    def format_cmd_desc(cmd, description, max_key_length):
        """Formats the command and description for display."""
        return f"{cmd} {" " * (max_key_length - len(cmd))} {description}"

