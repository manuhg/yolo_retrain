import os,sys

def write2file(filename,data):
    try:
        with open(filename,'w') as f:
            f.write(data)
    except Exception as e:
        print(e)

def gen_data_file(n_classes=1,train_data='train.txt',test_data='test.txt',pd='cfg/',data_file_name='obj.data',names_file='obj.names',backup_dir='backup/'):
    data_file = 'classes= '+str(n_classes)+'\ntrain = '+train_data+'\nvalid  = '+test_data+'\nnames = '+names_file+'\nbackup = '+backup_dir
    write2file(pd+data_file_name,data_file)

def gen_names_file(class_names,names_file_name='obj.names',pd='cfg/'):
    try:
        with open(pd+names_file_name,'w') as f:
            for i in range(len(class_names)):
                class_name = class_names[i]
                nl = '\n' if i <len(class_names)-1 else ''
                f.write(class_name+nl)
        return names_file_name
    except Exception as e:
        print(e)

def gen_yolo_v2_cfg(classes,mode='train',batch_size=None,subdivisions=None,pd='cfg/',cd='yolov2',filename='yolo_custom.cfg'):
    cfg_head = '[net]\n'
    if batch_size is None or subdivisions is None:
        if mode=='train':
            batch_size=64
            subdivisions=8
        else:
            batch_size=1
            subdivisions=1

    cfg_head+='batch='+str(batch_size)+r'\nsubdivisions='+str(subdivisions)+r'\n'
    write2file(cd+'/01head',cfg_head)
    n_classes = len(classes)
    n_filters = (n_classes+5)*5

    cfg_end =r'\n[convolutional]\nsize=1\nstride=1\npad=1\nfilters='+str(n_filters)+ r'\nactivation=linear\n[region]\nanchors =  0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828\nbias_match=1\nclasses='+str(n_classes)+ r'\ncoords=4\nnum=5\nsoftmax=1\njitter=.3\nrescore=1\n\nobject_scale=5\nnoobject_scale=1\nclass_scale=1\ncoord_scale=1\n\nabsolute=1\nthresh = .6\nrandom=1'
    write2file(cd+'/03end',cfg_end)
    cfg_file = pd + filename
    print(os.popen('cat '+cd+'/* > '+ cfg_file ))
    return cfg_file



def gen(class_names,train_data='train.txt',test_data='test.txt'):
    data_file = gen_data_file(len(class_names),train_data=train_data,test_data=test_data)
    names_file = gen_names_file(class_names)
    cfg_file = gen_yolo_v2_cfg(class_names)
    return data_file,names_file,cfg_file
