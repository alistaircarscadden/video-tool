import sys
import argparse

from videotool.subprograms import clip, cat, gif


def main():
    parser = argparse.ArgumentParser()

    # common parser for writing videofiles

    write_parent = argparse.ArgumentParser(add_help=False)
    write_parent.add_argument(
        '--threads', '-t', help='# of threads.', type=int, default=8
    )
    write_parent.add_argument(
        '--mute', '-m', help='Mute audio.', action='store_true'
    )
    write_parent.add_argument('--output', '-o', help='Output file.')

    subparsers = parser.add_subparsers(required=True)

    # vt clip

    sp_clip = subparsers.add_parser(
        'clip', help='Clip a section of video.', parents=[write_parent]
    )
    sp_clip.set_defaults(subprogram=clip)
    sp_clip.add_argument('input_file', help='File to read.')
    sp_clip.add_argument('start_time', help='Start time.')
    sp_clip.add_argument('end_time', help='End time.')

    # vt cat

    sp_cat = subparsers.add_parser(
        'cat', help='Concatenate multiple videos.', parents=[write_parent]
    )
    sp_cat.set_defaults(subprogram=cat)
    sp_cat.add_argument(
        'input_file', metavar='files', help='Files to read.', nargs='+'
    )

    # vt gif

    sp_gif = subparsers.add_parser('gif', help='Create a gif.')
    sp_gif.set_defaults(subprogram=gif)
    sp_gif.add_argument('input_file', help='File to read.')
    sp_gif.add_argument('--output', '-o', help='Output file.')

    # start subprogram

    args = parser.parse_args(sys.argv[1:])
    args.subprogram(args)
