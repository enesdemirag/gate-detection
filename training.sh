# Install requirements
pip3 install Cython
pip3 install contextlib2
pip3 install pillow
pip3 install lxml
pip3 install jupyter
pip3 install matplotlib

# Clone object detection API
git clone https://github.com/tensorflow/models.git

# Install COCO API
git clone https://github.com/cocodataset/cocoapi.git
cd cocoapi/PythonAPI/
make
cp -r pycocotools ../../models/research/

# Compile Protobuf
cd ../../models/research/
protoc object_detection/protos/*.proto --python_out=.

# Add libraries to Python Path
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
# set PYTHONPATH=/content/gate-detection/models/research : /content/gate-detection/models/research/slim

# Install API
sudo python3 setup.py install

# Copy training files into API folder
cd ../../
cp -r data/ models/research/object_detection/
cp -r images/ models/research/object_detection/
cp -r model/ models/research/object_detection/
cp -r training/ models/research/object_detection/

# Get inside object_detection folder
cd models/research/object_detection/

# Run training script
python3 legacy/train.py --logtostderr --train_dir=training/ --pipeline_config_path=training/ssd_mobilenet.config
