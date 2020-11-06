from moviepy.editor import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from os.path import splitext
from random import randint
from time import time
import sys


#
#   Command line argument parsing
#


def list_contains(item, _list):
    try:
        _list.index(item)
    except ValueError:
        return False

    return True


def has_arg(arg, argl=sys.argv):
    '''Returns True or False if `argl` contains `arg`'''

    return list_contains(arg, argl)


def has_any(args, argl=sys.argv):
    '''Returns True or False if `argl` contains any of `args`'''

    for arg in args:
        if list_contains(arg, argl):
            return True

    return False


def value_following(arg, argl=sys.argv):
    '''Returns the value in `argl` following `arg` or `None`'''

    try:
        i = argl.index(arg)
        return argl[i + 1]
    except ValueError:
        return None
    except IndexError:
        return None


def value_following_any(args, argl=sys.argv):
    '''Returns the value in `argl` following any of `args` or `None`.
    Prioritizes the first valid one found.'''

    for arg in args:
        try:
            i = argl.index(arg)
            return argl[i + 1]
        except ValueError:
            pass
        except IndexError:
            pass
    return None


def unnamed_value(k, ignore, argl=sys.argv):
    '''Returns the `k`th value in `argl` that is not one of `ignore` nor immediately following any of `ignore`.
    Ignores the script name.
    `k` is 0-indexed.'''

    for i, arg in enumerate(argl):
        if i != 0:
            if list_contains(arg, ignore) or list_contains(argl[i-1], ignore):
                continue
            else:
                if k == 0:
                    return arg

                k -= 1


#
#   Utility
#


def help(msg):
    '''If the `-h` or `--help` options were on the command line this will print the `msg` and exit.'''

    if has_any(['-h', '--help']):
        print(msg.format(script=sys.argv[0]))
        exit()


def generate_filename(extension=''):
    '''Generate a (very probably) unique filename with the given `extension`. Include the dot in the extension.'''
    x = int(time() * 1000)
    y = randint(0x0, 0xFFFF)
    return f'v_{x}_{y:04}{extension}'


#
#   Subprograms
#


def clip(args):
    '''Subprogram for taking a portion of a video'''

    help(
        '{script} [--help] [--threads THREADS] [--output OUTPUT_FILE] [--mute] INPUT_FILE START_TIME END_TIME')
    value_flags = ['-o', '--output', '-t', '--threads']
    input_file = unnamed_value(0, value_flags, argl=args)
    start_time = unnamed_value(1, value_flags, argl=args)
    end_time = unnamed_value(2, value_flags, argl=args)
    mute = has_any(['-m', '--mute'])

    output_file = value_following_any(['-o', '--output'], argl=args)
    if output_file is None:
        _, ext = splitext(input_file)
        output_file = generate_filename(ext)

    threads = 8
    if has_any(['-t', '--threads'], argl=args):
        threads = value_following_any(['-t', '--threads'], argl=args)

    clip = VideoFileClip(input_file)
    subclip = clip.subclip(start_time, end_time)
    subclip.write_videofile(output_file, threads=threads, audio=not mute)
    clip.close()
    subclip.close()


def cat(args):
    '''Subprogram for concatenating multiple videos'''

    help(
        '{script} [--help] [--threads THREADS] [--extension OUTPUT_EXTENSION] [--output OUTPUT_FILE] [--mute] INPUT_FILE [INPUT_FILE ...]')

    value_flags = ['-o', '--output', '-t', '--threads', '-e', '--extension']

    mute = has_any(['-m', '--mute'])

    first_input_file = unnamed_value(0, value_flags, argl=args)
    if first_input_file is None:
        exit()

    output_file = value_following_any(['-o', '--output'], argl=args)
    if output_file is None:
        if has_any(['-e', '--extension'], argl=args):
            out_ext = value_following_any(['-e', '--extension'], argl=args)
        else:
            _, out_ext = splitext(first_input_file)
        output_file = generate_filename(out_ext)

    threads = 8
    if has_any(['-t', '--threads'], argl=args):
        threads = value_following_any(['-t', '--threads'], argl=args)

    input_clips = []

    for i in range(0, 1024):
        input_file = unnamed_value(i, value_flags, argl=args)

        if input_file is None:
            break

        clip = VideoFileClip(input_file)
        input_clips.append(clip)

    for i in range(1, len(input_clips)):
        print(input_clips[i-1].end)
        input_clips[i].set_start(input_clips[i-1].end)
        print(input_clips[i].end)

    composition = concatenate_videoclips(input_clips)
    composition.write_videofile(output_file, audio=not mute)
    composition.close()

    for clip in input_clips:
        clip.close()


def gif(args):
    '''Subprogram for converting videos to gif format'''

    help(
        '{script} gif [--help] [--output OUTPUT_FILE] INPUT_FILE')

    value_flags = ['-o', '--output']

    input_file = unnamed_value(0, value_flags, argl=args)
    if input_file is None:
        exit()

    output_file = value_following_any(['-o', '--output'], argl=args)
    if output_file is None:
        output_file = generate_filename('.gif')

    clip = VideoFileClip(input_file)
    clip.write_gif(output_file, program='ffmpeg')
    clip.close()


#
#   Main
#


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'{sys.argv[0]} SUBPROGRAM [?]')
        exit()

    subprogram = sys.argv[1]
    args = sys.argv[1:]

    funcs = {
        'clip': clip,
        'cat': cat,
        'gif': gif
    }

    try:
        funcs[subprogram](args)
    except KeyError:
        print(f'Unknown subprogram: {subprogram}')
