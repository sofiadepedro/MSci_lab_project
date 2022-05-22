#!/bin/bash
# exec 1>/home/ivan/log-output.txt 2>/home/ivan/log-errors.txt

printf '\n\nAuto analysis script triggered in server...\n\n'

masterpath=$(pwd)
path="`dirname \"$0\"`"
echo $path
echo $masterpath

exptfolder=$(cat $masterpath/name_exp_folder)
echo $exptfolder
touch /home/ivan/Documents/phd/coding/python/phd/$exptfolder/src_analysis/automatic/temp_folder_analyse
export PYTHONPATH="${PYTHONPATH}:/home/ivan/Documents/phd/coding/python/phd/classes"

name_file=$1
# name_file=$(sed -e 's/^"//' -e 's/"$//' <<<"$name_file")
echo $name_file > /home/ivan/Documents/phd/coding/python/phd/$exptfolder/src_analysis/automatic/temp_folder_analyse
echo $name_file

printf '\n\nSTARTING analysis to plot the distributions of NOs across points\n\n'
/home/ivan/.pyenv/shims/python /home/ivan/Documents/phd/coding/python/phd/$exptfolder/src_analysis/automatic/auto_pos.py -f $name_file
printf '\n\nAnalysis to plot the distribution of NOs across points DONE\n\n'

printf '\n\nSTARTING PDF BUILDER\n\n'
/home/ivan/.pyenv/shims/python /home/ivan/Documents/phd/coding/python/phd/$exptfolder/src_analysis/automatic/auto_blind_pdf_builder.py -f $name_file
printf '\n\nPDF BUILDER DONE\n\n'

printf '\n\nSTARTING script to analyse thermal videos\n\n'
/home/ivan/.pyenv/shims/python /home/ivan/Documents/phd/coding/python/phd/$exptfolder/src_analysis/automatic/auto_ani_thermal_images.py -f $name_file
printf '\n\nScript to analyse thermal videos DONE\n\n'

rm /home/ivan/Documents/phd/coding/python/phd/$exptfolder/src_analysis/automatic/temp_folder_analyse