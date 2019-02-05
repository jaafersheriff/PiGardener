
cd stills
mkdir temp
cp *.jpg temp/ -v
cd temp
# for f in *.jpg ; do mv $f "${f:0:3}00${f:3}" -v; done
aa=0;for i in `ls -1v`; do mv $i `printf "%04d" $aa`.jpg -v; aa=$(($aa+1));done
avconv -r 10 -i %04d.jpg -r 10 -vcodec libx264 -vf scale=2592:1944 timelapse.mp4
mv timelapse.mp4 ..
cd ..
rm -rf temp/ -v
mv timelapse.mp4 ..

