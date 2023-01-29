#! /usr/bin/env bash

# call this script with trailing extra options to pass to enc_vid.py

# instead of hardcoding the path,
# we're going to follow where the scripts are installed
APP_DIR=$(dirname $0)
DIR=$(basename ${PWD})
# I will name a cover image with the same name
# as the final video file.
JPG=$(ls *${DIR}.jpg)
VID_BASE=$(echo ${JPG} | sed -e "s/\.jpg//g")

# I name my video files as dvd-rip-001.avi
# when there are multiple files to rip
for VID in dvd-rip*.avi
do
  INPUT_FILE="${PWD}/${VID}"
  VID_NUMBER="${VID:8:3}"
  if [ "${VID_NUMBER}" == "avi" ]
  then
    VID_NAME="${PWD}/${VID_BASE}.mp4"
  else
    VID_NAME="${PWD}/${VID_BASE}-${VID_NUMBER}.mp4"
  fi
  # you can pass additional args here
  CMD="python3 -u ${APP_DIR}/enc_vid.py --input ${INPUT_FILE} --output ${VID_NAME} $@"
  echo "${CMD}"
  eval "${CMD}"
  # don't continue of the ripping exit non-zero
  if [ $? != 0 ]; then
    echo "Error! Unable to complete rip."
    exit 9
  fi
  ~/bin/mk_ss.sh ${VID_NAME} av
  if [ "${VID_NUMBER}" != "avi" ]
  then
    /bin/mv tn100.jpg tn${VID_NUMBER}.jpg
  fi
done

~/bin/post_av.sh
