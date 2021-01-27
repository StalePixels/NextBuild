# -*- coding: utf-8 -*-

import argparse

from src import arch
from src.api import errmsg
from src.api.config import OPTIONS

from .version import VERSION


def parse_warning_option(code: str) -> str:
    if not errmsg.is_valid_warning_code(code):
        raise argparse.ArgumentTypeError(f"Invalid warning option 'W{code}'")
    return code


# ------------------------------------------------------------
# Command line parser
# ------------------------------------------------------------
def parser() -> argparse.ArgumentParser:
    parser_ = argparse.ArgumentParser(
        prefix_chars='-+'
    )
    parser_.add_argument('PROGRAM', type=str,
                         help='BASIC program file')
    parser_.add_argument('-d', '--debug', dest='debug', default=OPTIONS.Debug, action='count',
                         help='Enable verbosity/debugging output. Additional -d increase verbosity/debug level')
    parser_.add_argument('-O', '--optimize', type=int, default=OPTIONS.optimization,
                         help='Sets optimization level. '
                              '0 = None (default level is {0})'.format(OPTIONS.optimization))
    parser_.add_argument('-o', '--output', type=str, dest='output_file', default=None,
                         help='Sets output file. Default is input filename with .bin extension')
    parser_.add_argument('-T', '--tzx', action='store_true',
                         help="Sets output format to tzx (default is .bin)")
    parser_.add_argument('-t', '--tap', action='store_true',
                         help="Sets output format to tap (default is .bin)")
    parser_.add_argument('-B', '--BASIC', action='store_true', dest='basic',
                         help="Creates a BASIC loader which loads the rest of the CODE. Requires -T ot -t")
    parser_.add_argument('-a', '--autorun', action='store_true',
                         help="Sets the program to be run once loaded")
    parser_.add_argument('-A', '--asm', action='store_true',
                         help="Sets output format to asm")
    parser_.add_argument('-S', '--org', type=str, default=str(OPTIONS.org),
                         help="Start of machine code. By default %i" % OPTIONS.org)
    parser_.add_argument('-e', '--errmsg', type=str, dest='stderr', default=OPTIONS.StdErrFileName,
                         help='Error messages file (standard error console by default)')
    parser_.add_argument('--array-base', type=int, default=OPTIONS.array_base,
                         help='Default lower index for arrays ({0} by default)'.format(OPTIONS.array_base))
    parser_.add_argument('--string-base', type=int, default=OPTIONS.string_base,
                         help='Default lower index for strings ({0} by default)'.format(OPTIONS.array_base))
    parser_.add_argument('-Z', '--sinclair', action='store_true',
                         help='Enable by default some more original ZX Spectrum Sinclair BASIC features:'
                              ' ATTR, SCREEN$, POINT')
    parser_.add_argument('-H', '--heap-size', type=int, default=OPTIONS.heap_size,
                         help='Sets heap size in bytes (default {0} bytes)'.format(OPTIONS.heap_size))
    parser_.add_argument('--debug-memory', action='store_true',
                         help='Enables out-of-memory debug')
    parser_.add_argument('--debug-array', action='store_true',
                         help='Enables array boundary checking')
    parser_.add_argument('--strict-bool', action='store_true',
                         help='Enforce boolean values to be 0 or 1')
    parser_.add_argument('--enable-break', action='store_true',
                         help='Enables program execution BREAK detection')
    parser_.add_argument('-E', '--emit-backend', action='store_true',
                         help='Emits backend code instead of ASM or binary')
    parser_.add_argument('--explicit', action='store_true',
                         help='Requires all variables and functions to be declared before used')
    parser_.add_argument('-D', '--define', type=str, dest='defines', action='append',
                         help='Defines de given macro. Eg. -D MYDEBUG or -D NAME=Value')
    parser_.add_argument('-M', '--mmap', type=str, dest='memory_map', default=None,
                         help='Generate label memory map')
    parser_.add_argument('-i', '--ignore-case', action='store_true',
                         help='Ignore case. Makes variable names are case insensitive')
    parser_.add_argument('-I', '--include-path', type=str, default='',
                         help='Add colon separated list of directories to add to include path. e.g. -I dir1:dir2')
    parser_.add_argument('--strict', action='store_true',
                         help='Enables strict mode. Force explicit type declaration')
    parser_.add_argument('--headerless', action='store_true',
                         help='Header-less mode: omit asm prologue and epilogue')
    parser_.add_argument('--version', action='version', version='%(prog)s {0}'.format(VERSION))
    parser_.add_argument('--parse-only', action='store_true',
                         help='Only parses to check for syntax and semantic errors')
    parser_.add_argument('--append-binary', default=[], action='append',
                         help='Appends binary to tape file (only works with -t or -T)')
    parser_.add_argument('--append-headless-binary', default=[], action='append',
                         help='Appends binary to tape file (only works with -t or -T)')
    parser_.add_argument('-N', '--zxnext', action='store_true',
                         help='Enables ZX Next asm extended opcodes')
    parser_.add_argument('--arch', type=str, default=arch.AVAILABLE_ARCHITECTURES[0],
                         help=f"Target architecture (defaults is'{arch.AVAILABLE_ARCHITECTURES[0]}'). "
                              f"Available architectures: {','.join(arch.AVAILABLE_ARCHITECTURES)}")
    parser_.add_argument('--expect-warnings', default=OPTIONS.expect_warnings, type=int,
                         help='Expects N warnings: first N warnings will be silenced')
    parser_.add_argument('-W', '--disable-warning', type=parse_warning_option, action='append',
                         help='Disables warning WXXX (i.e. -W100 disables warning with code W100)')
    parser_.add_argument('+W', '--enable-warning', type=parse_warning_option, action='append',
                         help='Disables warning WXXX (i.e. -W100 disables warning with code W100)')
    parser_.add_argument('--hide-warning-codes', action='store_true',
                         help='Hides WXXX codes')
    return parser_
