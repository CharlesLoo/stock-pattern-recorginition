import os,shutil
from PIL import Image
def resize(images_path):
    files= os.listdir(images_path)
    num = 0
    x = 0
    y = 0
    for file_name in files:
        images_full_path = os.path.join(images_path,file_name)
        im  = Image.open(images_full_path)
        if num == 0:
            (x,y) = im.size
            num = num + 1
        #print('in===  ',im.size)
        out = im.resize((x,y),Image.ANTIALIAS)
        print('resize file ',images_full_path,' to ',out.size)
        out.save(images_full_path)

def move(figures_path,images_path):
    files= os.listdir(figures_path)
    for file_name in files:
        file_full_name = figures_path+r'/'+file_name
        if not os.path.exists(images_path):
            os.makedirs(images_path)  
        figures = os.listdir(file_full_name)
        for figure in figures:
            figure_full_name = file_full_name+r'/'+figure   
            shutil.copy(figure_full_name,images_path)

    print('Successfully copyied figures to images.')

def main():
    figures_path = os.path.join(os.getcwd(),'fitted_figures')
    images_path = os.path.join(os.getcwd(),'images')
    #move(figures_path,images_path)
    resize(images_path)

if __name__ == '__main__':
    main()
