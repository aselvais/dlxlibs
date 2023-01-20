"""
Generic methods for using the command line on linux
without any python library.
"""
import os


class DlxBash:


    def _execute_command(self, cmd=""):
        """
        Execute a shell command

        Args:
            cmd (str, optional): Command. Defaults to "".

        Returns:
            str: Output resulting of the command execution
        """
        stream = os.popen(cmd)
        output = stream.read()
        return output
