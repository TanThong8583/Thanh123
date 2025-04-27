# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 08:46:27 2025

@author: Administrator
"""


# models.py
class SanPham:
    def __init__(self, maSP, tenSP, giaBan, image):
        self.maSP = maSP
        self.tenSP = tenSP
        self.giaBan = giaBan
        self.image = image

    def chuyen_dict(self):
        return {
            'maSP': self.maSP,
            'tenSP': self.tenSP,
            'giaBan': self.giaBan,
            'image': self.image
        }
