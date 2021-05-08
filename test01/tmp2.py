import subprocess
import time
def run_shell(cmd):
    print("""cmd: {}""".format(cmd))
    sub = subprocess.Popen(""" %s """ % cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='.', shell=True)
    outs = []
    while sub.poll() is None:
        lines = sub.stdout.readlines()
        lines = [line.decode('utf-8', 'ignore') for line in lines]
        outs = outs + lines
        time.sleep(1)
    return sub.returncode, ''.join(outs)


select_sql=f'SELECT * FROM test.cs_01 c ;'
cmd = f"""
    
    l=`mysql -plocalhost -u root -proot -Ne " {select_sql} commit;"`;echo $
    """
(status, output) = run_shell(cmd)
#print(output)
if status != 0:
    exit(1)
