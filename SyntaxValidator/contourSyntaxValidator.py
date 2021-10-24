import re

def reader():
    try:
        path = r'C:\Users\01150208\OneDrive - Politechnika Warszawska\Pliki_Kuby\Studia\III_ROK\Kataster\Kataster\ćwiczenie1\Kontury_eksport_dz.txt'
        with open(path, 'r', encoding='ansi') as file:
            file_line = [line.strip() for line in file.readlines()]
        contours = [file_line[i + 1] for i in range(1, len(file_line) - 1) if file_line[i] == '' and file_line[i + 1] != '']
        contours.append(file_line[0])
        return contours
    except Exception:
        print("Błąd wczytywanego pliku!")

def fullSyntaxValid(con):
    return re.fullmatch(r'^\d{1,3}-\d+/[A-Za-zŁ]{1,5}(-[A-Za-z]{1,5})?$', con)

def containsBackSlash(contour):
    return re.search(r"(\d|\w)/\w+", contour)

def hasDigitsBeforeBackSlash(contour):
    return re.search(r'^\d{1,3}-\d+(/|\s)?', contour)

def hasOFU(con):
    return re.search(r"(\w|\W)(([A-HJ-UW-Z]|[Ł])([a-z]{1,2})?|dr)($|\W)", con)

def hasValidOFU(con, ofu):
    pattern = hasOFU(con)
    if pattern:
        return pattern.group(2) in ofu
    return True

def hasOZUWithOZK(con):
    return re.search(r'(\W)?([A-HJ-UW-ZŁ]([a-z]{1,2})?)([IV]{1,3}[a-z]?)', con)

def hasOZU(con):
    return re.search(r'-([A-HJ-UW-ZŁ]([a-z]{1,2})?)$', con)

def hasValidOZU(con, ozu):
    ozuWithOZK = hasOZUWithOZK(con)
    ozuWithoutOZK = hasOZU(con)
    if ozuWithOZK:
        return ozuWithOZK.group(2) in ozu
    if ozuWithoutOZK:
        return ozuWithoutOZK.group(1) in ozu
    return True

def hasOZK(con):
    return re.search(r'([IV]{1,3}[a-z]?)', con)

def hasValidOZUOZK(con, properOZK):
    ozu = hasOZUWithOZK(con)
    ozk = hasOZK(con)
    if ozu and ozk:
        if ozu.group(2) != 'R':
            return ozk.group(0) in properOZK[0]
        else:
            return ozk.group(0) in properOZK[1]
    return True

def hasValidOFUOZU(con, ofuOZU):
    ofu = hasOFU(con)
    ozu = hasOZUWithOZK(con)
    if ofu and ozu:
        if ozu.group(2) not in ofuOZU:
            return False
        else:
            return ofu.group(2) in ofuOZU[ozu.group(2)]
    return True

def hasDash(contour):
    ofu = hasOFU(contour)
    ozu = hasOZUWithOZK(contour)
    if ofu and ozu:
        return re.search(f'{ofu.group(2)}-{ozu.group(2)}', contour)
    return True

def syntaxValidator(contour):
    ofu = ('R', 'S', 'Ł', 'Ps', 'Br', 'Wsr', 'W', 'Lzr', 'Ls', 'Lz',
           'B', 'Ba', 'Bi', 'Bp', 'Bz', 'K', 'dr', 'Tk', 'Ti', 'Tp', 'N',
           'Wp', 'Ws', 'Tr',)
    ozu = ('R', 'Ł', 'Ps', 'Ls', 'Lz', 'N')
    ozk = (('I', 'II', 'III', 'IV', 'V', 'VI'),
           ('I', 'II', 'IIIa', 'IIIb', 'IVa', 'IVb', 'V', 'VI', 'VIz'))
    ofuOZU = {"R": ['R', 'S', 'Br', 'Wsr', 'W', 'Lzr'],
              "Ł": ['Ł', 'S', 'Br', 'Wsr', 'W', 'Lzr'],
              "Ps": ['Ps', 'S', 'Br', 'Wsr', 'W', 'Lzr'],
              "Ls": ['Ls', 'W'],
              "Lz": ['Lz', 'W']}
    valid = True
    if not containsBackSlash(contour):
        valid = False
        print(f"Błąd składniowy (brak '/'): {contour}")
    if not hasDigitsBeforeBackSlash(contour):
        valid = False
        print(f"Błąd składniowy (numer obrębu i numer konturu): {contour}")
    if not hasValidOFU(contour, ofu):
        valid = False
        print(f"Brak poprawnego OFU: {contour}")
    if not hasValidOZU(contour, ozu):
        valid = False
        print(f"Brak poprawnego OZU: {contour}")
    if not hasValidOZUOZK(contour, ozk):
        valid = False
        print(f"Brak poprawnego oznaczenia OZK: {contour}")
    if not hasValidOFUOZU(contour, ofuOZU):
        valid = False
        print(f"Brak poprawnej relacji OFU i OZU: {contour}")
    if not hasDash(contour):
        valid = False
        print(f"Błąd składniowy (brak '-' pomiędzy OFU i OZU): {contour}")
    if valid and not fullSyntaxValid(contour):
        valid = False
        print(f"Inny błąd składniowy: {contour}")
    return valid

def getInvalidContour(contours):
    invalidContours = [contour for contour in contours if not syntaxValidator(contour)]
    for i, contour in enumerate(invalidContours):
        print(f"{i + 1}: {contour}")
