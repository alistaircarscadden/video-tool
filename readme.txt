vt: Video Tool

clip, concatenate, mute videos and create gifs on the commandline


Usage Examples:
    vt clip --output out.mp4 in.mp4 3:45.05 3:49.12
    vt clip --output out2.mp4 in.mp4 4:05.00 4:22.00
    vt cat --output out3.mp4 --mute out.mp4 out2.mp4
    vt gif --output out4.gif out3.mp4

    Try vt <SUBPROGRAM> --help


Installation:
    Put this script wherever you want.
    Requires MoviePy: pip install moviepy
    Requires ffmpeg: I don't know if moviepy installs this or not but
    it's required
