#! /bin/sh

for FILE in input/*/*.wav
do
    # FILENAME=`echo ${FILE} | sed 's/\.[^\.]*$//'`
    FILENAME=`echo ${FILE} | sed 's/input\///'`
    echo ${FILENAME}
    ffmpeg -i input/${FILENAME} -ac 1 -ar 22050 for_transcribe/${FILENAME}
done