set -euo pipefail
IFS=$'\n\t'

tempdir=$(mktemp -d /tmp/fits.XXXXXX)
ng edu.harvard.hul.ois.fits.Fits -i "%relativeLocation%" -o "$tempdir/fits.xml" >/dev/null
cat "$tempdir/fits.xml"

rm -r "$tempdir"
