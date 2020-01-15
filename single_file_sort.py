import os 
import sys
import subprocess

import shutil 
import re

dl_dir = '/home/acarnec/Downloads/'

modules = ['mta', 'ana', 'met', 'log', 'mat',
           'lin', 'min', 'pol', 'mic', 'mte']

michaelmas = ['mta', 'ana', 'met', 'log', 'mat']
hilary = ['lin', 'min', 'pol', 'mic', 'mte']


def change_directory(path):
    """ 
    Changes directory to path. 
    """
    os.chdir(path)


def list_files(path):
    ls_output = os.listdir(path)
    return ls_output


def move_file_to_dir(f, dest_dir):
    """moves a file to dest_dir if it not already there"""
    ls = list_files(dest_dir)
    if ls == True:
        if f not in ls:
            subprocess.call(f"mv {f} {dest_dir} 2>/dev/null", shell=True)
        else:
            return 
    else:
        subprocess.call(f"mv {f} {dest_dir} 2>/dev/null", shell=True)

def tup_file(file_name, path='/home/acarnec/Downloads/'):
    """filename -> tup
    Returns a tuple of (path, filename)
    """
    f_tup = (path, file_name)
    return f_tup

def add_code(f_tup):
    """ tup -> tup """
    path, filename = f_tup
    for code in modules:
        if code == filename[:3]:
            f_tup = (path, filename, code)
            return f_tup
    else:
        raise Exception

def  add_type(f_tup):
    """ tup -> tup """
    path, filename, code = f_tup
    type_code = filename[3]
    f_tup = (path, filename, code, type_code)    
    return f_tup

def sort_to_dest(f_tup):
    path, filename, code, type_code = f_tup
    college_dir = '/home/acarnec/Documents/3rdYear'
    if code in michaelmas:
        dest_dir = f"{college_dir}/Michaelmas_Term/{code}/{type_code}"
    else:
        dest_dir = f"{college_dir}/Hilary_Term/{code}/{type_code}/"
    try:
        move_file_to_dir(filename, dest_dir)
    except TypeError:
        pass


def sort_file(filename):
    f_tup = tup_file(filename)
    f_tup = add_code(f_tup)
    f_tup = add_type(f_tup)
    sort_to_dest(f_tup)

def single_sort(filename):
    change_directory('/home/acarnec/Downloads')   
    sort_file(filename)
