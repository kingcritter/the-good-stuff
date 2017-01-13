from PIL import Image

# accepts: resolution of characters as xy tuple
#          image path
# returns: two dimensional array of 1s and 0s
def getMatrix(charSize, image):
    im = Image.open(image)
    width, height = im.size

    charWidth = charSize[0]
    charHeight = charSize[1]

    textCols = width // charWidth
    textRows = height // charHeight

    matrix = [[0 for i in range(textCols)] for j in range(textRows)]

    for col in range(0, textCols):
        for row in range(0, textRows):
            matrix[row][col] = getAverageRGBA((col, row), charSize, im)

    return matrix

# caret is a tuple, an xy pair that maps to a spot
# on the output matrix. We translate this to a spot
# on the input image and search a block coresponding 
# to the size given by charSize. We calculate the 
# average RGBA from the reigon and return it as a tuple.
def getAverageRGBA(caret, charSize, im):
    topleft = [None, None] 
    topleft[0] = caret[0] * charSize[0]
    topleft[1] = caret[1] * charSize[1]

    average = [0, 0, 0, 0]

    for x in range(topleft[0], topleft[0] + charSize[0]):
        for y in range(topleft[1], topleft[1] + charSize[1]):
            RGBA = im.getpixel((x, y))
            average[0] += RGBA[0]
            average[1] += RGBA[1]
            average[2] += RGBA[2]
            average[3] += RGBA[3]

    # n = total number of pixels
    n = charSize[0] * charSize[1]
    for i in range(len(average)):
        average[i] //= n

    return tuple(average)

def formatRawText(matrix, text, spacesKept=True):
    formattedString = ""
    textLength = len(text)
    textIndex = 0

    for row in matrix:
        for pixel in row: 
            if pixel[3] < 127: #less than half transparent
                formattedString += " "
            else:
                try:
                    if spacesKept == False:
                        while text[textIndex] == "\n" or text[textIndex] == " " and textIndex < textLength:
                            textIndex += 1
                    if text[textIndex] == "\n" or text[textIndex] == " ":
                        formattedString += " "
                    elif text[textIndex] != " " and text[textIndex] != "\n":
                        formattedString += text[textIndex]
                    # now, if spacesKept=False and it was a space or newline, we'll have skipped it
                    textIndex += 1
                # If we run out of text, fill in with asterisks
                except IndexError:
                    formattedString += "*"
        # at the end of the row
        formattedString += "\n"

    return formattedString

def formatHTML(matrix, text):
    formattedString = ""
    textLength = len(text)
    textIndex = 0

    formattedString += "<span style='font-family : monospace'>"

    for row in matrix:
        for pixel in row: 
            if pixel[3] < 127:
                formattedString += "&nbsp"
            else:
                try:
                    if text[textIndex] == "\n" or text[textIndex] == " " and spacesKept:
                        formattedString += "&nbsp"
                    else:
                        temp = ""
                        temp += "<span style='color : rgb("
                        temp += str(pixel[0]) + "," + str(pixel[1]) + ","
                        temp += str(pixel[2]) + ")'>"
                        if text[textIndex] == " ":
                            temp += "&nbsp"
                        else:
                            temp += text[textIndex]
                        temp += "</span>"
                        formattedString += temp
                    textIndex += 1
                except IndexError:
                    formattedString += "*"
        # at the end of the row
        formattedString += "<br />"

    formattedString += "</span>"

    return formattedString