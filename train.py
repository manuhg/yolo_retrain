import os
import sys
import subprocess
from gen_files import gen
import argparse


def exec_cmd(cmdstr):
    print(cmdstr, os.popen(cmdstr).read())


def print_info():
    print('Example python train.py -d data_dir')
    print('Please have a data directory such that:')
    print('It has train.txt and test.txt which contain images with absolute paths(recommended) or path relative to train.py file')
    print('It has classes.txt that contain names of classes that the dataset contains')


def train(data_dir, model_name='yolov2', batch_size='64', subdivisions='8', filename='yolo_custom.cfg',
          class_names_file='classes.txt', model_url='https://pjreddie.com/media/files/darknet19_448.conv.23'):
    try:
        batch_size, subdivisions = int(batch_size), int(subdivisions)
        class_names = None
        flag = False
        if not os.path.isfile('./darknet'):
            print('Cloning darknet repository')
            exec_cmd('git clone https://github.com/pjreddie/darknet.git dkn')
            exec_cmd('mv -v dkn/* ./')
            exec_cmd(
                "sed -i 's/GPU=0/GPU=1/;s/CUDNN=0/CUDNN=1/;s/OPENCV=0/OPENCV=1/;s/OPENMP=0/OPENMP=1/;' Makefile")
            exec_cmd('make -j8')

        if not os.path.isfile('darknet19_448.conv.23'):
            print('Downloading darknet model')
            exec_cmd('wget '+model_url)

        print('Generating config files')
        with open(data_dir+'/'+class_names_file) as f:
            class_names = list(
                map(lambda s: s.replace('\n', '').strip(), f.readlines()))
            class_names = list(map(filter(None,class_names)))

        data_file, names_file, cfg_file = gen(
            class_names, model_name=model_name, batch_size=batch_size, subdivisions=subdivisions, filename=filename)
        flag = True
        print(data_file, names_file, cfg_file)
        print('Traning the model')
        cmd = './darknet detector train '+data_file +' '+cfg_file+' darknet19_448.conv.23'
        
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
    data_dir = ''
    try:
        args = parser.parse_args()
        data_dir = args.data_dir
        model_name = args.model_name
        batch_size = args.batch_size
        subdivisions = args.subdivisions
        custom_cfg_filename = args.custom_cfg_filename
    except Exception as e:
        print(e)
        parser.print_help()
        print_info()

    train(data_dir, model_name, batch_size, subdivisions, custom_cfg_filename)