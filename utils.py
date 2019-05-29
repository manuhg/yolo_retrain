import os

def exec_cmd(cmdstr):
    print(cmdstr, os.popen(cmdstr).read())

def get_NFPA_dataset():
    if os.path.isdir('data/nfpa'):
        print('NFPA Dataset exists already.')
        return
        
    exec_cmd('pip install gdown')
    exec_cmd('gdown https://drive.google.com/uc?id=1_gJcci9p6cS0EucumFt2gpwA0tqgP7_f&export=download')
    exec_cmd('unzip NFPA_dataset.zip')
    exec_cmd('mkdir data')
    exec_cmd("mv 'NFPA dataset' data/nfpa")
    exec_cmd('cp data/nfpa/train.txt ./')
    exec_cmd('cp data/nfpa/test.txt ./')
    exec_cmd('printf "NFPA" > classes.txt')

def get_PASCAL_VOC_dataset():
    if os.path.isdir('VOCdevkit'):
        print('Pascal VOC Dataset exists already.')
        return
    exec_cmd('wget https://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar')
    exec_cmd('wget https://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar')
    exec_cmd('wget https://pjreddie.com/media/files/VOCtest_06-Nov-2007.tar')
    exec_cmd('tar xf VOCtrainval_11-May-2012.tar')
    exec_cmd('tar xf VOCtrainval_06-Nov-2007.tar')
    exec_cmd('tar xf VOCtest_06-Nov-2007.tar')
    
    exec_cmd('wget https://pjreddie.com/media/files/voc_label.py')
    exec_cmd('python voc_label.py')
    
    exec_cmd('cat 2007_train.txt 2012_*.txt > train.txt')
    
    exec_cmd('cp 2007_val.txt test.txt')
    
    exec_cmd('cp data/voc.names classes.txt')
    
    exec_cmd('mkdir bkup')
    exec_cmd('mv 2* bkup/')
    exec_cmd('mv *.tar bkup/')