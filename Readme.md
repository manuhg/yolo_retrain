# Re train yolo (yolov2, yolov2-tiny, yolov3, yolov3-tiny)
example:
data_dir is the location which contains train.txt test.txt and classes.txt
model_name is the version of yolo to be trained i.e one of (yolov2, yolov2-tiny, yolov3, yolov3-tiny)
batch_size is the number of images in each batch
subdivisions is the number of subdivisions in a batch

#Getting started
Train with pascal voc dataset
`!python train.py -d . -ts Pascal_VOC -m yolov2`

Train with custom dataset located in `/path/to/dataset`

`!python train.py -d /path/to/dataset -m yolov2`

#Inference 
Once the model is trained, the weights file is stored in backup folder.
Also for inference the batch_size and subdivisions in cfg file needs to be set to 1 (this is done automatically by run_inference function)

Example:
`!python train.py -d . -ts Pascal_VOC -m yolov2 --run_inference true`

#Getting help
run `python train.py --help` for more information regarding parameters to be passed for train.py