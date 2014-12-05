#!/bin/bash

inputFile="%fileFullName%"
framemd5path="%SIPDirectory%metadata/%fileUUID%.md5"
outputFile="%outputDirectory%%prefix%%fileName%%postfix%.mkv"
audioCodec="pcm_s16le"
videoCodec="ffv1 -level 3"

command="ffmpeg -vsync passthrough -i \"${inputFile}\" "
# Generating framemd5 at the same time as normalization is faster
# than doing both separately - framemd5 requires ffmpeg to decompress
# every frame in the video, but when performe at the same time as
# normalization, both tasks can share the same decompressed frames.
command="${command} -f framemd5 \"${framemd5path}\" "
command="${command} -vcodec ${videoCodec} -g 1 "
command="${command} -acodec ${audioCodec}"


command="${command} ${outputFile}"

echo $command
eval $command
