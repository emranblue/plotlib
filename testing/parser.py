from argparse import ArgumentParser,ArgumentError
import sys
def get_cli():
    parse=ArgumentParser()
    try:
        parse.add_argument('-a','--plot',action='store_true',default=True,help="Simple plotting")
        parse.add_argument('-g','--grid',action='store_true',help="grid setting")
        parse.add_argument('-ax','--axis',action='store_true',help="set axis")
        parse.add_argument('-f','--function',help="Fucntion",default='sin(x)',type=str)
        parse.add_argument('-d','--lower_limit',default='-5*pi',help="lower limit of function")
        parse.add_argument('-u','--upper_limit',default='5*pi',help="upper limit")
        parse.add_argument('-fx','--function_x',help="Perametric's first function")
        parse.add_argument('-fy','--function_y',help="Perametric's second function")
        parse.add_argument('-dir','--dir_name',help="directory name")
        parse.add_argument('-file','--file_name',help="file name")
        parse.add_argument('-b','--pera',action='store_true',help="Perametric function plotting")
        parse.add_argument('-c','--polar',help="Polar function plotting")
        parse.add_argument('--rm',action='store_true',help="Delete selected file")
        parse.add_argument('-ls','--list',action='store_true',help="list out the file")
        exclusive=parse.add_mutually_exclusive_group()
        exclusive.add_argument('-v','--svg',action='store_true',help="file format")
        exclusive.add_argument('-r','--png',action='store_true',help="file format")
        return parse.parse_args()
    except ArgumentError as err:
        print(str(err))
        sys.exit(2)
