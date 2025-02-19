import argparse



parser = argparse.ArgumentParser(
        prog='Hello',
        description='This program will say hello to you'
)
parser.add_argument('name', help='your name')
args = parser.parse_args()

def printName(name):
    return print(f"Hello {name}!")

if __name__ == "__main__":
    printName(args.name)
