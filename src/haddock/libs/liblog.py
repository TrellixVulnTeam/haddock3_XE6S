import logging
import io
import sys
from functools import partial
from logging import StreamHandler, FileHandler
from os import get_terminal_size
from pathlib import Path


log_file_name = 'log'


info_formatter = '[%(asctime)s] %(message)s'
debug_formatter = (
    "[%(asctime)s] "
    "%(filename)s:%(name)s:%(funcName)s:%(lineno)d: "
    "%(message)s"
    )

log_formatters = {
    'DEBUG': debug_formatter,
    'INFO': info_formatter,
    'WARNING': info_formatter,
    'ERROR': info_formatter,
    'CRITICAL': info_formatter,
    }

log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
    }


def add_loglevel_arg(parser):
    """Add log level argument to CLI."""
    parser.add_argument(
        "--log-level",
        default='INFO',
        choices=list(log_levels.keys()),
        )
    return


def add_handler(
        log_obj,
        handler,
        stream,
        log_level='INFO',
        formatter=info_formatter,
        ):
    """Add a logging Handler to the log object."""
    ch = handler(stream)
    ch.setLevel(log_levels[log_level.upper()])
    ch.setFormatter(logging.Formatter(formatter))
    log_obj.addHandler(ch)
    return ch


def add_log_for_CLI(log, log_level, logfile):
    """Configure log for command-line clients."""
    llu = log_level.upper()

    params = {
        'log_level': log_level,
        'formatter': log_formatters[log_level],
        }

    log.handlers.clear()
    add_sysout_handler(log, **params)
    add_logfile_handler(log, stream=logfile, **params)
    return


add_sysout_handler = partial(add_handler, handler=StreamHandler, stream=sys.stdout)
add_syserr_handler = partial(add_handler, handler=StreamHandler, stream=sys.stderr, log_level='ERROR')
add_logfile_handler = partial(add_handler, handler=FileHandler, stream=log_file_name)
add_stringio_handler = partial(add_handler, handler=StreamHandler, stream=io.StringIO())