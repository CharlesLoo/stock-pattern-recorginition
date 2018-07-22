import os,shutil
from PIL import Image
def rename(label_path):
    files= os.listdir(label_path)
    for file_name in files:
        label_full_path = os.path.join(label_path,file_name)
        if file_name.find(' (3rd copy)') > -1:
            new_name = file_name[0:file_name.index(' (3rd copy)')]+"_wider_20_.xml"
        elif file_name.find(' (4th copy)') > -1:
            new_name = file_name[0:file_name.index(' (4th copy)')]+"_r_5_0_.xml"
        elif file_name.find(' (5th copy)') > -1:
            new_name = file_name[0:file_name.index(' (5th copy)')]+"_r_10_0_.xml"
        elif file_name.find(' (6th copy)') > -1:
            new_name = file_name[0:file_name.index(' (6th copy)')]+"_r_5_1_.xml"
        elif file_name.find(' (7th copy)') > -1:
            new_name = file_name[0:file_name.index(' (7th copy)')]+"_r_10_1_.xml"
        elif file_name.find(' (another copy)') > -1:
            new_name = file_name[0:file_name.index(' (another copy)')]+"_taller_10_.xml"
        elif file_name.find(' (copy)') > -1:
            new_name = file_name[0:file_name.index(' (copy)')]+"_taller_20_.xml"
        elif file_name.find(' copy') == -1:
            new_name = file_name[0:file_name.index('.xml')]+"_wider_10_.xml"
        new_full_name = os.path.join(label_path,new_name)
        os.rename(label_full_path,new_full_name)


def main():
    label_path = os.path.join(os.getcwd(),'variation_data','labels')
    rename(label_path)

if __name__ == '__main__':
    main()
