import os
import sys
import errno
import shutil


def parse_arguments(args: list[str]) -> object:
    """
    Function that take a list of string, and send an object
    ordered by it flags
    """
    main_path = os.path.join('src/')
    dest_path = os.path.join('build/')
    default_arguments = {
        'main_file': os.path.join(main_path, 'App.java'),
        'dest_path': os.path.join(main_path, 'App'),
    }

    # Not flag main
    if not '--main' in args:
        return default_arguments

    file_index = args.index('--main') + 1

    # Not enough arguments
    if file_index >= len(args):
        return default_arguments

    # Not valid file extension
    if not args[file_index].endswith('.java'):
        return default_arguments

    dest_file = args[file_index].replace('.java', '')

    return {
        'main_file': os.path.join(main_path, args[file_index]),
        'dest_file': os.path.join(dest_path, dest_file),
    }


def get_all_directories_from_src(source: str = 'src') -> list[str]:
    """
    Find all the java files from the Source file,
    Validates if its empty, and if it is the main file
    """
    dir_list = list()
    file_list = os.listdir(f'./{source}')

    for file in file_list:
        file_path = os.path.join(source, file)

        if os.path.isfile(file_path) and file.endswith('.java'):
            dir_list.append(source)

        if os.path.isdir(file_path):
            # Recursive search
            for sub_dir in get_all_directories_from_src(file_path):
                dir_list.append(sub_dir)

    return dir_list


def execute_java(args: object) -> None:
    dest_file = args['dest_file'].split('/')[1:]
    dest_file = (os.sep).join(dest_file)

    os.chdir('build')
    os.system(f'java {dest_file}')
    os.chdir('../')


def compile_Java(dir_list: list[str]) -> None:
    """
    Compiles and runs java, in case that a file did not compile
    it will stop the execution
    """

    command_arguments = ""
    for directory in dir_list:
        command_arguments += f'{os.path.join(directory, "*.java")} '

    # keeps the build folder updated without old classes
    if os.path.isdir('build'):
        shutil.rmtree('build')

    os.system(f'javac {command_arguments} -d build')

    # Error while compiling
    if not os.path.isdir('build'):
        raise Exception('Cannot compile')


def main(args) -> None:
    arguments = parse_arguments(args[1:])  # first argument is the script name

    # Main file not found
    if not os.path.isfile(arguments['main_file']):
        print("Main file not found")
        sys.exit(errno.ECANCELED)

    print('\n--- STARTING BUILDING PROCESS ---')
    # Printing Information
    print(f'Main class:')
    print(f'\t {arguments["main_file"]}\n')

    # Printing Packages Information
    dir_list = get_all_directories_from_src()
    print(f'Packages found {len(dir_list) - 1}')
    for num, package in enumerate(dir_list):
        print(f'\t{num}.- {package}')
    print()

    # Printing Status
    try:
        compile_Java(dir_list)
        print(f'\u001b[32m--- BUILD SUCCEED ---\u001b[0m')
    except:
        print(f'\u001b[31m--- BUILD FAILED ---\u001b[0m')
        sys.exit(errno.ECANCELED)

    print("\n\u001b[34mOUTPUT: \u001b[0m\n-----------")
    execute_java(arguments)


if __name__ == '__main__':
    main(sys.argv)
