#! /bin/sh

for FILE in */*.mp4
do
    FILENAME=`echo ${FILE} | sed 's/\.[^\.]*$//'`
    ffmpeg -i ${FILENAME}.mp4 -f wav -vn ${FILENAME}.wav
done