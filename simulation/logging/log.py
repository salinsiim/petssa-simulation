import os


def log(step, path, intersection_name, msg):
    file_path = path + '/logging.txt'
    mode = 'a' if os.path.exists(file_path) else 'w'
    with open(file_path, mode) as logging_file:
        print("Step %s, %s: %s" % (step, intersection_name, msg), file=logging_file)
