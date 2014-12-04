#!/bin/bash

inputFile="%fileFullName%"
outputFile="%outputDirectory%%prefix%%fileName%%postfix%.mkv"
audioCodec="pcm_s16le"
videoCodec="ffv1 -level 3"

command="ffmpeg -vsync passthrough -i \"${inputFile}\" "
command="${command} -vcodec ${videoCodec} -g 1 "
command="${command} -acodec ${audioCodec}"


command="${command} ${outputFile}"

echo $command
eval $command
