
echo "Porting files..."
cd stills
sshpass -p raspberry scp -v pi@192.168.0.8:~/PiGardener/stills/* .
chmod 444 *
mkdir temp

echo "Copying files..."
cp -v *.jpg temp
cd temp
chmod 777 *

echo "Removing pink files..."
for i in `ls *.jpg`; do

    convert $i -resize 1x1 a.txt
    cat a.txt | sed -n -e 's/.*(//p' | sed -n -e 's/)//p' > b.txt
    A=$(awk -F "," '{ if (NR == 1) { print $1 } }' b.txt)
    C=$(awk -F "," '{ if (NR == 1) { print $3 } }' b.txt)
    B=$(awk -F "," '{ if (NR == 1) { print $2 } }' b.txt)
    
    rm a.txt
    rm b.txt

    if (( $(echo "($A / $B) > 2.5 && ($C / $B) > 2.5" | bc -l) )); then
        rm -v $i
    fi
done

echo "Renaming files..."
aa=0; for i in `ls -1v`; do mv $i `printf "%05d" $aa`.jpg -v; aa=$(($aa+1)); done

echo "Creating lapse..."
avconv -r 10 -i %05d.jpg -r 10 -vcodec libx264 -vf scale=1920:1080 timelapse.mp4
mv timelapse.mp4 ../../
cd ..
rm -rfv temp
cd ..

echo "Done"
wsl-open timelapse.mp4
