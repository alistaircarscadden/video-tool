 ___      ___ _________  ___  ___       
|\  \    /  /|\___   ___\\  \|\  \      
\ \  \  /  / ||___ \  \_\ \  \ \  \     
 \ \  \/  / /     \ \  \ \ \  \ \  \    
  \ \    / /       \ \  \ \ \__\ \__\   
   \ \__/ /         \ \__\ \|__|\|__|   
    \|__|/           \|__|     ___  ___ 
                              |\__\|\__\
                              \|__|\|__|


What does it do?
clip, concatenate, mute videos and create gifs on the commandline

Why?
This is a high level wrapper of ffmpeg intended for careless edits on the fly. If you need more control use anything else.
I can use this to take a video with ShadowPlay, and cut it down to 3 seconds or whatever.


Usage:
  > vt clip a.mp4 3:45.05 3:49.12
  > vt clip b.mp4 0:32 1:25
  > vt cat --mute a.mp4 b.mp4
  > vt gif a.mp4


Build:
  > py -m build
    

Install:
  > py -m pip install git+https://github.com/alistaircarscadden/video-tool
  OR
  > py -m pip install <whl>
  OR
  > the install method of YOUR DREAMS. you choose!


Requirements:
  Requires ffmpeg: I don't know if moviepy installs this or not but it's required.
