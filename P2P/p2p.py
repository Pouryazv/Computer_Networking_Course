import argparse
from server.serve import serve_files
from client.receive import receive_file

def main():
    parser = argparse.ArgumentParser(prog='p2p', description='P2P Command Line Application')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create the 'receive' command
    receive_parser = subparsers.add_parser('receive', help='Receive file')
    receive_parser.add_argument('filename', type=str, help='Name of the file to receive')
    receive_parser.set_defaults(func=receive_file)

    # Create the 'serve' command
    serve_parser = subparsers.add_parser('serve', help='Serve files')
    serve_parser.add_argument('-filepaths', nargs='+', type=str, help='List of file paths to serve')
    serve_parser.set_defaults(func=serve_files)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)

if __name__ == '__main__':
    main()
