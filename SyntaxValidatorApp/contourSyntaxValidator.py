import re

def reader(path):
    try:
        with open(path, 'r', encoding='ansi') as file:
            file_line = [line.strip() for line in file.readlines()]
        contours = [file_line[i + 1] for i in range(1, len(file_line) - 1) if file_line[i] == '' and file_line[i + 1] != '']
        contours.append(file_line[0])
        return contours
    except Exception:
        print("Błąd wczytywanego pliku!")

def fullSyntaxValid(con):
    return re.fullmatch(r'^\d{1,3}-\d+/[A-Za-zŁ]{1,5}(-[A-Za-zŁ]{1,5})?$', con)

def containsBackSlash(contour):
    return re.search(r"(\d|\w)/\w+", contour)

def hasDigitsBeforeBackSlash(contour):
    return re.search(r'^\d{1,3}-\d+(/|\s)?', contour)

def hasOFU(con):
    return re.search(r"(\w|\W)(([A-HJ-UW-Z]|[Ł])([a-z]{1,2})?|dr)$", con)

def hasOFUwithOZU(con):
    return re.search(r"(\w|\W)(([A-HJ-UW-Z]|[Ł])([a-z]{1,2})?|dr)-", con)

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
    ofu = hasOFUwithOZU(con)
    ozu = hasOZUWithOZK(con)
    if ofu and ozu:
        if ozu.group(2) not in ofuOZU:
            return False
        else:
            return ofu.group(2) in ofuOZU[ozu.group(2)]
    return True

def hasDash(contour):
    ofu = hasOFUwithOZU(contour)
    ozu = hasOZUWithOZK(contour)
    if ofu and ozu:
        return re.search(f'{ofu.group(2)}-{ozu.group(2)}', contour)
    return True

def syntaxValidator(contour):
    ofu = ('B', 'Ba', 'Bi', 'Bp', 'Bz', 'K', 'dr', 'Tk', 'Ti', 'Tp', 'N', 'Wp', 'Ws', 'Tr')
    ozu = ('R', 'Ł', 'Ps', 'Ls', 'Lz')
    ozk = (('I', 'II', 'III', 'IV', 'V', 'VI'),
           ('I', 'II', 'IIIa', 'IIIb', 'IVa', 'IVb', 'V', 'VI', 'VIz'))
    ofuOZU = {"R": ['R', 'S', 'Br', 'Wsr', 'W', 'Lzr'],
              "Ł": ['Ł', 'S', 'Br', 'Wsr', 'W', 'Lzr'],
              "Ps": ['Ps', 'S', 'Br', 'Wsr', 'W', 'Lzr'],
              "Ls": ['Ls', 'W'],
              "Lz": ['Lz', 'W']}
    valid = True
    syntaxError = ""
    modelError = ""
    if not containsBackSlash(contour):
        valid = False
        # print(f"Błąd składniowy (brak '/'): {contour}")
        syntaxError += f"Błąd składniowy (brak '/'): {contour}\n\n"
    if not hasDigitsBeforeBackSlash(contour):
        valid = False
        # print(f"Błąd składniowy (numer obrębu-numer konturu): {contour}")
        syntaxError += f"Błąd składniowy (numer obrębu-numer konturu): {contour}\n\n"
    if not hasValidOFU(contour, ofu):
        valid = False
        # print(f"Brak poprawnego OFU: {contour}")
        modelError += f"Brak poprawnego OFU: {contour}\n\n"
    if not hasValidOZU(contour, ozu):
        valid = False
        # print(f"Brak poprawnego OZU: {contour}")
        modelError += f"Brak poprawnego OZU: {contour}\n\n"
    if not hasValidOZUOZK(contour, ozk):
        valid = False
        # print(f"Brak poprawnego oznaczenia OZK: {contour}")
        modelError += f"Brak poprawnego oznaczenia OZK: {contour}\n\n"
    if not hasValidOFUOZU(contour, ofuOZU):
        valid = False
        # print(f"Brak poprawnej relacji OFU i OZU: {contour}")
        modelError += f"Brak poprawnej relacji OFU i OZU: {contour}\n\n"
    if not hasDash(contour):
        valid = False
        # print(f"Błąd składniowy (brak '-' pomiędzy OFU i OZU): {contour}")
        syntaxError += f"Błąd składniowy (brak '-' pomiędzy OFU i OZU): {contour}\n\n"
    if valid and not fullSyntaxValid(contour):
        valid = False
        # print(f"Inny błąd składniowy: {contour}")
        syntaxError += f"Inny błąd składniowy: {contour}\n\n"
    return valid, syntaxError, modelError

def getInvalidContour(contours):
    invalidContours = []
    invalidContour, syntaxError, modelError = "", "", ""
    for contour in contours:
        valid, syntax, model = syntaxValidator(contour)
        if not valid:
            invalidContours.append(contour)
            syntaxError += syntax
            modelError += model
            invalidContour += f"{contour}\n\n"
    return len(invalidContours), invalidContour, syntaxError, modelError

