import contourSyntaxValidator as con

if __name__ == "__main__":
    contours = con.reader()
    con.getInvalidContour(contours)
