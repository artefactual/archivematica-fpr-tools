ocrfiles="%SIPObjectsDirectory%metadata/OCRfiles"
test -d "$ocrfiles" || mkdir -p "$ocrfiles"

tesseract %fileFullName% "$ocrfiles/%fileName%"
