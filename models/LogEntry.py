from typing import Dict
from typing_extensions import TypedDict
import json

class LogEntry(TypedDict):

    source_system_name: str # logs
    schema_name: str        # logs
    table_name: str         # logs
    env: str                # dev
    asctime: str            # 2020-11-23 22:05:20,860
    levelname: str          # DEBUG
    levelno: str            # 10
    message: str            # end main_launcher
    module: str             # DlxImportsTemplate
    filename: str           # DlxImportsTemplate.py
    homedir: str            # 
    pathname: str           # /home/cdsw/datasnapshot-codegen/mssql/safeguardcorp/../../../libs/DlxImportsTemplate.py
    created: str            # 1606169120.860502
    msecs: str              # 860
    relativeCreated: str    # 308079
    name: str               # dlxlibs.DlxLogger
    username: str           # cdsw
    hostname: str           # 
    funcName: str           # main_launcher
    lineno: str             # 711
    process: str            # 3799
    processName: str        # MainProcess
    thread: str             # 139701601322752
    threadName: str         # MainThread
    args: str               # ()
    exc_info: str           # None
    exc_text: str           # None
    stack_info: str         # None


    def __init__(self, l: TypedDict) -> None:
        for i in l:
            self[i] = l[i]

