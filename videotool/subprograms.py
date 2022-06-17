from argparse import Namespace
from os.path import splitext

from moviepy.editor import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

from videotool.util import generate_filename


def clip(args: Namespace):
    '''Subprogram for taking a portion of a video'''

    output_file = args.output
    if output_file is None:
        _, ext = splitext(args.input_file)
        print(f'Output file using same extension as input file: {ext}')
        output_file = generate_filename(ext)

    audio = not args.mute

    clip = VideoFileClip(args.input_file)
    subclip = clip.subclip(args.start_time, args.end_time)
    subclip.write_videofile(output_file, threads=args.threads, audio=audio)
    clip.close()
    subclip.close()


def cat(args: Namespace):
    '''Subprogram for concatenating multiple videos'''

    if args.output == None:
        _, extension = splitext(args.input_file[0])
        output_file = generate_filename(extension)
    else:
        output_file = args.output

    input_clips = [VideoFileClip(i) for i in args.input_file]

    audio = not args.mute

    for i in range(1, len(input_clips)):
        print(input_clips[i - 1].end)
        input_clips[i].set_start(input_clips[i - 1].end)
        print(input_clips[i].end)

    composition = concatenate_videoclips(input_clips)
    composition.write_videofile(output_file, audio=audio)
    composition.close()

    for clip in input_clips:
        clip.close()


def gif(args: Namespace):
    '''Subprogram for converting videos to gif format'''

    if args.output == None:
        output_file = generate_filename('.gif')
    else:
        output_file = args.output

    clip = VideoFileClip(args.input_file)
    clip.write_gif(output_file, program='ffmpeg')
    clip.close()
