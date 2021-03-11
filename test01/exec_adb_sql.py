# coding=utf8
from optparse import OptionParser

import subprocess
import datetime
import yaml
import os
import sys
import time

TASK_HOME = os.environ['TASK_HOME']

opt_parser = OptionParser()
opt_parser.add_option('--db', action='store', type='string', dest='db', help='database name')
opt_parser.add_option('--table', action='store', type='string', dest='table', help='table name')
opt_parser.add_option('--sql', action='store', type='string', dest='sql', help='export data sql')
opt_parser.add_option('--output', action='store', type='string', dest='output', help='output file name')
opt_parser.add_option('--header', action='store_true', dest='header', default=False,
                      help='if export csv contains header')
opt_parser.add_option('--file', action='store', type='string', dest='file', default=False, help='sql file executed')
opt_parser.add_option('--inc_date', action='store', type='string', dest='inc_date', default=False, help='inc data date')


def load_config_from_db_conf(key):
    config_file = f'{TASK_HOME}/_global_conf/db_conf.yaml'
    with open(config_file, 'r') as r:
        config = yaml.load(r)
    return config[key]


def run_shell(cmd):
    # print("""cmd: {}""".format(cmd))
    sub = subprocess.Popen(""" %s """ % cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='.', shell=True)
    outs = []
    while sub.poll() is None:
        lines = sub.stdout.readlines()
        lines = [line.decode('utf-8', 'ignore') for line in lines]
        outs = outs + lines
        time.sleep(1)
    return sub.returncode, ''.join(outs)


def do_export(config, output, table=None, sql=None, header=False):
    if table:
        export_sql = f"\\COPY {table} to '{output}' with csv"
    elif sql:
        export_sql = f"\\copy ({sql}) to '{output}' with csv"
    else:
        raise Exception('table or sql not assigned.')

    if header:
        export_sql = f'{export_sql}  header'

    cmd = f""" export PGPASSWORD='{config["password"]}'; psql -h {config["host"]} -p {config["port"]} -d {config["database"]} -U {config["user"]} <<EOF
{export_sql}
EOF
"""
    (status, log) = run_shell(cmd)
    assert status == 0, print(log)


def do_new_file(config, file, inc_date):
    print("""sed -e "s/crmincdate/{0}/g" sql/{1} > sql_inc/{1}_{0} """.format(inc_date, file))
    os.system("""sed -e "s/crmincdate/{0}/g" sql/{1} > sql_inc/{1}_{0} """.format(inc_date, file))


def do_exec(config, file, inc_date):
    if file:
        cmd = f"""export PGPASSWORD='{config["password"]}'; psql -h {config["host"]} -p {config["port"]} -d {config["database"]} -U {config["user"]} -f sql_inc/{file}_{inc_date}"""
        # print(cmd)
        (status, log) = run_shell(cmd)


if __name__ == '__main__':
    option = opt_parser.parse_args(sys.argv[1:])[0]
    assert option.db, '[db] name should be assigned.'
    assert option.table or option.sql or option.file, '[table] or [sql] or [file] should be assigned.'
    # assert option.output and option.output.endswith('.csv'), '[output] should be assigned and endswith [.csv]'

    db_config = load_config_from_db_conf(option.db)

    # output = datetime.datetime.now().strftime(option.output)
    # do_export(db_config, output, table=option.table, sql=option.sql, header=option.header)
    do_new_file(db_config, option.file, option.inc_date)
    do_exec(db_config, option.file, option.inc_date)

