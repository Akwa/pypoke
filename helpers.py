# -*- coding: utf-8 -*-


def get_file_content(path, mode='rb'):
    with open(path, mode) as file:
        return file.read()