import os


def get_files_num(path):
    if not os.path.isdir(path):
        print(f'Warning the provided path ({path}) must be a directory\n trying to get the parent')
        path = os.path.dirname(path)
    return len(os.listdir(path))

def get_statuses(path):
    if not os.path.isdir(path):
        print(f'Warning the provided path ({path}) must be a directory\n trying to get the parent')
        path = os.path.dirname(path)
    return os.listdir(path)