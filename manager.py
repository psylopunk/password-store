from getpass import getpass
from hashlib import md5
from base64 import b64encode
import pyperclip
import sys, os

def invalid_usage(err):
    raise Exception("""Invalid usage
        
Syntax: python3 manager.py <command> <args>

Commands:
    save <name>
    read
    del <name>
    list""")

def read_list():
    if '.ps_list' not in os.listdir('.'):
        write_list([])

    with open('.ps_list', 'r') as file:
        return file.read().splitlines()

def write_list(ps_list):
    with open('.ps_list', 'w') as file:
        file.write('\n'.join(ps_list))

def update_list(new_entries):
    passwords = [*read_list(), *new_entries]
    write_list(passwords)

def main():
    args = sys.argv
    if len(args) <= 1: # Not enough arguments. Add command name
        return invalid_usage(0)

    command = sys.argv[1]
    if command in ['save', 'del'] and len(sys.argv) < 3:
        return invalid_usage(1)

    if command == 'save':
        comment = input('Enter comment for this password: ')
        update_list([sys.argv[2] + (f' – {comment}' if comment else '')])
        print('Successfully saved to .ps_list')
    elif command == 'read':
        message = getpass('Master-password: ')
        hash = md5(
            message.encode('utf8')
        ).digest()
        password = b64encode(
            hash
        ).decode().replace('=', '')
        pyperclip.copy(password)
        print('Password copied to clipboard')
    elif command == 'del':
        write_list([e for e in read_list() if e.find(sys.argv[2]) != 0])
        print('Password removed from the store')
    elif command == 'list':
        print('Known passwords:')
        print('\n'.join(read_list()))
    else:
        return invalid_usage(1)


if __name__ == '__main__':
    sys.tracebacklimit = 0
    main()