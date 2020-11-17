import os 
import cv2
import json
import pandas as pd
import xml.etree.ElementTree as ET
from os import path
from coco_get_annotations_xml_format import write_to_xml


def write_empty_to_xml(data_folder, image_name, save_folder,xml_template='pascal_voc_template.xml'):
    # read xml file
    tree = ET.parse(xml_template)
    root = tree.getroot()    
    
    # modify
    folder = root.find('folder')
    folder.text = 'Annotations'
    
    fname = root.find('filename')
    fname.text = image_name.split('.')[0] 
    
    src = root.find('source')
    database = src.find('database')
    database.text = 'COCO2017'
    
    
    # size
    img = cv2.imread(os.path.join(data_folder, image_name))
    h,w,d = img.shape
    
    size = root.find('size')
    width = size.find('width')
    width.text = str(w)
    height = size.find('height')
    height.text = str(h)
    depth = size.find('depth')
    depth.text = str(d)

    # save .xml to anno_path
    anno_path = os.path.join(save_folder, image_name.split('.')[0] + '.xml')
    print(anno_path)
    tree.write(anno_path)

if __name__=='__main__':
    photo_path = './val2017'
    xml_path = './saved'

    #checking for missing xml files
    missing=[]
    for image_path in os.listdir(photo_path):
        image_file_name = image_path.split('.')[0]
        xml_file_name = image_file_name+'.xml'
        xml_file_path = xml_path+'/'+xml_file_name
        exist = path.exists(xml_file_path)
        if exist==False:
            missing.append(image_path)

    #creating new directory for the missing files
    savepath = 'savedMissing'
    if not os.path.exists(savepath):
        os.makedirs(savepath)

    #generating "empty" xml for the missing files
    for image in missing:
        write_empty_to_xml(photo_path,image,savepath)