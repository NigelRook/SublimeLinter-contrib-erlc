###
# Erlang linter plugin for SublimeLinter3
# Uses erlc, make sure it is in your PATH
#
# Copyright (C) 2014  Clement 'cmc' Rey <cr.rey.clement@gmail.com>
#
# MIT License
###

"""This module exports the Erlc plugin class."""

import os
from SublimeLinter.lint import Linter, util


class Erlc(Linter):
    """Provides an interface to erlc."""

    syntax = (
        "erlang",
        "erlang improved"
    )

    executable = "erlc"
    tempfile_suffix = "erl"

    # ERROR FORMAT # <file>:<line>: [Warning:|] <message> #
    regex = (
        r".+:(?P<line>\d+):"
        r"(?:(?P<warning>\sWarning:\s)|(?P<error>\s))"
        r"+(?P<message>.+)"
    )

    error_stream = util.STREAM_STDOUT

    defaults = {
        "include_dirs": []
    }

    def cmd(self):
        """
        return the command line to execute.

        this func is overridden so we can handle included directories.
        """
        settings = self.get_view_settings()
        dirs = settings.get('include_dirs', [])
        pa_dirs = settings.get('pa_dirs', [])
        pz_dirs = settings.get('pz_dirs', [])
        output_dir = settings.get('output_dir', ".")
        deps_dirs = settings.get('deps_dirs', [])

        if 'cmd' in settings:
            command = [settings.get('cmd')]
        else:
            command = [self.executable_path]

        command.append('-W')

        for d in deps_dirs:
            for dep in (path for path in (os.path.join(d, e) for e in os.listdir(d)) if os.path.isdir(path)):
                dep_ebin = os.path.join(dep, 'ebin')
                if os.path.isdir(dep_ebin):
                    pa_dirs.append(dep_ebin)

        for d in dirs:
            command.extend(["-I", d])

        for d in pa_dirs:
            command.extend(["-pa", d])

        for d in pz_dirs:
            command.extend(["-pz", d])

        command.extend(["-o", output_dir])

        return command
