#!/usr/bin/env python
import os
import sys
#salut moi c'est mathieu
#c'est toujours mathieu

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projetprepa.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
