rm -rf /tmp/stream
mkdir /tmp/stream
sudo raspistill -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0 -awb sun > /dev/null 2>&1 &
LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -p 9000 -w /usr/local/www"
sudo pkill raspistill
