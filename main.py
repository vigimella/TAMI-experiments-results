"""

This script allows merging all files .results obtained after experimentation executions on TAMI.

The folder that contains files can be stored in any part of the disk, please specify the correct URL during the script execution.

2022 - Vigimella.

"""

import os
import pandas as pd

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def standard_parameters(file, txt_file, filed_to_check, index_before, default_parameter):
    if not filed_to_check in txt_file:
        index_begin = txt_file.index(index_before)
        before_lr = txt_file[0:index_begin]
        after_lr = txt_file[index_begin:len(txt_file)]

        new_file = before_lr + default_parameter + '\n' + after_lr

        text_file = open(file, "w")
        text_file.write(new_file)
        text_file.close()


def get_unique_file(dir_url, output_name, digits):
    dfl = list()
    col = ['file_path', 'model', 'epochs', 'batch_size', 'learning_rate', 'size_img', 'test_loss', 'test_accuracy',
           'precision', 'recall', 'f-measure', 'AUC', 'execution_time']
    elm = list()
    sub_path_list = list()
    file_to_check = list()
    for sub_dir in os.walk(dir_url):
        element = sub_dir[0].replace(APP_ROOT + '/', '')
        sub_path_list.append(element)

    for path in sub_path_list:

        for file in os.listdir(path):

            if file.endswith('.results'):
                file_elm = os.path.join(path, file)

                text_file = open(file_elm, "r")
                text_file_new = str(text_file.read())
                text_file.close()

                if 'mode = train-test' in text_file_new and 'test loss:' in text_file_new:
                    file_to_check.append(file_elm)

    for file in file_to_check:

        text_file = open(file, "r")
        text_file_new = str(text_file.read())
        text_file.close()

        # check parameter that can take on a default value is in file, otherwise it is added and setting as default
        # configuration

        standard_parameters(file, text_file_new, 'learning_rate', 'batch_size', 'learning_rate = 0.01')
        standard_parameters(file, text_file_new, 'epochs', 'output_model', 'epochs = 10')
        standard_parameters(file, text_file_new, 'batch_size', 'learning_rate', 'batch_size = 32')
        standard_parameters(file, text_file_new, 'size_img', 'data_type', 'size_img = 100x1')

        if 'Error' in text_file_new:
            text_file_new.replace('Error\n', '0')

        text_file_res = open(file, "r")

        elm.append(file)

        for line in text_file_res:

            if 'model = ' in line and not 'output_' in line and not 'modello_migliore' in line and not 'load_' in line:

                elm.append(line.replace('model = ', ''))

            elif 'epochs = ' in line:

                elm.append(line.replace('epochs = ', ''))

            elif 'batch_size' in line:

                elm.append(line.replace('batch_size = ', ''))

            elif 'learning_rate' in line:

                elm.append(line.replace('learning_rate = ', ''))
            elif 'size_img' in line:

                elm.append(line.replace('size_img = ', ''))

            elif 'test loss' in line:

                line = line.replace('test loss:', '').replace('\t', '').replace(' \n', '')
                try:
                    line = round(float(line), int(digits))
                    elm.append(line)
                except:
                    elm.append(line)

            elif 'test accuracy:' in line:

                line = line.replace('test accuracy:', '').replace('\t', '').replace(' \n', '')
                try:
                    line = round(float(line), int(digits))
                    elm.append(line)
                except:
                    elm.append(line)

            elif 'Prec:' in line:

                line = line.replace('Prec:', '').replace('\t', '').replace(' \n', '')
                try:
                    line = round(float(line), int(digits))
                    elm.append(line)
                except:
                    elm.append(line)

            elif 'Recall:' in line:

                line = line.replace('Recall:', '').replace('\t', '').replace(' \n', '')
                try:
                    line = round(float(line), int(digits))
                    elm.append(line)
                except:
                    elm.append(line)

            elif 'F-Measure:' in line:

                line = line.replace('F-Measure:', '').replace('\t', '').replace(' \n', '')
                try:
                    line = round(float(line), int(digits))
                    elm.append(line)
                except:
                    elm.append(line)

            elif 'AUC:' in line:

                line = line.replace('AUC:', '').replace('\t', '').replace(' \n', '')
                try:
                    line = round(float(line), int(digits))
                    elm.append(line)
                except:
                    elm.append(line)

            elif 'EX. TIME:' in line:

                elm.append(line.replace('EX. TIME:', ''))

    dfl = [elm[i:i + 13] for i in range(0, len(elm), 13)]

    df = pd.DataFrame(dfl, columns=[col]).drop_duplicates()
    save_file_path = os.path.join(APP_ROOT, output_name)

    df.to_csv(save_file_path, index=False)

    print(f'CSV file saved successfully at the following URL : {save_file_path}')


if __name__ == '__main__':

    print(
        ' +-----------------------------------------------------------------------------------------------------------------------------------+ \n |                                              ******* HINT: output_model_mode *******                                              | \n +-----------------------------------------------------------------------------------------------------------------------------------+ \n |            This script allow merging all files .results obtained after experimentation executions (train-test) on TAMI.           | \n |                                                                                                                                   | \n |                                                                                                                                   | \n | The folder that contains files can be stored in any part of the disk, please specify the correct URL during the script execution. | \n |                                                                                                                                   | \n |                                                                                                                                   | \n |                                                         2022 - Vigimella.                                                         | \n +-----------------------------------------------------------------------------------------------------------------------------------+ \n |                                                          Instructions :                                                           | \n |                                                                                                                                   | \n |                               - insert the name of the file that you want to use to the output file                               | \n |                                                                                                                                   | \n |                              - insert the path of directory where you have stored your .result files                              | \n |                                                                                                                                   | \n |                            - you obtain a file as output in the directory where you execute the program                           | \n +-----------------------------------------------------------------------------------------------------------------------------------+')
    output_file_name = input('Insert file name to give to the file: ')

    if not '.csv' in output_file_name:
        output_file_name = output_file_name + '.csv'

    user_choice = input(
        f'Your file will be saved with the following name "{output_file_name}". Do you want continue? Y/n: ')

    user_folder = input(f'Enter the folder name where you stored CSV files: ')
    folder_file = os.path.join(APP_ROOT, user_folder)
    print(
        'Pay attention, inserting 0 in the next step your results are rounded to the closest entire number available!\n')
    digits = input(f'How many digits after decimal point you need? ')
    if not os.path.exists(folder_file):
        print(f'No such directory "{user_folder}"')
    else:
        if user_choice.lower() == 'y':
            get_unique_file(folder_file, output_file_name, digits)

        elif user_choice.lower() == 'n':
            print('Exit...')
            exit(0)
        else:
            print('Character not recognized. Exit...')
            exit(-1)
