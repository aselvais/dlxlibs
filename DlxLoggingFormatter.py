from logging import Formatter
import json
import re

class DlxLoggingFormatter(Formatter):
    """
    Subclassing the default logging.Formatter

    Args:
        Formatter ([type]): [description]
    """

    def format(self, record):
        """
        Removes carriage return from the msg and custom formating

        Args:
            record ([type]): [description]

        Returns:
            [type]: [description]
        """
        if re.match('^\{', record.msg):
            try:
                r = json.loads(record.msg)
                ks = r.keys()
                if 'command' in ks:
                    record.command = r["command"]
                if 'storagename' in ks:
                    record.storagename = r["storagename"]
                if 'count' in ks:
                    record.count = r["count"]
            except:
                pass
        else:
            record.msg = re.sub(r'^\"|\"$', '', json.dumps(record.msg))
            #record.exc_text = re.sub(r'^\"|\"$', '', json.dumps(record.exc_text))
        return super(DlxLoggingFormatter, self).format(record)
