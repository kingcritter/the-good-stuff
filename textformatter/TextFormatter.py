#frontend

import formatter
import argparse

parser = argparse.ArgumentParser(description='Formatt text to image')
parser.add_argument("-i", "--image", dest="image",
                  help="specifiy input image", metavar="IMAGE")
parser.add_argument("-t", "--text", dest="text", 
                  help="specify text file", metavar="TEXTFILE")
parser.add_argument("-r", "--resolution", dest="resolution",
                  type=int, nargs=2, default=(5, 10),
                  help="specify resolution of characters, x and y", metavar=("X", "Y"))
parser.add_argument("--html",
                  action="store_true", dest="html", default=False,
                  help="output is html with color codes")
parser.add_argument("-f", "--file", dest="output",
                  help="specify output file", metavar="OUTPUTFILE")
parser.add_argument("-s", "--nospaces", dest="spacesKept", action="store_false",
                  default=True,
                  help="Don't include spaces in output",)


args = parser.parse_args()

# text and image options are mandatory, so we check for them:
if args.image == None:
    print("Must specify image file with -i option")
    exit()
if args.text == None:
    print("Must specify text file with -t option")
    exit()

# send the image file and character resolution to the formatter,
# get a matrix of RGBA values
matrix = formatter.getMatrix(args.resolution, args.image)


f = open(args.text, 'r')
fullText = f.readlines()
fullText = "".join(fullText)

#out put to colored HTML or plain text? 
if args.html:
    formattedText = formatter.formatHTML(matrix, fullText, args.spacesKept)
else: 
    formattedText = formatter.formatRawText(matrix, fullText, args.spacesKept)

if args.output:
    outfile = open(args.output, 'w')
    outfile.write(formattedText)
    outfile.close()
else:
    print(formattedText)