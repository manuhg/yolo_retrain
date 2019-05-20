def gen_data_file(n_classes=1,train_data='train.txt',validation_data='test.txt',data_file_name='obj.data',names_file='obj.names',backup_dir='backup/'):
    data_file = 'classes= '+n_classes+'\ntrain = '+train_data+'\nvalid  = '+validation_data+'\nnames = '+names_file+'\nbackup = '+backup_dir
    try:
        with open(data_file_name,'w') as f:
            f.write(data_file)
        return data_file_name
    except Exception as e:
        print(e)

def gen_names_file(class_names,names_file_name='obj.names'):
    try:
        with open(names_file_name,'w') as f:
            for class_name in class_names:
                f.write('\n'+class_name)
        return names_file_name
    except Exception as e:
        print(e)

def gen(class_names,train_data='train.txt',validation_data='test.txt'):
    data_file = gen_data_file(len(class_names),train_data=train_data,validation_data=validation_data)
    names_file = gen_names_file(class_names)
