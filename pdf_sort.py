import os
import sys
import subprocess
from time import sleep

from single_file_sort import single_sort


def listdir(path):
    """ path -> list(filenames) """
    ls_output = os.listdir(path)
    exts = ('.PDF','.pdf', '.doc', '.docx')
    ls_output = [f for f in ls_output if f.endswith(exts)]
    converted_docs = [convert_to_pdf(f) for f in ls_output if any('.pdf','.PDF') not in f]
    ls_output.extend(converted_docs)
    # Remove any doc or docx files.
    docs = ('.docx', '.doc')
    ls_output = [pdf for pdf in ls_output if pdf.endswith(docs) is not True]
    return ls_output


def format_pdf_name(pdf):
    """ str -> formatted_str

    Escapes whitespace.
    """
    pdf = "\'" + pdf + "\'"
    return pdf


def add_path_do_pdf(pdf, path):
    """ str_filename -> str_path -> str """
    formatted_pdf = path + pdf
    return formatted_pdf


def zathura(pdf_path):
    """
    str -> subprocess_object
    """
    cmd = 'zathura ' + pdf_path
    process_obj = subprocess.Popen("exec " + cmd,
                                   shell=True,
                                   stderr=subprocess.DEVNULL)
    return process_obj


def terminate_pdf(process_obj):
    """
    subprocess_object -> bool
    End the Process
    """
    process_obj.kill()
    return True


def select_terminal():
    """Select for input"""
    os.system("wmctrl -a 'Downloads : python — Konsole'")


def triage(pdf_path, pdf_obj):
    text = (f"File: {pdf_path}\n"
            "What would you like to do?"
            "\nr for rename"
            "\nd for delete"
            "\nf for rename and sort "
            "\nn to pass"
            "\nq to quit")
    answer = input(text + "\n> ")
    if answer == 'r':
        new_name = rename(pdf_path)
        return
    elif answer == 'd':
        delete(pdf_path)
        return
    elif answer == 'f':
        new_name = rename(pdf_path)
        sort(new_name)
        return
    elif answer == 'q':
        terminate_pdf(pdf_obj)
        sys.exit()
    elif answer == 'n':
        return
    else:
        print("Invalid Input.")
        triage(pdf_path, pdf_obj)


def rename(pdf_path):
    # Get new name
    new_name = input("New Name: ")

    # Formate new name
    renamed_pdf_path = "/home/acarnec/Downloads/" + new_name
    if ".pdf" not in renamed_pdf_path:
        renamed_pdf_path = renamed_pdf_path + ".pdf"
    if renamed_pdf_path != pdf_path:
        cmd = f"mv {pdf_path} {renamed_pdf_path}"
        subprocess.Popen(cmd, shell=True)
        return new_name
    else:
        return pdf_path


def delete(file_path):
    cmd = f"rm {file_path}"
    subprocess.run("exec " + cmd, shell=True)


def sort(filename):
    """ Sorts the object based on it's filename
    filename -> action
    """
    single_sort(filename)


def convert_to_pdf(filename):
    cmd = f"libreoffice --headless --convert-to pdf /home/acarnec/Downloads/'{filename}'"
    subprocess.call(cmd, shell=True)
    new_filename = os.path.splitext(filename)[0] + ".pdf"
    return new_filename


def delete_docs():
    for f in os.listdir('/home/acarnec/Downloads'):
        if f.endswith(('.doc', '.docx')):
            delete(f)


def main():
    """Do the main stuff."""
    os.system("clear")

    dl = '/home/acarnec/Downloads/'

    pdfs_unformatted = listdir(dl)
    print(pdfs_unformatted)
    pdfs_formatted = [format_pdf_name(pdf) for pdf in pdfs_unformatted]
    pdfs_paths = [add_path_do_pdf(pdf, dl) for pdf in pdfs_formatted]
    print(pdfs_paths)
    for pdf in pdfs_paths:
        os.system("clear")
        pdf_obj = zathura(pdf)
        sleep(0.5)
        select_terminal()
        triage(pdf, pdf_obj)
        terminate_pdf(pdf_obj)
    delete_docs()


if __name__ == "__main__":
    main()

# TODO Make sure that no characters in the delete_docs function can interfere with the rm command.
