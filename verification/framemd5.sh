framemd5_path="%SIPDirectory%metadata/%fileUUID%.md5"

# If framemd5 wasn't calculated during characterization, perform it now
test -e $framemd5_path || ffmpeg -i %fileFullPath% -f framemd5 $framemd5_path

diff="$(diff -U3 $framemd5_path <(ffmpeg -i %outputLocation% -f framemd5 -))" 

test -z "$diff" || echo 'framemd5 comparison failed!' && echo "$diff" > "%SIPDirectory%metadata/%fileUUID%.framemd5_failure.diff" && exit 1
