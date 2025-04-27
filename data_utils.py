# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 08:46:40 2025

@author: Administrator
"""


# data_utils.py
import json, os

def load_sanpham():
    if not os.path.exists("danhsach_aoquan.json"):
        return []
    with open("danhsach_aoquan.json", "r", encoding="utf-8") as f:
        content = f.read()
        return json.loads(content) if content.strip() else []

def luu_sanpham(data):
    with open("danhsach_aoquan.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def luu_hoadon(hoadon):
    ds = []
    if os.path.exists("hoadon.json"):
        with open("hoadon.json", "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():
                ds = json.loads(content)
    ds.append(hoadon)
    with open("hoadon.json", "w", encoding="utf-8") as f:
        json.dump(ds, f, ensure_ascii=False, indent=2)
