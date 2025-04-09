.ONESHELL:
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make install"
	@echo "  make uninstall"

SHELL := /bin/bash
VENV_NAME := whatcmd
VENV_DIR := ~/.virtualenvs
VENV_DIR_NAME := $(VENV_DIR)/$(VENV_NAME)
VENV_BIN_DIR := $(VENV_DIR_NAME)/bin
VENV_PYTHON := $(VENV_BIN_DIR)/python
VENV_PIP := $(VENV_BIN_DIR)/pip
VENV_ACTIVATE	:= $(VENV_BIN_DIR)/activate
VENV_REQUIREMENTS := requirements.txt

define create-venv
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV_DIR_NAME)
endef

define activate-venv
	@echo "Activating virtual environment..."
	@source $(VENV_ACTIVATE)
	@echo "Virtual environment $(VENV_NAME) is ready to use."
endef

define venv-upgrade-pip
	@echo "Upgrading pip..."
	@$(VENV_PIP) install --upgrade pip
	@echo "Pip upgraded to the latest version."
endef

define venv-install-pre-commit
	@echo "Installing pre-commit hooks..."
	@$(VENV_PIP) install pre-commit
	@$(VENV_PIP) install --upgrade pre-commit
	@pre-commit install
	@pre-commit autoupdate
	@echo "Pre-commit hooks installed."
endef

define venv-install-requirements
	@echo "Installing requirements..."
	@$(VENV_PIP) install -r $(VENV_REQUIREMENTS)
	@echo "Requirements installed."
endef

define pip-install
	@echo "Installing app..."
	@$(VENV_PIP) install -e .
	@echo "App installed."
endef

define deactivate-venv
	@echo "Deactivating virtual environment..."
	@deactivate
	@echo "Virtual environment $(VENV_NAME) has been deactivated."
endef

define uninstall-venv
	@echo "Uninstalling virtual environment..."
	@rm -rf $(VENV_DIR_NAME)
	@echo "Virtual environment $(VENV_NAME) has been removed."
endef

install:
	@$(shell read -p "Please ensure python3 is installed and available in your PATH. Press enter to continue...")
	@${create-venv}
	@${activate-venv}
	@${venv-upgrade-pip}
	@${venv-install-pre-commit}
	@${venv-install-requirements}
	@${pip-install}
	@${deactivate-venv}
	@echo "******** Installation complete ********"
	@echo "To activate the virtual environment, run:"
	@echo "source $(VENV_ACTIVATE)"
	@echo "To deactivate the virtual environment, run:"
	@echo "deactivate"
	@echo "To uninstall the virtual environment, run:"
	@echo "make uninstall"
	@echo "To run the pre-commit hooks, run:"
	@echo "pre-commit run --all-files"
	@echo "To run the pre-commit hooks on a specific file, run:"
	@echo "pre-commit run --all-files <file>"

uninstall:
	@${deactivate-venv}
	@${uninstall-venv}
