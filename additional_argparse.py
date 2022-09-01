import argparse

my_parser = argparse.ArgumentParser(
    prog="my_program",
    usage="%(prog)s [options] path",
    description="List the content of a folder",
)
my_parser.add_argument("test", nargs="?", help="test")
my_parser.add_argument('additional', nargs=argparse.REMAINDER)

args = my_parser.parse_args()

print(*args.additional)

print("Test")