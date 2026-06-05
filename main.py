from sparser import Code_Parser


def main():
    parser = Code_Parser("data.txt")
    parser.parse()
    print(parser.get_value("f"))


if __name__ == "__main__":
    main()
