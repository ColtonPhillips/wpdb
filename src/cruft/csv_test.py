import csv

def main():
    with open('test.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            print ','.join(row)


if __name__ == "__main__":
    main()