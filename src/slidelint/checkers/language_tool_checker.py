""" Language tool based grammar checker """
from slidelint.utils import help_wrapper
from slidelint.utils import SubprocessTimeoutHelper
from slidelint.pdf_utils import convert_pdf_to_text

import os
import requests
import socket
import subprocess

from appdirs import user_data_dir
from lxml import etree

PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LT_PATH = os.path.join(PACKAGE_ROOT, 'LanguageTool')

MESSAGES = (
    {'id': 'C2000',
     'msg_name': 'language-tool',
     'msg': 'Language tool',
     'help': "Language tool found error"},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2001',
     'msg': 'Language tool',
     'msg_name': 'COMMA_PARENTHESIS_WHITESPACE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2002',
     'msg': 'Language tool',
     'msg_name': 'UPPERCASE_SENTENCE_START'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2003',
     'msg': 'Language tool',
     'msg_name': 'WHITESPACE_PUNCTUATION'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2004',
     'msg': 'Language tool',
     'msg_name': 'WHITESPACE_RULE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2005',
     'msg': 'Language tool',
     'msg_name': 'MORFOLOGIK_RULE_EN_US'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2006',
     'msg': 'Language tool',
     'msg_name': 'BRITISH_SIMPLE_REPLACE_RULE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2007',
     'msg': 'Language tool',
     'msg_name': 'MORFOLOGIK_RULE_EN_AU'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2008',
     'msg': 'Language tool',
     'msg_name': 'MORFOLOGIK_RULE_EN_CA'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2009',
     'msg': 'Language tool',
     'msg_name': 'MORFOLOGIK_RULE_EN_NZ'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2010',
     'msg': 'Language tool',
     'msg_name': 'A_WAS'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2011',
     'msg': 'Language tool',
     'msg_name': 'CONFUSION_OF_OUR_OUT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2012',
     'msg': 'Language tool',
     'msg_name': 'YOUR_SHOULD'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2013',
     'msg': 'Language tool',
     'msg_name': 'THE_SOME_DAY'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2014',
     'msg': 'Language tool',
     'msg_name': 'MAKE_US_OF'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2015',
     'msg': 'Language tool',
     'msg_name': 'ON_OF_THE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2016',
     'msg': 'Language tool',
     'msg_name': 'ASK_WETHER'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2017',
     'msg': 'Language tool',
     'msg_name': 'UP_TO_DATA'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2018',
     'msg': 'Language tool',
     'msg_name': 'FEEL_TREE_TO'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2019',
     'msg': 'Language tool',
     'msg_name': 'EASIEST_WAS_TO'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2020',
     'msg': 'Language tool',
     'msg_name': 'ARE_STILL_THE_SOME'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2021',
     'msg': 'Language tool',
     'msg_name': 'IS_EVEN_WORST'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2022',
     'msg': 'Language tool',
     'msg_name': 'DE_JURO'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2023',
     'msg': 'Language tool',
     'msg_name': 'MASSAGE_MESSAGE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2024',
     'msg': 'Language tool',
     'msg_name': 'I_THIN'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2025',
     'msg': 'Language tool',
     'msg_name': 'SUPPOSE_TO'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2026',
     'msg': 'Language tool',
     'msg_name': 'ALL_BE_IT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2027',
     'msg': 'Language tool',
     'msg_name': 'ALL_FOR_NOT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2028',
     'msg': 'Language tool',
     'msg_name': 'ALL_OVER_THE_WORD'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2029',
     'msg': 'Language tool',
     'msg_name': 'ANOTHER_WORDS'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2030',
     'msg': 'Language tool',
     'msg_name': 'BACK_AND_FOURTH'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2031',
     'msg': 'Language tool',
     'msg_name': 'BACK_IN_FORTH'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2032',
     'msg': 'Language tool',
     'msg_name': 'BOB_WIRE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2033',
     'msg': 'Language tool',
     'msg_name': 'BYE_THE_WAY'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2034',
     'msg': 'Language tool',
     'msg_name': 'CHALK_FULL'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2035',
     'msg': 'Language tool',
     'msg_name': 'EGG_YOKE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2036',
     'msg': 'Language tool',
     'msg_name': 'ET_ALL'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2037',
     'msg': 'Language tool',
     'msg_name': 'EYE_BROW'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2038',
     'msg': 'Language tool',
     'msg_name': 'FOR_SELL'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2039',
     'msg': 'Language tool',
     'msg_name': 'THERE_EXITS'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2040',
     'msg': 'Language tool',
     'msg_name': 'HE_THE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2041',
     'msg': 'Language tool',
     'msg_name': 'INSURE_THAT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2042',
     'msg': 'Language tool',
     'msg_name': 'IN_MASSE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2043',
     'msg': 'Language tool',
     'msg_name': 'IN_PARENTHESIS'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2044',
     'msg': 'Language tool',
     'msg_name': 'IN_STEAD_OF'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2045',
     'msg': 'Language tool',
     'msg_name': 'IN_TACT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2046',
     'msg': 'Language tool',
     'msg_name': 'IN_VEIN'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2047',
     'msg': 'Language tool',
     'msg_name': 'IT_SELF'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2048',
     'msg': 'Language tool',
     'msg_name': 'VE_GO_TO'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2049',
     'msg': 'Language tool',
     'msg_name': 'FOR_ALONG_TIME'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2050',
     'msg': 'Language tool',
     'msg_name': 'FOR_ALL_INTENSIVE_PURPOSES'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2051',
     'msg': 'Language tool',
     'msg_name': 'AWAY_FRO'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2052',
     'msg': 'Language tool',
     'msg_name': 'ONE_IN_THE_SAME'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2053',
     'msg': 'Language tool',
     'msg_name': 'PER_SE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2054',
     'msg': 'Language tool',
     'msg_name': 'SNEAK_PEAK'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2055',
     'msg': 'Language tool',
     'msg_name': 'SOME_WHAT_JJ'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2056',
     'msg': 'Language tool',
     'msg_name': 'STAND_ALONE_NN'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2057',
     'msg': 'Language tool',
     'msg_name': 'TEEM_TEAM'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2058',
     'msg': 'Language tool',
     'msg_name': 'UNDER_WEAR'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2059',
     'msg': 'Language tool',
     'msg_name': 'WHERE_AS'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2060',
     'msg': 'Language tool',
     'msg_name': 'WITCH_HAUNT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2061',
     'msg': 'Language tool',
     'msg_name': 'YOUR_S'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2062',
     'msg': 'Language tool',
     'msg_name': 'YOURS_APOSTROPHE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2063',
     'msg': 'Language tool',
     'msg_name': 'HEAR_HERE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2064',
     'msg': 'Language tool',
     'msg_name': 'TOT_HE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2065',
     'msg': 'Language tool',
     'msg_name': 'WITH_OUT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2066',
     'msg': 'Language tool',
     'msg_name': 'ALLOT_OF'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2067',
     'msg': 'Language tool',
     'msg_name': 'I_HERD'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2068',
     'msg': 'Language tool',
     'msg_name': 'ADVICE_ADVISE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2069',
     'msg': 'Language tool',
     'msg_name': 'ALL_MOST'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2070',
     'msg': 'Language tool',
     'msg_name': 'ANALYSIS_IF'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2071',
     'msg': 'Language tool',
     'msg_name': 'BED_ENGLISH'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2072',
     'msg': 'Language tool',
     'msg_name': 'PIGEON_ENGLISH'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2073',
     'msg': 'Language tool',
     'msg_name': 'TELEPHONE_POLL'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2074',
     'msg': 'Language tool',
     'msg_name': 'OPINION_POLE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2075',
     'msg': 'Language tool',
     'msg_name': 'BOTTLE_NECK'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2076',
     'msg': 'Language tool',
     'msg_name': 'FIRE_ARM'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2077',
     'msg': 'Language tool',
     'msg_name': 'NEWS_PAPER'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2078',
     'msg': 'Language tool',
     'msg_name': 'AN_OTHER'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2079',
     'msg': 'Language tool',
     'msg_name': 'IN_THE_PASSED'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2080',
     'msg': 'Language tool',
     'msg_name': 'SENT_START_THEM'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2081',
     'msg': 'Language tool',
     'msg_name': 'TOO_TO'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2082',
     'msg': 'Language tool',
     'msg_name': 'THINK_YOU_A'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2083',
     'msg': 'Language tool',
     'msg_name': 'IS_WERE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2084',
     'msg': 'Language tool',
     'msg_name': 'ONE_ORE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2085',
     'msg': 'Language tool',
     'msg_name': 'THE_ONLY_ON'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2086',
     'msg': 'Language tool',
     'msg_name': 'THEIR_IS'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2087',
     'msg': 'Language tool',
     'msg_name': 'I_A'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2088',
     'msg': 'Language tool',
     'msg_name': 'I_NEW'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2089',
     'msg': 'Language tool',
     'msg_name': 'PLEASE_NOT_THAT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2090',
     'msg': 'Language tool',
     'msg_name': 'NUT_NOT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2091',
     'msg': 'Language tool',
     'msg_name': 'AND_SO_ONE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2092',
     'msg': 'Language tool',
     'msg_name': 'THROUGH_AWAY'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2093',
     'msg': 'Language tool',
     'msg_name': 'OR_WAY_IT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2094',
     'msg': 'Language tool',
     'msg_name': 'DT_RESPONDS'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2095',
     'msg': 'Language tool',
     'msg_name': 'THINK_OFF'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2096',
     'msg': 'Language tool',
     'msg_name': 'YOU_THING'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2097',
     'msg': 'Language tool',
     'msg_name': 'VBZ_VBD'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2098',
     'msg': 'Language tool',
     'msg_name': 'FORE_DPS'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2099',
     'msg': 'Language tool',
     'msg_name': 'LESS_MORE_THEN'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2100',
     'msg': 'Language tool',
     'msg_name': 'COMMA_THAN'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2101',
     'msg': 'Language tool',
     'msg_name': 'FROM_THAN_ON'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2102',
     'msg': 'Language tool',
     'msg_name': 'AND_THAN'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2103',
     'msg': 'Language tool',
     'msg_name': 'THAN_INTERJ'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2104',
     'msg': 'Language tool',
     'msg_name': 'WHO_THAN'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2105',
     'msg': 'Language tool',
     'msg_name': 'OF_CAUSE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2106',
     'msg': 'Language tool',
     'msg_name': 'LOOK_ATE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2107',
     'msg': 'Language tool',
     'msg_name': 'A_KNOW_BUG'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2108',
     'msg': 'Language tool',
     'msg_name': 'MY_BE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2109',
     'msg': 'Language tool',
     'msg_name': 'IS_SHOULD'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2110',
     'msg': 'Language tool',
     'msg_name': 'THE_FLEW'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2111',
     'msg': 'Language tool',
     'msg_name': 'CAN_NOT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2112',
     'msg': 'Language tool',
     'msg_name': 'CAN_BEEN'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2113',
     'msg': 'Language tool',
     'msg_name': 'CANT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2114',
     'msg': 'Language tool',
     'msg_name': 'TURNED_OFF'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2115',
     'msg': 'Language tool',
     'msg_name': 'FEMALE_ACTOR'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2116',
     'msg': 'Language tool',
     'msg_name': 'FEMALE_WAITER'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2117',
     'msg': 'Language tool',
     'msg_name': 'FIRST_WOMAN_NOUN'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2118',
     'msg': 'Language tool',
     'msg_name': 'FIRST_MAN_NOUN'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2119',
     'msg': 'Language tool',
     'msg_name': 'LITTLE_BIT'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2120',
     'msg': 'Language tool',
     'msg_name': 'MANGER_MANAGER'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2121',
     'msg': 'Language tool',
     'msg_name': 'HAD_OF'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2122',
     'msg': 'Language tool',
     'msg_name': 'ONES'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2123',
     'msg': 'Language tool',
     'msg_name': 'SPARKING_WINE'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2124',
     'msg': 'Language tool',
     'msg_name': 'VERY_MATCH'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2125',
     'msg': 'Language tool',
     'msg_name': 'VARY_MUCH'},
    {'help': 'http://wiki.languagetool.org/',
     'id': 'C2126',
     'msg': 'Language tool',
     'msg_name': 'ZERO-SUM_GAIN'}
)

MESSAGES_BY_RULES = {m['msg_name']: m for m in MESSAGES}


def get_java():
    """ getting executable binary of java 7"""
    cmd = ["update-alternatives", "--query", "java"]
    try:
        output = SubprocessTimeoutHelper(cmd)()
    except (OSError, IOError):
        return 'java'
    for line in output:
        if not line.startswith("Alternative: "):
            continue
        if "java-7" in line:
            return line[len("Alternative: "):].strip(" \n")
    return 'java'


def get_free_port():
    """ returns unused port number"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(('', 0))
    sock.listen(socket.SOMAXCONN)
    _, port = sock.getsockname()
    sock.close()
    return str(port)


class LanguagetoolSubprocessHandler(SubprocessTimeoutHelper):
    """ class for setting timeout for Languagetool """

    def subprocess_handler(self):
        """ starts languagetool_server and wait until message about that it
        ready to work appear in its logs """
        self.process = subprocess.Popen(
            self.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,)
        # waiting for server start
        output = []
        while True:
            output.append(self.process.stdout.readline())
            if 'Server started' in output[-1]:
                break

            retcode = self.process.poll()
            if retcode is not None:
                output.extend(self.process.stdout.readlines())
                output.insert(
                    0,
                    "languagetool-server died with exit code %s!\n" % retcode
                )
                output.insert(1, " ".join(self.cmd) + "\n")
                output.append("\nLanguageTool requires Java 7 or later."
                              " Please check and update java version."
                              " For more details look at "
                              "http://help.ubuntu.com/community/Java\n")
                raise IOError("".join(output))


def start_languagetool_server(lt_path, config_file):
    """ starts languagetool_server, returns its port and pid """
    port = get_free_port()
    java = get_java()
    cmd = [java, '-cp', os.path.join(lt_path, 'languagetool-server.jar'),
           'org.languagetool.server.HTTPServer', '--port', port]
    lt_server = LanguagetoolSubprocessHandler(cmd, 30)
    lt_server()
    pid = lt_server.process.pid
    with open(config_file, 'w') as out_file:
        out_file.write("%s,%s" % (port, pid))
    return port, pid


def get_languagetool_port_and_pid(lt_path, config_file):
    """ checks if languagetool is running and stats it if not;
    returns its ports and pid"""
    if os.path.isfile(config_file):
        port, pid = open(config_file, 'r').read().strip(' \n').split(',')
        if os.path.exists("/proc/%s" % pid):
            return port, int(pid)
    return start_languagetool_server(lt_path, config_file)


class LanguagetoolServer(object):
    """ Class for allowing to work with LanguagetoolServer as
    with context object"""
    def __init__(self, lt_path, keep_alive=False):
        self.keep_alive = keep_alive
        config_dir = user_data_dir('slidelint')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        self.config_file = os.path.join(config_dir, 'run')
        self.lt_path = lt_path
        self.port, self.pid = get_languagetool_port_and_pid(self.lt_path,
                                                            self.config_file)
        self.url = 'http://127.0.0.1:%s' % self.port

    # pylint gets confused about lxml.etree not having fromstring or
    # XMLSyntaxError properties.
    # pylint: disable=no-member
    def grammar_checker(self, text, language="en-US"):
        """ sends text to Languagetool Server and returns its checks results"""
        data = dict(language=language, text=text)
        try:
            content = requests.post(self.url, data=data, timeout=15)
        except requests.exceptions.Timeout:
            # after tense LanguagetoolServer are freezing,
            # so it's needs a restart
            os.kill(self.pid, 9)
            self.port, self.pid = start_languagetool_server(self.lt_path,
                                                            self.config_file)
            self.url = 'http://127.0.0.1:%s' % self.port
            content = requests.post(self.url, data=data, timeout=15)
        try:
            root = etree.fromstring(content.text.encode('utf-8'))
        except etree.XMLSyntaxError as e:
            # Add the content to the traceback
            e.message += """
--
%s
--
""" % (content.text.encode('utf-8'))
            raise

        return root.findall('error')

    def __enter__(self):
        return self.grammar_checker

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if not self.keep_alive:
            os.kill(self.pid, 9)


def new_lines_replaser(string):
    """ string clean up function for language-tool server """
    string = string.replace(' \n', ' ').replace('\n ', ' ')
    return string.replace('\n', ' ').replace('  ', ' ')


@help_wrapper(MESSAGES)
def main(target_file=None, keep_alive='False'):
    """ language tool based grammar checker """
    keep_alive = keep_alive.lower() == 'true'
    pages = convert_pdf_to_text(target_file)
    rez = []
    with LanguagetoolServer(LT_PATH, keep_alive) as grammar_checker:
        for num, page in enumerate(pages):
            for paragraph in page:
                # fixing new-lines and spaces for languagetool
                for error in grammar_checker(new_lines_replaser(paragraph)):
                    rule_id = error.get('ruleId')
                    cur_msg = MESSAGES_BY_RULES.get(
                        rule_id,
                        MESSAGES_BY_RULES['language-tool'])
                    rez.append({
                        'id': cur_msg['id'],
                        'page': 'Slide %s' % (num + 1),
                        'msg_name': rule_id,
                        'msg': '%s - %s' % (error.get('locqualityissuetype'),
                                            error.get('msg')),
                        'help': error.get('context')})
    return rez
