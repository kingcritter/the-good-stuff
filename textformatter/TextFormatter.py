#frontend

import formatter
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--image", dest="image",
                  help="specifiy input image", metavar="IMAGE")
parser.add_option("-t", "--text", dest="text", 
                  help="specify text file", metavar="TEXTFILE")
parser.add_option("-r", "--resolution", dest="resolution",
                  type="int", nargs=2, default=(5, 10),
                  help="specify resolution of characters, x and y", metavar="X Y")
parser.add_option("--html",
                  action="store_true", dest="html", default=False,
                  help="output is html with color codes")
parser.add_option("-f", "--file", dest="output",
                  help="specify output file", metavar="OUTPUTFILE")


(options, args) = parser.parse_args()

# text and image options are mandatory, so we check for them:
if options.image == None:
    print("Must specify image file with -i option")
    exit()
if options.text == None:
    print("Must specify text file with -t option")
    exit()

# send the image file and character resolution to the formatter,
# get a matrix of RGBA values
matrix = formatter.getMatrix(options.resolution, options.image)


f = open(options.text, 'r')
fullText = f.readlines()
fullText = "".join(fullText)

#out put to colored HTML or plain text? 
if options.html:
    formattedText = formatter.formatHTML(matrix, fullText)
else: 
    formattedText = formatter.formatRawText(matrix, fullText)

if options.output:
    outfile = open(options.output, 'w')
    outfile.write(formattedText)
    outfile.close()
else:
    print(formattedText)