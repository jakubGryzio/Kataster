import re

def reader():
    path = r'C:\Users\01150208\OneDrive - Politechnika Warszawska\Pliki_Kuby\Studia\III_ROK\Kataster\Kataster\ćwiczenie1\kontury_dane.txt'
    with open(path, 'r', encoding='utf-8') as file:
        file_line = [line.strip() for line in file.readlines()]
    contours = [file_line[i + 1] for i in range(1, len(file_line) - 1) if file_line[i] == '' and file_line[i + 1] != '']
    contours.append(file_line[0])
    assert len(contours) == 194
    return contours

def containsBackSlash(con):
    return con.count('/') == 1

def matchDigitsBeforeBackSlash(con):
    return re.search('^\d{1,3}-\d{1,4}', con)

def syntaxValidator(contours):
    counter = 0
    for contour in contours:
        if containsBackSlash(contour):
            counter += 1
            print(f"{counter}: {contour}")
        # if not matchDigitsBeforeBackSlash(contour):
        #     counter += 1
        #     print(f"{counter}: {contour}")


if __name__ == "__main__":
    data = reader()
    syntaxValidator(data)
