from video_writer import VideoWriter
from argparse import ArgumentParser,ArgumentError
def get_cli():
    parser=ArgumentParser()
    try:
        parser.add_argument('-fl','--video_file',help="Target Video file")
        parser.add_argument('-c','--caption',help="MEME caption")
        parser.add_argument('-d','--direction',default='down',help='Either up or Down...where to write caption')
        parser.add_argument('-i','--invert',action='store_true',default=False,help='invert the video')
        parser.add_argument('-f','--font',default="Courier New",help='font of meme')
        return parser.parse_args()
    except ArgumentError as err:
        print(str(err))
        sys.exit(2)


if __name__=='__main__':
    args=get_cli()
    writer=VideoWriter()
    assert args.video_file is not None
    writer.meme(args.video_file,args.caption,invert=args.invert,direction=args.direction,font=args.font)
