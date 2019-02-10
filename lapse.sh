
cd stills
mkdir temp
# cp *.jpg temp/ -v
# cd temp
aa=0;for i in `ls -1v`; do cp $i `printf "temp/%04d" $aa`.jpg -v; aa=$(($aa+1));done
cd temp
avconv -r 10 -i %04d.jpg -r 10 -vcodec libx264 -vf scale=1920:1080 timelapse.mp4
mv timelapse.mp4 ..
cd ..
rm -rf temp/ -v
mv timelapse.mp4 ..

