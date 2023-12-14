import optparse
import subprocess
import time
from datetime import datetime

def run_shell(cmd):
    sub = subprocess.Popen(""" %s """ % cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='.', shell=True)
    outs = []
    while sub.poll() is None:
        lines = sub.stdout.readlines()
        lines = [line.decode('utf-8', 'ignore') for line in lines]
        outs = outs + lines
        time.sleep(1)
    return sub.returncode, ''.join(outs)

def export_csv(table_name, partition_spec, csv_file_name, timeout):
    while datetime.now().hour <= timeout:
        cmd_check = f'odpscmd -e "desc {table_name} partition (dt={partition_spec})"'
        print(cmd_check)
        (status, output) = run_shell(cmd_check)
        if status != 0 and 'Partition not found' in output:
            print(f'{table_name} Partition {partition_spec} does not exists. Waiting for 10 min...')
            time.sleep(10)
        elif status == 0:
            print(f'{table_name} exists partition {partition_spec}\nstart exporting {csv_file_name}')
            cmd_export = f'odpscmd -e "tunnel download -cf true -h true {table_name}/dt={partition_spec} {csv_file_name}_{partition_spec}.csv; "'
            print(cmd_export)
            (status, output) = run_shell(cmd_export)
            if status == 0: 
                print(output)    
                print(f'Successfully exported {csv_file_name}')
                exit(0)
            else:
                print(f'An error occurred while exporting {csv_file_name}:{output}')
                exit(1)
        else: 
            print(f"An error occurred while exec cmd {cmd_check}")
            exit(1)
    print(f'Export operation has exceeded the timeout. Exiting...')



parser = optparse.OptionParser()
parser.add_option('-t', '--table', dest='table', help='table name')
parser.add_option('-p', '--partition', dest='partition', help='partition specification')
parser.add_option('-f', '--file-name', dest='file_name', help='CSV file name')
parser.add_option('-H', '--hour', dest='hour', type='int', default=22)
(options, args) = parser.parse_args()

if not options.table or not options.file_name:
    parser.error('Required parameters are missing.')


export_csv(options.table, options.partition, options.file_name, options.hour)
