# THY TRAN
# THYNT1@UCI.EDU
# 90526048

import ui
import Profile
import ds_client
import shlex

HOST = "168.235.86.101"
PORT = 3021

class Editing:

    def __init__(self, attribute, attribute_edit, profile_path):

        self.attribute = attribute
        self.attribute_edit = attribute_edit
        self.profile_path = profile_path

    def make_edit(self) -> None:

        profile = Profile.Profile()
        profile.load_profile(self.profile_path)

        if self.attribute == "USERNAME":
            old_attribute = profile.username
            profile.username = self.attribute_edit

        elif self.attribute == "PASSWORD":
            old_attribute = profile.password
            profile.password = self.attribute_edit

        elif self.attribute == "BIO":
            old_attribute = profile.bio
            profile.bio = self.attribute_edit

        if old_attribute == self.attribute_edit:
            print(f"{self.attribute} IS ALREADY {self.attribute_edit}" +
                  "\nNO CHANGE MADE\n")

        else:
            print(f"OLD {self.attribute}: {old_attribute}")
            print(f"NEW {self.attribute}: {self.attribute_edit}\n")

        profile.save_profile(self.profile_path)


def check_id(id: str) -> bool:

    try:
        int_id = int(id)
        if int_id < 0:
            print(ui.OUTPUT_ID_NEGATIVE)
            return False
        else:
            return True

    except ValueError:
        print(ui.OUTPUT_ID_INVALID)
        return False


def edit_command_intake(path: str, mode: bool) -> str:

    user_input = input(ui.opened_file_ui(path, mode))
    return user_input


def edit_command_check_validity(command_line) -> bool:

    option_list = ["-usr", "-pwd", "-bio", "-addpost", "-delpost"]
    options = command_line[1:]
    valid_command = True

    if len(options) == 0:
        print(ui.OUTPUT_E_USE)
        valid_command = False

    for index, option in enumerate(options):
        if (index % 2 == 0) and (option not in option_list):
            valid_command = False
            print(ui.OUTPUT_E_OPTION_INVALID)
            break

        if (index % 2 == 0) and option == "-delpost":
            valid_command = check_id(options[index + 1])
            if valid_command is False:
                break

    return valid_command


def print_command_check_validity(command_line) -> bool:

    option_list = ["-usr", "-pwd", "-bio", "-posts", "-post", "-all"]
    options = command_line[1:]
    valid_command = True

    if options[-1] == "-post":
        print(ui.OUTPUT_POST_USE)
        return False

    for index, option in enumerate(options):
        if option not in option_list and options[index - 1] == "-post":
            valid_command = check_id(option)
            if valid_command is False:
                break

        elif option not in option_list and options[index - 1] != "-post":
            valid_command = False
            print(ui.OUTPUT_COMMAND_INVALID)
            break

    return valid_command


def publish_command_check_validity(command_line) -> bool:
    return check_id(command_line[1])


def file_check_validity(command_line) -> bool:

    if command_line[0] == "E" and len(command_line) % 2 == 1:
        return edit_command_check_validity(command_line)

    elif command_line[0] == "P" and len(command_line) > 1:
        return print_command_check_validity(command_line)
    
    elif command_line[0] == "PUB_POST" and len(command_line) == 2:
        return publish_command_check_validity(command_line)
    
    elif command_line[0] == "PUB_BIO" and len(command_line) == 1:
        return True

    else:
        print(ui.OUTPUT_COMMAND_INVALID)
        return False


def get_edits(command_line):

    options = command_line[1:]

    commands = []
    edits = []

    for ind, command in enumerate(options):
        if ind % 2 == 0 and (command not in commands or command == "-addpost"):
            commands.append(command)

        elif ind % 2 == 0 and command in commands:
            print(f"{ui.OUTPUT_DUPLICATE} {command}\n")
            prev_command_ind = commands.index(command)
            commands.remove(command)
            edits.remove(edits[prev_command_ind])
            commands.append(command)

        else:
            edits.append(command)

    return commands, edits


def check_empty(input: str) -> bool:
    if input.strip() == "":
        return True
    else:
        return False


def edit_user(new_user, dsu_path):

    username_edit = Editing("USERNAME", new_user, dsu_path)
    username_edit.make_edit()


def edit_pwd(new_pwd, dsu_path):

    password_edit = Editing("PASSWORD", new_pwd, dsu_path)
    password_edit.make_edit()


def edit_bio(new_bio, dsu_path):

    bio_edit = Editing("BIO", new_bio, dsu_path)
    bio_edit.make_edit()


def edit_addpost(new_entry, dsu_path):

    new_post = Profile.Post()
    new_post.set_entry(new_entry)

    profile = Profile.Profile()
    profile.load_profile(dsu_path)

    profile.add_post(new_post)
    all_posts = profile.get_posts()
    id = len(all_posts) - 1

    print("NEW POST SUCCESSFULLY ADDED:")
    print_post(all_posts, id)

    profile.save_profile(dsu_path)


def edit_delpost(post_to_delete: int, dsu_path: str):

    profile = Profile.Profile()
    profile.load_profile(dsu_path)

    deletion = profile.del_post(post_to_delete)

    if deletion:
        print(f"\nPOST {post_to_delete} DELETED\n")
        profile.save_profile(dsu_path)

    else:
        print("POST ID INVALID")


def get_prints(command_line):

    command_list = ["-usr", "-pwd", "-bio", "-posts", "-post", "-all"]

    command_line = command_line[1:]

    all_commands = []
    id = None

    for index, command in enumerate(command_line):

        if command in command_list:
            all_commands.append(command)

        elif command_list[index - 1] in command_list:
            id = int(command)

    return all_commands, id


def print_all_posts(posts: list[Profile.Post]):

    if len(posts) == 0:
        print("NO POSTS")

    else:
        for i in range(len(posts)):
            print_post(posts, i)
            i += 1


def print_post(posts: list[Profile.Post], id: int):

    print("\nID: " + str(id))
    print("ENTRY:")
    print(posts[id].get_entry())
    print("TIMESTAMP:")
    print(str(posts[id].get_time()) + "\n")


def edit_file(command_list: list[str], path: str, mode: bool):

    attributes, new_att = get_edits(command_list)

    for index, attribute in enumerate(attributes):
        if check_empty(new_att[index]):
            print(f"\n{attribute} {ui.OUTPUT_EMPTY_COMMAND}")

        elif attribute == "-usr":
            edit_user(new_att[index], path)

        elif attribute == "-pwd":
            edit_pwd(new_att[index], path)

        elif attribute == "-bio":
            edit_bio(new_att[index], path)

        elif attribute == "-addpost":
            edit_addpost(new_att[index], path)

        elif attribute == "-delpost":
            edit_delpost(int(new_att[index]), path)


def print_file(command_list: list[str], path: str, mode: bool):

    commands_raw, read_id = get_prints(command_list)

    prof = Profile.Profile()
    prof.load_profile(path)

    if "-all" in commands_raw:
        commands = ["-usr", "-pwd", "-bio", "-posts"]

    else:
        commands = []

        for command in commands_raw:
            if command not in commands:
                commands.append(command)

    posts_list = prof.get_posts()

    if read_id is not None and read_id > (len(posts_list) - 1):
        print(ui.OUTPUT_INDEX_ERROR)

    else:
        for command in commands:
            if command == "-usr":
                print(f"USERNAME: {prof.username}")

            elif command == "-pwd":
                print(f"PASSWORD: {prof.password}")

            elif command == "-bio":
                print(f"BIO: {prof.bio}")

            elif command == "-posts":
                print_all_posts(posts_list)

            elif command == "-post":
                print_post(posts_list, read_id)


def publish_post(command_list: list[str], path: str):
    
    prof = Profile.Profile()
    prof.load_profile(path)

    posts_list = prof.get_posts()

    id = int(command_list[1])

    post_to_pub = posts_list[id].get_entry()

    send_sucess = ds_client.send(HOST, PORT, prof.username, prof.password, post_to_pub)


def publish_bio(command_list: list[str], path: str):
    prof = Profile.Profile()
    prof.load_profile(path)

    send_sucess = ds_client.send(HOST, PORT, prof.username, prof.password, "", prof.bio)

    print(send_sucess)


def file_run(path: str, mode: bool):

    file_command = edit_command_intake(path, mode)

    if file_command.strip() != "CL":

        try:
            file_command = shlex.split(file_command)

        except ValueError:
            print(ui.OUTPUT_COMMAND_INVALID)
            file_run(path, mode)

        else:
            if file_check_validity(file_command) is False:
                pass

            elif file_command[0] == "E":
                edit_file(file_command, path, mode)

            elif file_command[0] == "P":
                print_file(file_command, path, mode)

            elif file_command[0] == "PUB_POST":
                publish_post(file_command, path)
            
            elif file_command[0] == "PUB_BIO":
                publish_bio(file_command, path)
            
            file_run(path, mode)
