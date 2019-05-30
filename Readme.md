# Re train yolo (yolov2, yolov2-tiny, yolov3, yolov3-tiny)
example:
data_dir is the location which contains train.txt test.txt and classes.txt
model_name is the version of yolo to be trained i.e one of (yolov2, yolov2-tiny, yolov3, yolov3-tiny)
batch_size is the number of images in each batch
subdivisions is the number of subdivisions in a batch

#Getting started
`python train.py --data-dir='.'`