import subprocess


def bash(*args) -> bool:
    try:
        return subprocess.call(list(args)) == 0
    except subprocess.CalledProcessError as e:
        print(f"There was a problem calling the following command: {args}")
