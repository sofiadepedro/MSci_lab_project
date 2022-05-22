#!/bin/sh
echo "${#1}" "${#2}" "${#3}" "${#4}"
path="`dirname \"$0\"`"
echo $path
masterpath=$(pwd)

username=$(cat $path/username)
exptfolder=$(cat $masterpath/name_exp_folder)

server_name=$(cat /Users/$username/.ssh/server_name_icn)
cip=$(cat /Users/$username/.ssh/server_hostname_icn)

if (( ${#1} < 1 )) || (( ${#2} < 1 ));
then
echo "Missing -s or ex/tb"
exit 1
fi

if [ "${1}" != "-s" ] || [ "${2}" != "ex" ] && [ "${2}" != "tb" ];
then
echo "Wrong inputs"
exit 1
fi

read -t 1 -n 10000 discard
clear
name_scripts=('Thermal camera check' 'Zabers check' 'Touch stability' 'Height finding' 'Extrapolation of heights' 'Grid ROI finding' 'Checking stimulations' 'Scaling' 'Training Staircase' 'Staircase' 'Send data to computer')
PS3='What Python script would you like to start with?   '
read -t 1 -n 10000 discard
select opt in "${name_scripts[@]}"; do
for i in "${!name_scripts[@]}"; do
    if [[ "${name_scripts[$i]}" = "${opt}" ]]; then
        index_start="${i}";
    fi
    done
    break
done

clear
if (( $index_start < 1 )); then
    echo '\nStarting script to check thermal image...\n'
    python ${path}/thermal_camera_check.py $1 $2
    echo '\nScript to check thermal image DONE...\n'
fi

clear
if (( $index_start < 2 )); then
    echo '\nStarting script to check set of Zaber\n'
    python ${path}/zabers_check.py $1 $2
    echo '\nScript to check set of Zabers is DONE...\n'
fi

clear
if (( $index_start < 3 )); then
    echo '\nStarting script to check set of Zaber\n'
    python ${path}/touch_stability.py $1 $2 $3 $4
    echo '\nScript to check set of Zabers is DONE...\n'
fi

clear
if (( $index_start < 4 )); then
    echo '\nStarting script to find master grid point\n'
    python ${path}/master_height_finding.py $1 $2 $3 $4
    echo '\nScript to find master grid point DONE...\n'
fi

clear
if (( $index_start < 5 )); then
    echo '\nStarting script to find master grid point\n'
    python ${path}/height_extrapolation.py $1 $2 $3 $4
    echo '\nScript to find master grid point DONE...\n'
fi

clear
if (( $index_start < 6 )); then
    echo '\nStarting script to find the ROI per grid position\n'
    python ${path}/grid_roi_finding.py $1 $2 $3 $4
    echo '\nScript for finding the ROI per grid position is done...\n'
fi

clear
if (( $index_start < 7 )); then
    echo '\nStarting script to perform SCALING on the grid...\n'
    python ${path}/checking_stims.py $1 $2 $3 $4
    echo '\n\nScript for SCALING is done...\n\n'
fi

clear
if (( $index_start < 8 )); then
    echo '\nStarting script to perform SCALING on the grid...\n'
    python ${path}/exp_scaling.py $1 $2 $3 $4
    echo '\n\nScript for SCALING is done...\n\n'
fi

clear
if (( $index_start < 9 )); then
    echo '\nStarting script to train on task...\n'
    python ${path}/training_staircase.py $1 $2 $3 $4
    echo '\nScript for training on task is done...\n'
fi

clear
if (( $index_start < 10 )); then
    echo '\nStarting script to perform STAIRCASE on the grid...\n'
    python ${path}/exp_stair.py $1 $2 $3 $4 "-ns" "1"
    echo '\n\nScript for STAIRCASE is done...\n\n'
fi

clear
if (( $index_start <= 11 )) && [ $2 == "ex" ]; then
    echo '\n\nSending data to computer office...\n\n'

    folder_name=$(cat $path/temp_folder_name.txt)

    echo $folder_name
    echo $server_name
    echo $cip
    scp -rv "$masterpath/data/$folder_name" $server_name@$cip:/home/ivan/Documents/phd/coding/python/phd/$exptfolder/data

    echo '\n\nData in computer office..\n\n'
fi

clear
if [ $2 == "ex" ];then
    echo '\n\nStart analysis script..\n\n'

    echo $folder_name
    echo $server_name
    echo $cip

    nohup ssh $server_name@$cip "cd /home/ivan/Documents/phd/coding/python/phd/$exptfolder && /home/ivan/Documents/phd/coding/python/phd/$exptfolder/src_analysis/automatic/auto_analysis.sh $folder_name" &

    echo '\n\nAnalysis is done!\n\n'
fi
