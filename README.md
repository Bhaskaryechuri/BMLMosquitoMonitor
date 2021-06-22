# BML Mosquito Monitor

This repository contains all files & instructions needed to recreate the BML Mosquito Monitor including:
- Mechanical design files needed for laser-cutting
- A copy of the entire Raspberry Pi image (most efficient way of replicating the BML Mosquito Monitor software and settings on a new Raspberry Pi)
- Latest version of the BMLBox App Code (already present in the RPi Image, but helpful when iterating on the software)
- A [Zoology Owncloud link to the raspberry pi disk image](https://cloud.zoology.ubc.ca/s/NsVyCmkXQ03NwOV) containing all the code and required settings (use this as your starting point when using a new Raspberry Pi)


On a high-level, using up the BML Mosquito Monitor involves the following steps:
1. Fabricating and assembling the mechanical aspects of the box (instructions in the [Mechanical ](https://github.com/Bhaskaryechuri/BMLMosquitoMonitor/tree/main/Mechanical)folder)
2. Setting up the Raspberry Pi and camera system (instructions in the [RPi_Code](https://github.com/Bhaskaryechuri/BMLMosquitoMonitor/tree/main/RPi_Code) folder)
3. Setting up the behavioral assay items & conditions inside the box (lighting, experimental treatments & controls)
4. Configuring and running the video recording software
5. Getting the video data out of the Raspberry Pi (via a USB drive)
