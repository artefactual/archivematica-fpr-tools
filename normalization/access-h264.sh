ffmpeg -i "%fileFullName%" -vcodec libx264 -pix_fmt yuv420p -preset medium -crf 18 "%outputDirectory%%prefix%%fileName%%postfix%.mp4"
