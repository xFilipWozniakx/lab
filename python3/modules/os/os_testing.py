import os


# os — Miscellaneous operating system interfaces

#  All functions in this module raise OSError (or subclasses thereof)
#  in the case of invalid or inaccessible file names and paths,
#  or other arguments that have the correct type, but are not accepted by the operating system

# except OSError:
#     print("File or path is inaccessible")
#

print(os.name)  # posix

# process parameters:

os.ctermid()  # returns which terminal emulator was used to run script

# os.environ retuns key value pairs for environemtn variables:
# os.environb ( returns in byte format instead of string)


def return_env():
    for i in os.environ.items():
        # can uses with os.environ["SHELL"] f.ex
        print(i)

        # works just fine on arch linux
        os.environ["new"] = "random_env_var"
        print(os.environ["new"])


def clear_env():
    # os.environ.clear() or smarter:
    os.environ["TEST"] = "TESTING_ENV_VARIABLES"
    os.environ.pop("TEST")

    print(os.environ["TEST"])


# try:
#     clear_env()
# except KeyError:
#     print("Env key is not in env")


"""
os.reload_environ()
The os.environ and os.environb mappings are a cache of environment variables at the time that Python started. 
As such, changes to the current process environment are not reflected if made outside Python, or by os.putenv() or os.unsetenv().
Use os.reload_environ() to update os.environ and os.environb with any such changes to the current process environment.
"""
