def read_csv(file_name):
    with open(file_name, "r") as file:
        for line in file:
            yield line.split(",")
            