import sys
import os

args = sys.argv
arg = args[1]
prog_files = args[0]

host = os.environ.get('HOST')

print(f'hello {arg} from {prog_files}')
print(f'connecting to {host}')