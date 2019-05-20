import os,sys
from gen_files import gen
import argparse

def exec_cmd(cmdstr):
    print(cmdstr,os.popen(cmdstr).read())

def print_info():
    print('Example python train.py -d data_dir')
    print('Please have a data directory such that:')
    print('It has train.txt and test.txt which contain images with absolute paths(recommended) or path relative to train.py file')
    print('It has classes.txt that contain names of classes that the dataset contains')

def train(data_dir,class_names_file='classes.txt',model_url='https://pjreddie.com/media/files/darknet19_448.conv.23'):
    try:
        class_names = None
        if not os.path.isfile('./darknet'):
            print('Cloning darknet repository')
            exec_cmd('git clone https://github.com/pjreddie/darknet.git dkn')
            exec_cmd('mv -v dkn/* ./')
            exec_cmd("sed -i 's/GPU=0/GPU=1/;s/CUDNN=0/CUDNN=1/;s/OPENCV=0/OPENCV=1/;s/OPENMP=0/OPENMP=1/;' Makefile")
            exec_cmd('make -j8')
        
        if not os.path.isfile('darknet19_448.conv.23'):
            print('Downloading darknet model')
            exec_cmd('wget '+model_url)
        
        print('Generating config files')
        with open(data_dir+'/'+class_names_file) as f:
            class_names = list(map(lambda s:s.replace('\n',''),f.readlines()))
        
        data_file,names_file,cfg_file = gen(class_names)

        print('Traning the model')
        exec_cmd('./darknet detector train '+data_file+' '+cfg_file+' darknet19_448.conv.23')
        
    except Exception as e:
        print(e)
        print_info()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tool to extract re train darknet (yolo v2)')
    parser.add_argument('-d','--data_dir', dest='data_dir',help='Directory that contains train.txt test.txt and also images to train on', default='',required=True, type=str)
    data_dir = ''
    try:
        args = parser.parse_args()
        data_dir = args.data_dir
    except Exception as e:
        print(e)
        parser.print_help()
        print_info()
    
    if args.data_dir=='':
        parser.print_help()
        print_info()

    train(data_dir)
