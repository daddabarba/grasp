launch_base="python -i augmentData.py"
folder=$1

for target in {0,10}
do
python -i augmentData.py $folder $target &
#$gnome-terminal -x bash -c "$cmd"
#echo "Launched target $target with command: \"$cmd\""
done
