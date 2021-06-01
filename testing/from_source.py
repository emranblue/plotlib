from from_video import ApplyMethodToVideo
class FromSource(ApplyMethodToVideo):
    CONFIG={
            'method':lambda m:m,##just do nothing
            'source':0,
            }
    def __init__(self,source=0,fps=8,**kwargs):
        self.fps=fps
        ApplyMethodToVideo.__init__(self,filename=str(source),source=source,**kwargs)
        try:
            print("\n\nTo stop press ctrl+c\n\n")
            self.make()
        except:#stop for any types of error
            self.cap.release()
            self.close()
            self.processbar.close()
            self.print_end()
            
            
            
