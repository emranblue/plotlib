import os,sys
import subprocess as sp

import proglog,warning,decorator





@decorator.decorator
def outplace(f, clip, *a, **k):
    """ Applies f(clip.copy(), *a, **k) and returns clip.copy()"""
    newclip = clip.copy()
    f(newclip, *a, **k)
    return newclip

@decorator.decorator
def convert_masks_to_RGB(f, clip, *a, **k):
    """ If the clip is a mask, convert it to RGB before running the function """
    if clip.ismask:
        clip = clip.to_RGB()
    return f(clip, *a, **k)

@decorator.decorator
def apply_to_mask(f, clip, *a, **k):
    """ This decorator will apply the same function f to the mask of
        the clip created with f """
        
    newclip = f(clip, *a, **k)
    if getattr(newclip, 'mask', None):
        newclip.mask = f(newclip.mask, *a, **k)
    return newclip



@decorator.decorator
def apply_to_audio(f, clip, *a, **k):
    """ This decorator will apply the function f to the audio of
        the clip created with f """
        
    newclip = f(clip, *a, **k)
    if getattr(newclip, 'audio', None):
        newclip.audio = f(newclip.audio, *a, **k)
    return newclip


@decorator.decorator
def requires_duration(f, clip, *a, **k):
    """ Raise an error if the clip has no duration."""
    
    if clip.duration is None:
        raise ValueError("Attribute 'duration' not set")
    else:
        return f(clip, *a, **k)



@decorator.decorator
def audio_video_fx(f, clip, *a, **k):
    """ Use an audio function on a video/audio clip
    
    This decorator tells that the function f (audioclip -> audioclip)
    can be also used on a video clip, at which case it returns a
    videoclip with unmodified video and modified audio.
    """
    
    if hasattr(clip, "audio"):
        newclip = clip.copy()
        if clip.audio is not None:
            newclip.audio =  f(clip.audio, *a, **k)
        return newclip
    else:
        return f(clip, *a, **k)

def preprocess_args(fun,varnames):
    """ Applies fun to variables in varnames before launching the function """
    
    def wrapper(f, *a, **kw):
        if hasattr(f, "func_code"):
            func_code = f.func_code # Python 2
        else:
            func_code = f.__code__ # Python 3
            
        names = func_code.co_varnames
        new_a = [fun(arg) if (name in varnames) else arg
                 for (arg, name) in zip(a, names)]
        new_kw = {k: fun(v) if k in varnames else v
                 for (k,v) in kw.items()}
        return f(*new_a, **new_kw)
    return decorator.decorator(wrapper)


def convert_to_seconds(varnames):
    "Converts the specified variables to seconds"
    return preprocess_args(cvsecs, varnames)



@decorator.decorator
def add_mask_if_none(f, clip, *a, **k):
    """ Add a mask to the clip if there is none. """        
    if clip.mask is None:
        clip = clip.add_mask()
    return f(clip, *a, **k)



@decorator.decorator
def use_clip_fps_by_default(f, clip, *a, **k):
    """ Will use clip.fps if no fps=... is provided in **k """
    
    def fun(fps):
        if fps is not None:
            return fps
        elif getattr(clip, 'fps', None):
            return clip.fps
        raise AttributeError("No 'fps' (frames per second) attribute specified"
                " for function %s and the clip has no 'fps' attribute. Either"
                " provide e.g. fps=24 in the arguments of the function, or define"
                " the clip's fps with `clip.fps=24`" % f.__name__)


    if hasattr(f, "func_code"):
        func_code = f.func_code # Python 2
    else:
        func_code = f.__code__ # Python 3
        
    names = func_code.co_varnames[1:]
    
    new_a = [fun(arg) if (name=='fps') else arg
             for (arg, name) in zip(a, names)]
    new_kw = {k: fun(v) if k=='fps' else v
             for (k,v) in k.items()}

    return f(clip, *new_a, **new_kw)












def sys_write_flush(s):
    """ Writes and flushes without delay a text in the console """
    # Reason for not using `print` is that in some consoles "print" 
    # commands get delayed, while stdout.flush are instantaneous, 
    # so this method is better at providing feedback.
    # See https://github.com/Zulko/moviepy/pull/485
    sys.stdout.write(s)
    sys.stdout.flush()


def verbose_print(verbose, s):
    """ Only prints s (with sys_write_flush) if verbose is True."""
    if verbose:
        sys_write_flush(s)


def subprocess_call(cmd, logger='bar', errorprint=True):
    """ Executes the given subprocess command.
    
    Set logger to None or a custom Proglog logger to avoid printings.
    """
    logger = proglog.default_bar_logger(logger)
    logger(message='Moviepy - Running:\n>>> "+ " ".join(cmd)')

    popen_params = {"stdout": DEVNULL,
                    "stderr": sp.PIPE,
                    "stdin": DEVNULL}

    if os.name == "nt":
        popen_params["creationflags"] = 0x08000000

    proc = sp.Popen(cmd, **popen_params)

    out, err = proc.communicate() # proc.wait()
    proc.stderr.close()

    if proc.returncode:
        if errorprint:
            logger(message='Moviepy - Command returned an error')
        raise IOError(err.decode('utf8'))
    else:
        logger(message='Moviepy - Command successful')

    del proc

def is_string(obj):
    """ Returns true if s is string or string-like object,
    compatible with Python 2 and Python 3."""
    try:
        return isinstance(obj, basestring)
    except NameError:
        return isinstance(obj, str)


def cvsecs(time):
    """ Will convert any time into seconds. 
    
    If the type of `time` is not valid, 
    it's returned as is. 

    Here are the accepted formats::

    >>> cvsecs(15.4)   # seconds 
    15.4 
    >>> cvsecs((1, 21.5))   # (min,sec) 
    81.5 
    >>> cvsecs((1, 1, 2))   # (hr, min, sec)  
    3662  
    >>> cvsecs('01:01:33.045') 
    3693.045
    >>> cvsecs('01:01:33,5')    # coma works too
    3693.5
    >>> cvsecs('1:33,5')    # only minutes and secs
    99.5
    >>> cvsecs('33.5')      # only secs
    33.5
    """
    factors = (1, 60, 3600)
    
    if is_string(time):     
        time = [float(f.replace(',', '.')) for f in time.split(':')]

    if not isinstance(time, (tuple, list)):
        return time

    return sum(mult * part for mult, part in zip(factors, reversed(time)))


def deprecated_version_of(f, oldname, newname=None):
    """ Indicates that a function is deprecated and has a new name.

    `f` is the new function, `oldname` the name of the deprecated
    function, `newname` the name of `f`, which can be automatically
    found.

    Returns
    ========

    f_deprecated
      A function that does the same thing as f, but with a docstring
      and a printed message on call which say that the function is
      deprecated and that you should use f instead.

    Examples
    =========

    >>> # The badly named method 'to_file' is replaced by 'write_file'
    >>> class Clip:
    >>>    def write_file(self, some args):
    >>>        # blablabla
    >>>
    >>> Clip.to_file = deprecated_version_of(Clip.write_file, 'to_file')
    """

    if newname is None: newname = f.__name__

    warning= ("The function ``%s`` is deprecated and is kept temporarily "
              "for backwards compatibility.\nPlease use the new name, "
              "``%s``, instead.")%(oldname, newname)

    def fdepr(*a, **kw):
        warnings.warn("MoviePy: " + warning, PendingDeprecationWarning)
        return f(*a, **kw)
    fdepr.__doc__ = warning

    return fdepr


# non-exhaustive dictionnary to store default informations.
# any addition is most welcome.
# Note that 'gif' is complicated to place. From a VideoFileClip point of view,
# it is a video, but from a HTML5 point of view, it is an image.

extensions_dict = { "mp4":  {'type':'video', 'codec':['libx264','libmpeg4', 'aac']},
                    'ogv':  {'type':'video', 'codec':['libtheora']},
                    'webm': {'type':'video', 'codec':['libvpx']},
                    'avi':  {'type':'video'},
                    'mov':  {'type':'video'},

                    'ogg':  {'type':'audio', 'codec':['libvorbis']},
                    'mp3':  {'type':'audio', 'codec':['libmp3lame']},
                    'wav':  {'type':'audio', 'codec':['pcm_s16le', 'pcm_s24le', 'pcm_s32le']},
                    'm4a':  {'type':'audio', 'codec':['libfdk_aac']}
                  }

for ext in ["jpg", "jpeg", "png", "bmp", "tiff"]:
    extensions_dict[ext] = {'type':'image'}


def find_extension(codec):
    if codec in extensions_dict:
        # codec is already the extension
        return codec

    for ext,infos in extensions_dict.items():
        if codec in infos.get('codec', []):
            return ext
    raise ValueError(
        "The audio_codec you chose is unknown by MoviePy. "
        "You should report this. In the meantime, you can "
        "specify a temp_audiofile with the right extension "
        "in write_videofile."
    )











FFMPEG_BINARY = os.getenv('FFMPEG_BINARY', 'ffmpeg-imageio')
IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', 'auto-detect')



if os.name == 'nt':
    try:
        import winreg as wr # py3k
    except ImportError:
        import _winreg as wr # py2k


def try_cmd(cmd):
    try:
        popen_params = {
            "stdout": sp.PIPE,
            "stderr": sp.PIPE,
            "stdin": DEVNULL
        }

        # This was added so that no extra unwanted window opens on windows
        # when the child process is created
        if os.name == "nt":
            popen_params["creationflags"] = 0x08000000

        proc = sp.Popen(cmd, **popen_params)
        proc.communicate()
    except Exception as err:
        return False, err
    else:
        return True, None

if FFMPEG_BINARY=='ffmpeg-imageio':
    from imageio.plugins.ffmpeg import get_exe
    FFMPEG_BINARY = get_exe()

elif FFMPEG_BINARY=='auto-detect':

    if try_cmd(['ffmpeg'])[0]:
        FFMPEG_BINARY = 'ffmpeg'
    elif try_cmd(['ffmpeg.exe'])[0]:
        FFMPEG_BINARY = 'ffmpeg.exe'
    else:
        FFMPEG_BINARY = 'unset'
else:
    success, err = try_cmd([FFMPEG_BINARY])
    if not success:
        raise IOError(
            str(err) +
            " - The path specified for the ffmpeg binary might be wrong")

if IMAGEMAGICK_BINARY=='auto-detect':
    if os.name == 'nt':
        try:
            key = wr.OpenKey(wr.HKEY_LOCAL_MACHINE, 'SOFTWARE\\ImageMagick\\Current')
            IMAGEMAGICK_BINARY = wr.QueryValueEx(key, 'BinPath')[0] + r"\convert.exe"
            key.Close()
        except:
            IMAGEMAGICK_BINARY = 'unset'
    elif try_cmd(['convert'])[0]:
        IMAGEMAGICK_BINARY = 'convert'
    else:
        IMAGEMAGICK_BINARY = 'unset'
else:
    if not os.path.exists(IMAGEMAGICK_BINARY):
        raise IOError(
            "ImageMagick binary cannot be found at {}".format(
                IMAGEMAGICK_BINARY
            )
        )

    if not os.path.isfile(IMAGEMAGICK_BINARY):
        raise IOError(
            "ImageMagick binary found at {} is not a file".format(
                IMAGEMAGICK_BINARY
            )
        )

    success, err = try_cmd([IMAGEMAGICK_BINARY])
    if not success:
        raise IOError("%s - The path specified for the ImageMagick binary might "
                      "be wrong: %s" % (err, IMAGEMAGICK_BINARY))


def get_setting(varname):
    """ Returns the value of a configuration variable. """
    gl = globals()
    if varname not in gl.keys():
        raise ValueError("Unknown setting %s"%varname)
    # Here, possibly add some code to raise exceptions if some
    # parameter isn't set set properly, explaining on how to set it.
    return gl[varname]


def change_settings(new_settings=None, filename=None):
    """ Changes the value of configuration variables."""
    new_settings = new_settings or {}
    gl = globals()
    if filename:
        with open(filename) as in_file:
            exec(in_file)
        gl.update(locals())
    gl.update(new_settings)
    # Here you can add some code  to check that the new configuration
    # values are valid.













PY3=sys.version_info.major >= 3

try:
    string_types = (str, unicode)     # Python 2
except NameError:
    string_types = (str)              # Python 3
   
try:
    from subprocess import DEVNULL    # Python 3
except ImportError:
    DEVNULL = open(os.devnull, 'wb')  # Python 2









class FFMPEG_AudioWriter:
    """
    A class to write an AudioClip into an audio file.

    Parameters
    ------------

    filename
      Name of any video or audio file, like ``video.mp4`` or ``sound.wav`` etc.

    size
      Size (width,height) in pixels of the output video.

    fps_input
      Frames per second of the input audio (given by the AUdioClip being
      written down).

    codec
      Name of the ffmpeg codec to use for the output.

    bitrate:
      A string indicating the bitrate of the final video. Only
      relevant for codecs which accept a bitrate.

    """

    def __init__(self, filename, fps_input, nbytes=2,
                 nchannels=2, codec='libfdk_aac', bitrate=None,
                 input_video=None, logfile=None, ffmpeg_params=None):

        self.filename = filename
        self.codec = codec
        if logfile is None:
            logfile = sp.PIPE
            
        self.logfile=logfile
        self.input_video=input_video
        self.fps_input=fps_input
        self.bitrate=bitrate
        self.codec=codec
        self.nchannels=nchannels
        self.nbytes=nbytse
        self.ffmpeg_params=ffmpeg_paras
        
        
        
        
        
    def init_audio(self):

        
        cmd = ([get_setting("FFMPEG_BINARY"), '-y',
                "-loglevel", "error" if self.logfile == sp.PIPE else "info",
                "-f", 's%dle' % (8*nbytes),
                "-acodec",'pcm_s%dle' % (8*nbytes),
                '-ar', "%d" % self.fps_input,
                '-ac', "%d" % self.nchannels,
                '-i', '-']
               + (['-vn'] if self.input_video is None else ["-i", self.input_video, '-vcodec', 'copy'])
               + ['-acodec', self.codec]
               + ['-ar', "%d" % self.fps_input]
               + ['-strict', '-2']  # needed to support codec 'aac'
               + (['-ab', self.bitrate] if (self.bitrate is not None) else [])
               + (self.ffmpeg_params if self.ffmpeg_params else [])
               + [self.filename])

        popen_params = {"stdout": DEVNULL,
                        "stderr": logfile,
                        "stdin": sp.PIPE}

        if os.name == "nt":
            popen_params["creationflags"] = 0x08000000

        self.proc = sp.Popen(cmd, **popen_params)

    def write_frames(self, frames_array):
        try:
            try:
                self.proc.stdin.write(frames_array.tobytes())
            except NameError:
                self.proc.stdin.write(frames_array.tostring())
        except IOError as err:
            ffmpeg_error = self.proc.stderr.read()
            error = (str(err) + ("\n\nMoviePy error: FFMPEG encountered "
                                 "the following error while writing file %s:" % self.filename
                                 + "\n\n" + str(ffmpeg_error)))

            if b"Unknown encoder" in ffmpeg_error:

                error = (error +
                         ("\n\nThe audio export failed because FFMPEG didn't "
                          "find the specified codec for audio encoding (%s). "
                          "Please install this codec or change the codec when "
                          "calling to_videofile or to_audiofile. For instance "
                          "for mp3:\n"
                          "   >>> to_videofile('myvid.mp4', audio_codec='libmp3lame')"
                          ) % (self.codec))

            elif b"incorrect codec parameters ?" in ffmpeg_error:

                error = (error +
                         ("\n\nThe audio export failed, possibly because the "
                          "codec specified for the video (%s) is not compatible"
                          " with the given extension (%s). Please specify a "
                          "valid 'codec' argument in to_videofile. This would "
                          "be 'libmp3lame' for mp3, 'libvorbis' for ogg...")
                         % (self.codec, self.ext))

            elif b"encoder setup failed" in ffmpeg_error:

                error = (error +
                         ("\n\nThe audio export failed, possily because the "
                          "bitrate you specified was two high or too low for "
                          "the video codec."))

            else:
                error = (error +
                         ("\n\nIn case it helps, make sure you are using a "
                          "recent version of FFMPEG (the versions in the "
                          "Ubuntu/Debian repos are deprecated)."))

            raise IOError(error)

    def close(self):
        if hasattr(self, 'proc') and self.proc:
            self.proc.stdin.close()
            self.proc.stdin = None
            if self.proc.stderr is not None:
                self.proc.stderr.close()
                self.proc.stdee = None
            # If this causes deadlocks, consider terminating instead.
            self.proc.wait()
            self.proc = None

    def __del__(self):
        # If the garbage collector comes, make sure the subprocess is terminated.
        self.close()

    # Support the Context Manager protocol, to ensure that resources are cleaned up.

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


