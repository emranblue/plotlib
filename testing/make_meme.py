from video_writer import VideoWriter
from argparse import ArgumentParser,ArgumentError
def get_cli():
    parser=ArgumentParser()
    try:
        parser.add_argument('-fl','--video_file',default="jara-abir.mp4",help="Target Video file")
        parser.add_argument('-c','--caption',default="jara-abir flirting moment",help="MEME caption")
        parser.add_argument('-d','--direction',default='down',help='Either up or Down...where to write caption')
        parser.add_argument('-i','--invert',action='store_true',default=False,help='invert the video')
        parser.add_argument('-f','--font',default="Courier New",help='font of meme')
        parser.add_argument('-fs','--font_size',default=36,type=int,help="font size")
        parser.add_argument('-fc','--font_color',default=[1,1,1,1],type=list,help="font color,must be a list,values from 0 to 1")
        parser.add_argument('-b','--border',default=30,type=int,help="side border of caption")
        return parser.parse_args()
    except ArgumentError as err:
        print(str(err))
        sys.exit(2)


if __name__=='__main__':
    args=get_cli()
    writer=VideoWriter()
    assert args.video_file is not None
    writer.meme(args.video_file,
    args.caption,
    invert=args.invert,
    direction=args.direction,
    font=args.font,
    font_size=args.font_size,
    color=args.font_color,
    border=args.border
    )
