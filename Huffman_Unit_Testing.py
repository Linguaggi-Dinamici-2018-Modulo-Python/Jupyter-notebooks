#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Set of unit tests for the Huffman module

Created on Fri Oct  5 11:48:13 2018

@author: Mauro Leoncini
"""

import unittest
from os import system
from random import randint
from Huffman import filereader, priority_queue, compress, decompress

class knownCounts(unittest.TestCase):
    '''Classe che contiene test per le funzionalità di filereader'''
    known_Counts = (('Huffman/testfile1', 34474),
                    ('Huffman/testfile2', 33792),
                    ('Huffman/testfile3', 1471),
                    ('Huffman/testfile4', 1123))

    def test_iterable_filereader(self):
        '''La classe enc_ind_File deve essere un iterabile che fornisce
           lo stesso numero di caratteri dato dal comando linux wc'''
        for filename, wc_count in self.known_Counts:
            file = filereader(filename)
            count = 0
            for _ in file:
                count += 1
            self.assertEqual(count, wc_count)

    def test_frequencies_filereader(self):
        '''La classe enc_ind_File deve fornire le frequenze corrette
           dei caratteri nel file. Il controllo viene però fatto
           sulla somma, che deve essere uguale al conteggio fornito
           dal comando linux wc'''
        for filename, wc_count in self.known_Counts:
            file = filereader(filename)
            count = 0
            for freq in file.frequencies.values():
                count += freq
            self.assertEqual(count, wc_count)

class sortedSequences(unittest.TestCase):
    '''Classe per testare le funzionalità della coda con priorità'''
    num_seq = 10          # 10 sequenze
    len_seq = 100         # di 100 numeri
    sorted_Sequences = []
    for _ in range(num_seq):
        seq = [randint(1, 1000) for i in range(len_seq)]
        sorted_Sequences.append((seq, sorted(seq)))

    def test_priority_queue(self):
        '''La coda con priorità deve restituire tutti gli
            elementi in ordine crescente, consentendo quindi anche
            di ordinarli'''
        for seq, sorted_seq in self.sorted_Sequences:
            queue = priority_queue()
            for item in seq:
                queue.insert(item)
            seq_sorted = []
            while not queue.is_empty():
                seq_sorted.append(queue.minimum())
            self.assertEqual(seq_sorted, sorted_seq)

class sanityCheck(unittest.TestCase):
    '''Classe per il sanity check di verifica, che cioè il file
       ripristinato dopo la decompressione coincida con il file
       originale'''

    test_files = (('Huffman/testfile1'),
                  ('Huffman/testfile2'),
                  ('Huffman/testfile3'),
                  ('Huffman/testfile4'))

    def test_sanity(self):
        '''Check for file equality'''
        for file in self.test_files:
            compressed_file = compress(file)
            decompressed_file = decompress(compressed_file)
            retcode = system("cmp "+decompressed_file+" "+file)
            self.assertEqual(retcode, 0)
    