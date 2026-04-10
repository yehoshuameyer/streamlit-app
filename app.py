#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:29:10 2026

@author: zoschi
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt


# Gleichtaktdrosseln

cmc_DYEF = pd.DataFrame({
    "subckt": [
        "S_744822301_1m",
        "S_744822222_2.2m",
        "S_744822233_3.3m",
        "S_744822110_10m",
        "S_744822120_20m",
        "M_744823601_1m",
        "M_744823422_2.2m",
        "M_744823305_5m",
        "M_744823210_10m",
        "M_744823220_20m",
        "L_744824801_1m",
        "L_744824622_2.2m",
        "L_744824433_3.3m",
        "L_744824310_10m",
        "L_744824220_20m",
        "M_7448030509_9m",
        "L_7448040707_7m",
        "LF_SH_74466240007_0m7",
        "LF_SH_7446622002_2m2",
        "LF_SH_7446621007_6m8",
        "LF_SH_7446620027_27m"     
              
        
    ],
   
    "I": [
        3,
        2,
        1.5,
        1,
        0.5,
        6,
        4,
        2.5,
        2,
        1.5,
        7.5,
        6,
        4,
        3,
        2,
        5,
        7,
        4,
        2,
        1,
        0.4             
    ]
})


# Übersschrift 
st.title("Ergebnisse Filtersimulation")


#Eingabe Filter-Parameter

strom_max = st.number_input("maximaler Strom in A: ")
#st.write("maximaler Strom:",strom_max)



eingabe_freq, eingabe_db = st.columns(2)

with eingabe_freq:
    freq_filter = st.number_input("Filterfrequenz f in e+8 Hz: ")

with eingabe_db:
    db_filter = st.number_input("mindest Dämpfung bei f: ")


eingabe_freq1, eingabe_db1 = st.columns(2)

with eingabe_freq:
    freq_filter1 = st.number_input("Filterfrequenz f1 in e+8 Hz: ")

with eingabe_db:
    db_filter1 = st.number_input("mindest Dämpfung bei f1: ")

filter_ord = st.number_input("Filter Ordnung: ")

spulen_limit =  cmc_DYEF[cmc_DYEF["I"] >= strom_max] ["subckt"]

spulen_limit = pd.concat(                            
    [spulen_limit, pd.Series(["without"])],
    ignore_index=True
)


freq = np.load("Daten/f.npy")
freq_real = freq.real

freq_index = np.argmin(np.abs(freq_real - freq_filter*1e8))
freq_index1 = np.argmin(np.abs(freq_real - freq_filter1*1e8))
st.write("frequnez index",freq_index)

with open("Daten/03_DYEF_Simlist_50+RealImp.pkl", "rb") as f:
    data = pickle.load(f)

    # Befindet sich der Spulennamen von Strom Limit in Data ? 
    filter_strom = data[data["csub"].isin(spulen_limit)]   

    filter_freq = filter_strom[filter_strom["adm_db"].apply(lambda x: -1*x[freq_index]) > db_filter]

    filter_freq1 = filter_freq[filter_freq["adm_db"].apply(lambda x: -1*x[freq_index1]) > db_filter1]

    db_diff = filter_freq1.iloc[:, 12]
    db_comm = filter_freq1.iloc[:,13]
    


# Diagramm mit Matplotlib

fig1, ax1 = plt.subplots()

for zeile in db_diff:
    ax1.plot(freq, zeile)    

ax1.set_title("Dämpfung Differantialmode")
ax1.set_xlabel("f")
ax1.set_ylabel("db")

fig2, ax2 = plt.subplots()

for zeile in  db_comm :
    ax2.plot(freq, zeile)    

ax2.set_title("Dämpfung Commenmode")
ax2.set_xlabel("f")
ax2.set_ylabel("db")


# In Streamlit anzeigen


col1, col2 = st.columns(2)

with col1:
    st.pyplot(fig1)

with col2:
    st.pyplot(fig2)


