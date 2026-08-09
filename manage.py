import multiprocessing
import os
import sys


def main():
    multiprocessing.freeze_support()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) == 1:
        sys.argv = [sys.argv[0], "runserver", "0.0.0.0:8000", "--noreload"]
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

# import os
# import sys


# def main():
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# if __name__ == "__main__":
#     main()
