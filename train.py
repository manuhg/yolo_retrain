import os
import sys
import subprocess
from gen_files import gen,gen_cfg_file
import argparse
from utils import exec_cmd,get_NFPA_dataset,get_PASCAL_VOC_dataset
import random
import glob
exec_cmd('pip -q install natsort')
from natsort import natsorted

def print_info():
    print('Example python train.py -d data_dir')
    print('Please have a data directory such that:')
    print('It has train.txt and test.txt which contain images with absolute paths(recommended) or path relative to train.py file')
    print('It has classes.txt that contain names of classes that the dataset contains')

def run_inference(model_name,class_names_file='classes.txt',filename='yolo_custom.cfg',test_file='test.txt'):
    try:
        with open(class_names_file) as f:
            class_names = list(
                map(lambda s: s.replace('\n', '').strip(), f.readlines()))
            class_names = list(filter(None,class_names))
        
        cfg_file =  gen_cfg_file(class_names, model_name,1, 1, filename=filename)
        with open(test_file) as f:
            lines = f.readlines()

        filename = '.'.join(filename.split('.')[:-1])
        weights_file = natsorted(glob.glob('backup/'+filename+'_*.weights'))[-1]
        test_file = random.choice(lines).replace('\n','').strip()
        cmd = './darknet detect '+cfg_file+' '+weights_file+ ' '+test_file
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1,shell = True)
        for line in iter(p.stdout.readline,''):
            print(line)
        p.stdout.close()
        p.wait()
    except Exception as e:
        print('Error during inference',e)
    

def train(data_dir, model_name='yolov2', batch_size='64', subdivisions='8', filename='yolo_custom.cfg',
          class_names_file='classes.txt', model_url='https://pjreddie.com/media/files/darknet19_448.conv.23',
          dataset_dw_func=None):
    try:
        batch_size, subdivisions = int(batch_size), int(subdivisions)
        class_names = None
        flag = False
        if not os.path.isfile('./darknet'):
            print('Cloning darknet repository')
            exec_cmd('git clone https://github.com/AlexeyAB/darknet.git dkn')#https://github.com/pjreddie/darknet.git dkn')
            exec_cmd('mv -v dkn/* ./')
            exec_cmd("sed -i 's/GPU=0/GPU=1/;s/CUDNN=0/CUDNN=1/;s/OPENCV=0/OPENCV=1/;s/OPENMP=0/OPENMP=1/;' Makefile")
            exec_cmd('make -j8')

        if not os.path.isfile('darknet19_448.conv.23'):
            print('Downloading darknet model')
            exec_cmd('wget '+model_url)

        if dataset_dw_func is not None:
            print('Downloading dataset')
            dataset_dw_func()
        
        print('Generating config files')
        with open(data_dir+'/'+class_names_file) as f:
            class_names = list(
                map(lambda s: s.replace('\n', '').strip(), f.readlines()))
            class_names = list(filter(None,class_names))

        data_file, names_file, cfg_file = gen(
            class_names, model_name=model_name, batch_size=batch_size, subdivisions=subdivisions, filename=filename)
        flag = True
        print(data_file, names_file, cfg_file)
        
        print('Traning the model')
        cmd = './darknet detector train '+data_file +' '+cfg_file+' darknet19_448.conv.23 -dont_show'
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1,shell = True)
        for line in iter(p.stdout.readline,''):
            print(line)
        p.stdout.close()
        p.wait()

    except Exception as e:
        print(e)
        if not flag:
            print_info()
        else:
            print('Error training the model')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Tool to extract re train YOLO')
    parser.add_argument('-d', '--data_dir', dest='data_dir',
                        help='Directory that contains train.txt test.txt and also images to train on', default='', required=True, type=str)
    parser.add_argument('-m', '--model_name', dest='model_name',
                        help='Model name (yolov2,yolov2-tiny,yolov3,yolov3-tiny', default='yolov2', type=str)
    parser.add_argument('-b', '--batch_size', dest='batch_size',
                        help='batch size for training', default='24', type=str)
    parser.add_argument('-s', '--subdivisions', dest='subdivisions',
                        help='subdivision batch for training', default='8', type=str)
    parser.add_argument('-f', '--custom_cfg_filename', dest='custom_cfg_filename',
                        help='filename of custom cfg file that will be generated', default='yolo_custom.cfg', type=str)
    parser.add_argument('-ts', '--train_sample', dest='train_sample',
                        help='Train on a sample dataset (optional NFPA or Pascal_VOC)', default='', type=str)
    parser.add_argument('-ri', '--run_inference', dest='do_inference',
                        help='Run inference on a sample dataset (optional NFPA or Pascal_VOC) on which model is already trained', default='', type=str)
    data_dir = ''
    try:
        args = parser.parse_args()
        data_dir = args.data_dir
        model_name = args.model_name
        batch_size = args.batch_size
        subdivisions = args.subdivisions
        custom_cfg_filename = args.custom_cfg_filename
        train_sample = args.train_sample
        do_inference = args.do_inference
    except Exception as e:
        print(e)
        parser.print_help()
        print_info()
    
    ##################Train on a sample dataset (optional)
    get_datasets={'NFPA':get_NFPA_dataset,'Pascal_VOC':get_PASCAL_VOC_dataset}
    dataset_dw_func = get_datasets.get(train_sample)
    # if dataset_dw_func is not None:
        # dataset_dw_func()
    ###########################################################3
    if do_inference:
        run_inference(model_name,data_dir+'/classes.txt',custom_cfg_filename,test_file='test.txt')
    
    train(data_dir, model_name, batch_size, subdivisions, custom_cfg_filename,dataset_dw_func=dataset_dw_func)