"""
\defgroup File system
Abstraction layer to use HDFS on the EDP. 
"""
from datetime import datetime
import re, os, sys
try:
    _rootpath = os.path.dirname(os.path.abspath(__file__)) + '/..'
except:
    _rootpath = os.getcwd()
sys.path.append(_rootpath)
from dlxlibs.DlxLogger import DlxLogger
from dlxlibs.DlxBash import DlxBash

_logger = DlxLogger().get_logger()


class DlxHdfs(DlxBash):
    """
    Simple API to access HDFS for our EDP platform

    Args:
        DlxBash ([type]): [description]
    """


    def __init__(self):
        pass


    def _file_system_line_to_dict(self, l):
        """
        Returns a dictionary out of a ls line (from HDFS)

        Args:
            l ([type]): [description]

        Returns:
            [type]: [description]
        """
        m = re.search(
            '^([+drwxt-]{10,11})[ ]{1,50}([0-9-]{1,20})[ ]{1,50}([A-z0-9]{1,50})[ ]{1,50}([A-z0-9]{1,50})[ ]{1,50}([0-9]{1,50})[ ]{1,50}([0-9-]{10})[ ]{1,50}([0-9:]{5})[ ]{1,50}(.*)$',
            l
        )
        ll = {'_raw_output': l}
        try:
            if m.lastindex == 8:
                ll['permissions'] = m.group(1)  # 'drwxr-xr-x'
                ll['number_of_replicas'] = m.group(2)  # '-'
                ll['userid'] = m.group(3)  # 't442512'
                ll['groupid'] = m.group(4)  # 't442512'
                ll['filesize'] = int(m.group(5))  # '0'
                ll['modification_date'] = m.group(6)  # '2020-04-26'
                ll['modification_time'] = m.group(7)  # '20:00'
                ll['filename'] = m.group(8)  # '.Trash'
                try:
                    ll['timestamp'] = datetime.timestamp(
                        datetime.strptime(ll['modification_date'] + ' ' + ll['modification_time'], '%Y-%m-%d %H:%M'))
                except:
                    ll['timestamp'] = 0
        except:
            _logger.error("Can not create dict out of : " + l)
        return ll

    def ls(self, path=""):
        """
        List files in hdfs
        [-ls [-C] [-d] [-h] [-q] [-R] [-t] [-S] [-r] [-u] [-e] [<path> ...]]

        Args:
            path (str, optional): Path. Defaults to "".

        Returns:
            [type]: [description]
        """
        _logger.debug("HDFS fs \"" + path + "\"")
        r = self._execute_command('hdfs dfs -ls ' + path).split("\n")
        r.remove(r[len(r) - 1])
        r.remove(r[0])
        toret = list()
        for i in r:
            toret.append(self._file_system_line_to_dict(i))
        return toret

    def cat(self, src=""):
        '''
        [-cat [-ignoreCrc] <src> ...]
        :param src:
        :return:
        '''
        _logger.debug("HDFS cat \"" + src + "\"")
        return self._execute_command('hdfs dfs -cat ' + src)

    def chgrp(self, path=""):
        '''
        [-chgrp [-R] GROUP PATH...]
        :param path:
        :return:
        '''
        _logger.debug("HDFS chgrp \"" + path + "\"")
        return self._execute_command('hdfs dfs -chgrp ' + path)

    def chmod(self, path=""):
        '''
        [-chmod [-R] <MODE[,MODE]... | OCTALMODE> PATH...]
        :param path:
        :return:
        '''
        _logger.debug("HDFS chmod \"" + path + "\"")
        return self._execute_command('hdfs dfs -chmod ' + path)

    def chown(self, path=""):
        '''
        [-chown [-R] [OWNER][:[GROUP]] PATH...]
        :param path:
        :return:
        '''
        _logger.debug("HDFS chown \"" + path + "\"")
        return self._execute_command('hdfs dfs -chown ' + path)

    def copyFromLocal(self, localsrc="", dst=""):
        '''
        [-copyFromLocal [-f] [-p] [-l] [-d] [-t <thread count>] <localsrc> ... <dst>]
        :param localsrc:
        :param dst:
        :return:
        '''
        _logger.debug("HDFS copyFromLocal \"" + localsrc + "\"" + " " + dst)
        return self._execute_command('hdfs dfs -copyFromLocal ' + localsrc + " " + dst)

    def copyToLocal(self, src="", localdst=""):
        '''
        [-copyToLocal [-f] [-p] [-ignoreCrc] [-crc] <src> ... <localdst>]
        :param src:
        :param localdst:
        :return:
        '''
        _logger.debug("HDFS copyToLocal \"" + src + "\"" + " " + localdst)
        return self._execute_command('hdfs dfs -copyToLocal ' + src + " " + localdst)

    def count(self, path=""):
        '''
        [-count [-q] [-h] [-v] [-t [<storage type>]] [-u] [-x] [-e] <path> ...]
        :param path:
        :return:
        '''
        _logger.debug("HDFS count \"" + path + "\"")
        return self._execute_command('hdfs dfs -count ' + path)

    def cp(self, src="", dst=""):
        '''
        [-cp [-f] [-p | -p[topax]] [-d] <src> ... <dst>]
        :param src:
        :param dst:
        :return:
        '''
        _logger.debug("HDFS cp \"" + src + "\" " + dst)
        return self._execute_command('hdfs dfs -cp ' + src + " " + dst)

    def df(self, path=""):
        '''
        [-df [-h] [<path> ...]]
        :param path:
        :return:
        '''
        _logger.debug("HDFS df \"" + path + "\"")
        return self._execute_command('hdfs dfs -df ' + path)

    def du(self, path=""):
        '''
        [-du [-s] [-h] [-v] [-x] <path> ...]
        :param path:
        :return:
        '''
        _logger.debug("HDFS du \"" + path + "\"")
        return self._execute_command('hdfs dfs -du ' + path)

    def find(self, path="", expression=""):
        '''
        [-find <path> ... <expression> ...]
        :param path:
        :param expression:
        :return:
        '''
        _logger.debug("HDFS find \"" + path + "\" " + expression)
        return self._execute_command('hdfs dfs -find ' + path + " " + expression)

    def get(self, src="", localdst=""):
        '''
        [-get [-f] [-p] [-ignoreCrc] [-crc] <src> ... <localdst>]
        :param src:
        :param localdst:
        :return:
        '''
        _logger.debug("HDFS get \"" + src + "\" " + localdst)
        return self._execute_command('hdfs dfs -get ' + src + " " + localdst)

    def mkdir(self, path=""):
        '''
        [-mkdir [-p] <path> ...]
        :param path:
        :return:
        '''
        _logger.debug("HDFS mkdir \"" + path + "\"")
        return self._execute_command('hdfs dfs -mkdir ' + path)

    def moveFromLocal(self, localsrc="", dst=""):
        '''
        [-moveFromLocal <localsrc> ... <dst>]
        :param localsrc:
        :param dst:
        :return:
        '''
        _logger.debug("HDFS moveFromLocal \"" + localsrc + "\" " + dst)
        return self._execute_command('hdfs dfs -moveFromLocal ' + localsrc + " " + dst)

    def moveToLocal(self, src="", localdst=""):
        '''
        [-moveToLocal <src> <localdst>]
        :param src:
        :param localdst:
        :return:
        '''
        _logger.debug("HDFS moveToLocal \"" + src + "\" " + localdst)
        return self._execute_command('hdfs dfs -moveToLocal ' + src + " " + localdst)

    def mv(self, src="", dst=""):
        '''
        [-mv <src> ... <dst>]
        :param src:
        :param dst:
        :return:
        '''
        _logger.debug("HDFS mv \"" + src + "\" " + dst)
        return self._execute_command('hdfs dfs -mv ' + src + " " + dst)

    def rm(self, src=""):
        '''
        [-rm [-f] [-r|-R] [-skipTrash] [-safely] <src> ...]
        :param src:
        :return:
        '''
        _logger.debug("HDFS rm \"" + src + "\"")
        return self._execute_command('hdfs dfs -rm ' + src)

    def rmdir(self, dir=""):
        '''
        [-rmdir [--ignore-fail-on-non-empty] <dir> ...]
        :param dir:
        :return:
        '''
        _logger.debug("HDFS rmdir \"" + dir + "\"")
        return self._execute_command('hdfs dfs -rmdir ' + dir)

    def stat(self, path=""):
        '''
        [-stat [format] <path> ...]
        :param path:
        :return:
        '''
        _logger.debug("HDFS stat \"" + path + "\"")
        return self._execute_command('hdfs dfs -stat ' + path)

    def tail(self, file=""):
        '''
        [-tail [-f] <file>]
        :param file:
        :return:
        '''
        _logger.debug("HDFS tail \"" + file + "\"")
        return self._execute_command('hdfs dfs -tail ' + file)

    def usage(self, cmd=""):
        '''
        [-usage [cmd ...]]
        :param cmd:
        :return:
        '''
        _logger.debug("HDFS usage \"" + cmd + "\"")
        return self._execute_command('hdfs dfs -usage ' + cmd)
