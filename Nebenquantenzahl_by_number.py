#!/bin/env/python

import string


def stringType(L):
    #* List for all letters
    #* Get index of 'f' 
    alphabet_list = list(string.ascii_lowercase)
    f_index = alphabet_list.index('f') 
    l_dict = {
        num : l 
        for num, l in 
        zip(range(13),
            ['s', 'p', 'd'] + alphabet_list[f_index:f_index+10])
        }            
    return l_dict.get(L) 
