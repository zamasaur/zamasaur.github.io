
import glob
import os
import json
import re
from PyPDF2 import PdfReader


def getNormalizedTxt(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    # remove Materia: description
    regex = r"(Materia: .*)$"
    subst = ""
    text = re.sub(regex, subst, text, 0, re.MULTILINE)

    # remove Contenuto: description
    regex = r"(Contenuto: .*)$"
    subst = ""
    text = re.sub(regex, subst, text, 0, re.MULTILINE)

    # remove Pag. X
    regex = r"(Pag. \d*)$"
    subst = ""
    text = re.sub(regex, subst, text, 0, re.MULTILINE)

    # remove Copyright
    regex = r"(Copyright © OCF - Organismo di vigilanza e tenuta dell'albo unico dei Consulenti Finanziari)"
    subst = ""
    text = re.sub(regex, subst, text, 0, re.MULTILINE)

    # remove multiple newline
    regex = r"\n(?=(\n))"
    subst = ""
    text = re.sub(regex, subst, text, 0, re.MULTILINE)

    # remove new line
    regex = r"\n(?!(A: )|(B: )|(C: )|(D: )|(Livello: )|(Sub-contenuto: )|(Pratico: ))"
    subst = " "
    text = re.sub(regex, subst, text, 0, re.MULTILINE)

    # new line after Pratico:
    regex = r"(Pratico: )(..)"
    subst = "\\1\\2\\nDomanda: "
    text = re.sub(regex, subst, text, 0, re.MULTILINE)

    # add first Domanda:
    text = "Domanda: "+text

    # remove last Domanda:
    regex = r"^(Domanda: )$"
    subst = ""
    text = re.sub(regex, subst, text, 0, re.MULTILINE)

    # remove ending new line
    if text[len(text)-1] == "\n":
        text = text[0:len(text)-1]

    # remove wrong aswers
    regex = r"(B: .*)$"
    subst = ""
    text = re.sub(regex, subst, text, 0, re.MULTILINE)
    regex = r"(C: .*)$"
    subst = ""
    text = re.sub(regex, subst, text, 0, re.MULTILINE)
    regex = r"(D: .*)$"
    subst = ""
    text = re.sub(regex, subst, text, 0, re.MULTILINE)

    # remove multiple newline
    regex = r"\n(?=(\n))"
    subst = ""
    text = re.sub(regex, subst, text, 0, re.MULTILINE)

    # remove leading number
    regex = r"^(Domanda: )([\d |\W]{0,})"
    subst = "Domanda: "
    text = re.sub(regex, subst, text, 0, re.MULTILINE)

    return text


def getData(text, scope=""):
    list = []
    count = 0

    for line in text.split('\n'):
        modulus = count % 5
        if (modulus == 0):
            list.append({
                "question": line[-len(line)+len("Domanda: "):],
                "answer": "",
                "metadata": {
                    "scope": scope,
                    "level": 1,
                    "subcontent": "",
                    "isPractical": False
                }
            })
        elif (modulus == 1):
            list[count//5]["answer"] = line[-len(line)+len("A: "):]
        elif (modulus == 2):
            list[count //
                 5]["metadata"]["level"] = int(line[-len(line)+len("Livello: "):])
        elif (modulus == 3):
            list[count //
                 5]["metadata"]["subcontent"] = line[-len(line)+len("Sub-contenuto: "):]
        else:
            list[count//5]["metadata"]["isPractical"] = False if line[-len(
                line)+len("Pratico: "):] == "NO" else True
        count += 1

    return list


print("\n")

root = './resources/pdf/repaired'
dirList = [item for item in os.listdir(
    root) if os.path.isdir(os.path.join(root, item))]

list = {}

for dir in dirList:
    list[dir[2:]] = []
    fileList = glob.glob("./resources/pdf/repaired/"+dir+"/*.pdf")
    for file in fileList:
        print(file[len(root)+1:])
        scope = os.path.basename(file)[0:len(os.path.basename(file))-4]
        list[dir[2:]] += getData(getNormalizedTxt(file), scope)

file = open(r"./js/data.json", "w", encoding='utf8')
file.writelines(json.dumps(list, ensure_ascii=False, indent=3))

print("\n")

count = 0
for item in list:
    count += len(list[item])
    print(item+" "+str(len(list[item])))

print("total "+str(count))
print("\n")
print("done.")
print("\n")
