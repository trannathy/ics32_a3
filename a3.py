# a3.py

# THY TRAN
# THYNT1@UCI.EDU
# 90526048

import ds_client
import ds_protocol

from Profile import *
import ui
import file_commands

import shlex
import os
from pathlib import Path


def create_file(command_line: list, admin) -> None:

    DIRECTORY = Path(command_line[1])
    FILE_NAME = Path(command_line[3] + ".dsu")

    p = DIRECTORY / FILE_NAME

    if p.exists():
        print(ui.OUTPUT_FILE_EXISTS)
        new_path = str(p)

        new_command_line = ["O", new_path]

        open_file(new_command_line, admin)

    else:
        try:
            p.touch()
            p.unlink()

        except FileNotFoundError:
            print(ui.OUTPUT_NO_PATH)

        else:
            new_username, new_password, new_bio = profile_set_up(admin)

            new_profile = Profile(dsuserver="168.235.86.101", username=new_username,
                                  password=new_password)
            new_profile.bio = new_bio

            p.touch()
            print(f"\n{str(p)} CREATED\n")
            new_profile.save_profile(p)

            open_file(["O", str(p)], admin)


def open_file(command_line, admin) -> None:
    if check_dsu(command_line):
        p = Path(command_line[-1])

        if p.exists():
            try:
                with open(p, "a+") as f:
                    print(f"\n{str(p)} SUCESSFULLY LOADED\n")

                    file_commands.file_run(str(p), admin)

                print(f"\n{str(p)} CLOSED\n")

            except PermissionError:
                print(ui.OUTPUT_NO_PERM)

        else:
            print(ui.OUTPUT_NO_PATH)

    else:
        print(ui.OUTPUT_NOT_DSU)


def delete_file(command_line) -> None:
    if check_dsu(command_line):
        p = Path(command_line[-1])

        try:
            p.unlink()
            print(f"\n{p} DELETED\n")

        except PermissionError:
            print(ui.OUTPUT_NO_PERM)
    else:
        print(ui.OUTPUT_NOT_DSU)


def read_file(command_line):

    if not check_dsu(command_line):
        print(ui.OUTPUT_NOT_DSU)

    else:
        try:
            p = Path(command_line[-1])

            if os.path.getsize(p) == 0:
                print('EMPTY')

            else:
                print(p.read_text())

        except PermissionError:
            print(ui.OUTPUT_NO_PERM)


def command_intake(mode) -> str:

    user_input = input(ui.command_intake_ui(mode))
    return user_input


def profile_set_up(mode) -> tuple:
    user = ""
    while file_commands.check_empty(user):
        user = input(ui.set_new_profile("username", mode))

    pwd = ""

    while file_commands.check_empty(pwd):
        pwd = input(ui.set_new_profile("password", mode))

    bio = input(ui.set_new_profile("bio", mode))

    return user, pwd, bio


def check_validity(command_line):

    if command_line[0] in ['D', 'R', 'O'] and len(command_line) == 2:
        return True

    elif command_line[0] in ['D', 'R', 'O'] and len(command_line) != 2:
        print(ui.OUTPUT_D_R_O_USE)
        return False

    elif (command_line[0] == 'C' and len(command_line) == 4 and
            command_line[2] == "-n"):
        return True

    elif command_line[0] == 'C' and (len(command_line) != 4 or
                                     command_line[2] != "-n"):
        print(ui.OUTPUT_C_USE)
        return False

    else:
        print(ui.OUTPUT_COMMAND_INVALID)
        return False


def check_path(command_line):

    p = Path(command_line[1])

    if not p.exists():
        print(ui.OUTPUT_NO_PATH)
        return False

    else:
        return True


def check_dsu(command_line: list[str]):

    file_type = (command_line[-1].split('.'))[-1]

    if file_type == "dsu":
        return True

    else:
        return False


def run(mode: bool):
    user_command = command_intake(mode)

    if user_command == 'admin':
        run(not mode)

    elif user_command != "Q":

        try:
            user_command = shlex.split(user_command)

        except ValueError:
            print(ui.OUTPUT_COMMAND_INVALID)
            run(mode)

        else:

            if (check_validity(user_command) is False or
                    check_path(user_command) is False):
                pass

            elif user_command[0] == 'C':
                create_file(user_command, mode)

            elif user_command[0] == 'O':
                open_file(user_command, mode)

            elif user_command[0] == 'D':
                delete_file(user_command)

            elif user_command[0] == 'R':
                read_file(user_command)

            run(mode)


if __name__ == "__main__":
    ui.welcome()
    run(False)
