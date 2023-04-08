import os
import json
import shutil
from subprocess import PIPE, run
import sys

# global variables

GAME_DIR_PATTERN = "game"
GAME_FILE_FORMAT = ".py"
GAME_COMPILE_COMMAND = ["python3"]


def find_all_game_paths(source):
    # print("Finding all game paths")
    game_paths = []

    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                print("path: ", path)
                game_paths.append(path)

        break

    # print("done finding all game")

    return game_paths


def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)

    shutil.copytree(source, dest)


def make_json_data(path, game_dirs):
    data = {"gameNames": game_dirs, "numberOfGames": len(game_dirs)}

    with open(path, "w") as f:
        json.dump(data, f)


def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_FILE_FORMAT):
                code_file_name = file
                command = GAME_COMPILE_COMMAND + [code_file_name]
                run_command(command, path)


def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)

    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("compile result", result)

    os.chdir(cwd)


def main(source, target):
    cwd = os.getcwd()
    print("cwd: ", cwd)
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    # print("source_path: ", source_path)
    # print("target_path: ", target_path)

    game_paths = find_all_game_paths(source_path)
    new_game_dir = get_name_from_paths(game_paths, "_game")

    # print("game_path: ", game_paths)
    # print("new_game_dir: ", new_game_dir)

    create_dir(target_path)

    for src, dest in zip(game_paths, new_game_dir):
        # print("src", src)
        # print("dest", dest)
        dest_path = os.path.join(target_path, dest)
        # print("dest_path", dest_path)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)

    json_path = os.path.join(target_path, "database.json")
    make_json_data(json_path, new_game_dir)


if __name__ == "__main__":
    args = sys.argv
    # print("args:", args)
    # print("args length:", len(args))

    if len(args) != 3:
        raise Exception("You must provide a source and target file")

    source = args[1]
    target = args[2]

    # print("source: " + source)
    # print("target: " + target)

    main(source, target)
