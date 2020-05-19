import os


class DlxBash:

    def _execute_command(self, cmd=""):
        """
        Execute a shell command

        :param cmd: String Command
        :return: Output resulting of the command execution
        """
        stream = os.popen(cmd)
        output = stream.read()
        return output
