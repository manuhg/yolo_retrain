import os
import sys
from utils import exec_cmd

def write2file(filename, data):
    try:
        with open(filename, 'w') as f:
            f.write(data)
    except Exception as e:
        print(e)

def gen_data_file(n_classes=1, train_data='train.txt', test_data='test.txt', pd='cfg/', data_file_name='obj.data', names_file='obj.names', backup_dir='backup/'):
    data_file = 'classes= '+str(n_classes)+'\ntrain = '+train_data + \
        '\nvalid  = '+test_data+'\nnames = '+pd+'/'+names_file+'\nbackup = '+backup_dir
    write2file(pd+data_file_name, data_file)
    return pd+data_file_name


def gen_names_file(class_names, names_file_name='obj.names', pd='cfg/'):
    try:
        with open(pd+names_file_name, 'w') as f:
            for i in range(len(class_names)):
                class_name = class_names[i]
                nl = '\n' if i < len(class_names)-1 else ''
                f.write(class_name+nl)
        return pd+names_file_name
    except Exception as e:
        print(e)


def yolov2_tiny_cfg(num_classes, batch_size=64, subdivisions=8):
    return {'6': 'batch='+str(batch_size),
            '7': 'subdivisions='+str(subdivisions),
            '20': 'max_batches='+str(2000*num_classes),
            '22': 'steps='+str(int(.8*(2000*num_classes)))+','+ str(int(.9*(2000*num_classes))),
            '119': 'filters='+str((num_classes+5)*5),
            '125': 'classes='+str(num_classes)}


def yolov2_cfg(num_classes, batch_size=64, subdivisions=8):
    return {'6': 'batch='+str(batch_size),
            '7': 'subdivisions='+str(subdivisions),
            '20': 'max_batches='+str(2000*num_classes),
            '22': 'steps='+str(int(.8*(2000*num_classes)))+','+ str(int(.9*(2000*num_classes))),
            '237': 'filters='+str((num_classes+5)*5),
            '244': 'classes='+str(num_classes)}


def yolov3_tiny_cfg(num_classes, batch_size=64, subdivisions=8):
    return {'6': 'batch='+str(batch_size),
            '7': 'subdivisions='+str(subdivisions),
            '20': 'max_batches='+str(2000*num_classes),
            '22': 'steps='+str(int(.8*(2000*num_classes)))+','+ str(int(.9*(2000*num_classes))),
            '127': 'filters='+str((num_classes+5)*3),
            '171': 'filters='+str((num_classes+5)*3),
            '135': 'classes='+str(num_classes),
            '177': 'classes='+str(num_classes)}


def yolov3_cfg(num_classes, batch_size=64, subdivisions=8):
    return {'6': 'batch='+str(batch_size),
            '7': 'subdivisions='+str(subdivisions),
            '20': 'max_batches='+str(2000*num_classes),
            '22': 'steps='+str(int(.8*(2000*num_classes)))+','+ str(int(.9*(2000*num_classes))),
            '603': 'filters='+str((num_classes+5)*3),
            '689': 'filters='+str((num_classes+5)*3),
            '776': 'filters='+str((num_classes+5)*3),
            '610': 'classes='+str(num_classes),
            '696': 'classes='+str(num_classes),
            '783': 'classes='+str(num_classes)}


def modify_cfg_file(filename, modifications_dict):
    def gen_mdstr(item):
        return item[0]+'s/.*/'+item[1]+'/;'
    modification_str = ''.join(
        list(map(gen_mdstr, modifications_dict.items())))
    exec_cmd("sed -i '"+modification_str+"' '"+filename+"'")


def gen_cfg_file(classes, model_name='yolov2', batch_size=64, subdivisions=8, target_dir='cfg/', src_dir='cfgs/', filename='yolo_custom.cfg'):
    config_funcs = {'yolov2-tiny': yolov2_tiny_cfg, 'yolov2': yolov2_cfg,
                    'yolov3-tiny': yolov3_tiny_cfg, 'yolov3': yolov3_cfg}
    
    num_classes = len(classes)
    print('Configuring to train ',model_name,' classes:',num_classes)
    
    cfg_func = config_funcs.get(model_name)
    if cfg_func is None:
        print(model_name, 'Not found. Available models are: ',
              list(config_funcs.keys()))
    output_filename = target_dir+filename
    exec_cmd('cp '+src_dir+model_name+'.cfg '+output_filename)
    cfg_dict = cfg_func(num_classes, batch_size, subdivisions)
    
    modify_cfg_file(output_filename,cfg_dict)
    return output_filename


def gen(class_names, train_data='train.txt', test_data='test.txt', model_name='yolov2', batch_size=64,
        subdivisions=8, filename='yolo_custom.cfg'):

    data_file = gen_data_file(
        len(class_names), train_data=train_data, test_data=test_data)
    names_file = gen_names_file(class_names)
    cfg_file = gen_cfg_file(class_names, model_name,
                            batch_size, subdivisions, filename=filename)
    return data_file, names_file, cfg_file
