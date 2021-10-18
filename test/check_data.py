# checking .txt data file: count of items in row and column


def check_data(input_file_name: str):
    file = open(input_file_name, "r")

    # print file header
    preamble = file.readline()
    print("preamble: " + preamble)
    print("item count: " + str(len(preamble.split())))

    idx = 1
    # check each line
    while True:
        line = file.readline()

        # file has read
        if not line:
            break
        print("line " + str(idx) + "; items count: " + str(len(line.split())))
        idx += 1
    file.close()


def main():
    check_data("../data/data.txt")


if __name__ == "__main__":
    main()
