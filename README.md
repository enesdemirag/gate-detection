![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)

# Underwater Object (Gate) Detection using TensorFlow

## Overview

This repository created to train a model and detect an underwater object using tensorflow API.

Our team works on an Autonomous Underwater Vehicle to prepare for [Singapore AUV Challange](https://sauvc.org/) and the [RoboSub'20](https://robonation.org/programs/robosub/).

Check out our [website](http://auv.itu.edu.tr/) and [repo](https://gitlab.com/itu-auv).

> Tested on Ubuntu 18.04

## Getting Ready

#### 1. Install [tensorflow](https://www.tensorflow.org/install)

```
sudo apt update
sudo apt install python3-dev python3-pip
pip3 install --user --upgrade tensorflow
```

#### 2. Get your images for dataset.

#### 3. Use [labelimg](https://github.com/tzutalin/labelImg) to label images.

```
pip3 install labelImg
```

#### 4. Run [xml2csv](xml2csv.py) script to convert xml files.

```
python3 xml2csv.py
```

#### 5. Install tensorflow model

```
git clone https://github.com/tensorflow/models.git
sudo apt-get install protobuf-compiler python-pil python-lxml
cd models/
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
sudo python3 setup.py install
```

#### 6. Run script for train and test

```
python3 generate-tfrecord.py --csv_input=data/train-labels.csv --output_path=data/train.record --image_dir=images/train/
```

```
python3 generate-tfrecord.py --csv_input=data/test-labels.csv --output_path=data/test.record --image_dir=images/test/
```

## Training

#### Local

- Train on your PC, run [this](training.sh) script.

#### Server

- Train on a powerful machine, run [colab notebook](training.ipynb) on Google Colab.