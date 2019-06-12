
echo "Porting files..."
cd stills
sshpass -p raspberry scp -v pi@192.168.0.8:~/gardener/stills/* .
chmod 444 *
mkdir temp

echo "Moving files..."
aa=0; for i in `ls -1v`; do cp $i `printf "temp/%05d" $aa`.jpg -v; aa=$(($aa+1)); done
cd temp

echo "Creating lapse..."
avconv -r 10 -i %05d.jpg -r 10 -vcodec libx264 -vf scale=1920:1080 timelapse.mp4
mv timelapse.mp4 ../../
cd ..
rm -rfv temp
cd ..

echo "Done"
wsl-open timelapse.mp4
