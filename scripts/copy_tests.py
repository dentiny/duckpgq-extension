from os import listdir, mkdir
from os.path import isfile, join, exists

from pathlib import Path
import shutil
from textwrap import dedent
import sys
import getopt
import os


def main(argv):
    mode = ''
    opts, args = getopt.getopt(argv, "hm:", ["mode=", "ofile="])
    for opt, arg in opts:
        if opt == '-h':
            print('copy_tests.py -m <release/debug>')
            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg
    if mode != "release" or mode != "debug":
        raise Exception("Invalid parameter, --mode should be release or debug")
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    test_path_duckpgq = Path("../test/sql")
    test_path_duckdb = Path("../duckdb/test/extension/duckpgq")

    onlyfiles = [str(f) for f in listdir(test_path_duckpgq) if isfile(join(test_path_duckpgq, f))]

    if not exists(test_path_duckdb):
        mkdir(test_path_duckdb)
    else:
        shutil.rmtree(test_path_duckdb)
        mkdir(test_path_duckdb)

    for file in onlyfiles:
        f = open(test_path_duckpgq / file, "r")
        content = f.read()
        content = content.replace("require duckpgq\n",
                                  dedent(f"""\
                                  statement ok
                                  install '__BUILD_DIR__/../../../build/{mode}/extension/duckpgq/duckpgq.duckdb_extension';
                                  
                                  statement ok
                                  load 'duckpgq';
                                  """))

        new_file = open(test_path_duckdb / file, "w")
        new_file.write(content)
        new_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
