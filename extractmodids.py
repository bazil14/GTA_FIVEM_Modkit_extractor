from bs4 import BeautifulSoup
from pathlib import Path
import csv
import sys

modkits = []
binary_list = []
#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

if len(sys.argv) > 1:
    for file in Path(sys.argv[1]).rglob('carcols*.meta'):
        data = open(file, 'r').read()

        soup = BeautifulSoup(data, "lxml")
        # print(soup.prettify())

        print("Reading Meta file: " + str(file))
        kits = soup.find("kits")
        if kits is not None:
            id_list = kits.find_all("id")
            kitnames = kits.find_all("kitname")
            for index, item in enumerate(id_list):
                id = int((id_list[index].get("value")))
                mod = (kitnames[index].text)

                modkits.append([id, mod,file])

    modkits = sorted(modkits, key=lambda x: x[0])
    print("======== Sorted Modkit list ========")
    print(modkits)

    with open(sys.argv[1] + '/modkits.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        previous_item = ["", ""]
        i = 0
        for item in modkits:
            if item[1] == previous_item[1]:
                pass
            else:
                if i <= 1000:
                    if item[0] != i:
                        min = i
                        for x in range(min, item[0]):
                            numStr = bin(int(i))[2:]
                            modkit_binary = numStr.zfill(20)
                            writer.writerow([modkit_binary] + [i])
                            i +=1
                numStr = bin(int(item[0]))[2:]
                modkit_binary = numStr.zfill(20)
                binary_list.append(modkit_binary[-11:])
                if item[0] == previous_item[0]:
                    writer.writerow([modkit_binary] + [item[0]] + [item[1]] +[item[2]]+ ["--- DUPLICATE"] )
                else:
                    writer.writerow([modkit_binary] + [item[0]] + [item[1]]+[item[2]])
                    i += 1
                previous_item = item


    print("======== Removing duplicate entries (not clashing entries) ========")
    Duplicates = set([x for x in binary_list if binary_list.count(x) > 1])
    print("======== Binary list of results ========")
    print(Duplicates)
    print("======== MOD KIT CSV CREATED ========")


else:
    print("No arguments specified, Please give a location of where to look :)")
