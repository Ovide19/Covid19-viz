#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 19:27:56 2020

@author: sheldon
"""
import os
import urllib
import yaml  
import folium
from folium import plugins
from folium import IFrame
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import earthpy as et
import pdb 
import flask
from flask import Flask
import numpy as np
import collections
import datetime
import numpy as np
import pandas as pd
import unidecode
import branca.colormap as cm
colormap =cm.linear.YlOrRd_09.scale(0, 1000)

     
legend_html = '''
<div style="position: fixed;
     padding: .5em; top: 10px; left: 60px; width: 30em; height: 10em;
     border:2px solid grey; z-index:9999; font-size:14px; background: #eee;
     "> &nbsp; Nombre de cas de COVID-19 par departement pour la France metropolitaine<br>
     &nbsp; Donnees tirees de https://github.com/opencovid19-fr/data  <br>
     &nbsp; Carte interactive creee par: &nbsp;</i><br>
     &nbsp; - Sheldon Warden: sheldon.warden@protonmail.com &nbsp;</i><br>
     &nbsp; - Pierre Thierry: pierre@nothos.net &nbsp; </i>
</div>
'''


class CovidData(object):


    def __init__(self):
         self.Confirmed_Cases = pd.read_csv('https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.csv')
         self.Departements = {                
                  'DEP-29': [48.26111111, -4.058888889], 
                  'DEP-22': [48.44111111, -2.864166667], 
                  'DEP-56': [47.84638889, -2.81], 
                  'DEP-44': [47.36138889, -1.682222222], 
                  'DEP-35': [48.15444444, -1.638611111],
                  'DEP-51': [48.9405, 4.24555], 
                  'DEP-10': [48.30444444, 4.161666667], 
                  'DEP-52': [48.1022, 5.18945], 
                  'DEP-08': [49.61555556, 4.640833333], 
                  'DEP-55': [48.98944444, 5.37408], 
                  'DEP-54': [48.78694444, 6.165], 
                  'DEP-57': [49.03722222, 6.663333333], 
                  'DEP-88': [48.19666667, 6.3805555567], 
                  'DEP-67': [48.67083333, 7.551388889], 
                  'DEP-68': [47.85861111, 7.274166667],
                  'DEP-50': [49.07944444, -1.3275],
                  'DEP-14': [49.09972222, -0.363611111],
                  'DEP-65': [48.62361111, 0.128888889],
                  'DEP-27': [49.11361111, 0.996111111],
                  'DEP-59': [50.44722222, 3.220555556],
                  'DEP-61': [48.62361111, 0.128888889],
                  'DEP-62': [50.49361111, 2.288611111],
                  'DEP-28': [48.3875, 1.370277778],
                  'DEP-72': [47.99444444, 0.222222222],
                  'DEP-49': [47.39083333, -0.564166667],
                  'DEP-37': [47.25805556, 0.691388889],
                  'DEP-86': [46.56388889, 0.460277778],
                  'DEP-79': [46.55555556, -0.317222222],
                  'DEP-17': [45.78083333, -0.674444444],
                  'DEP-16': [45.71805556, 0.201666667],
                  'DEP-33': [44.82527778, -0.575277778],
                  'DEP-47': [44.3675, 0.460277778],
                  'DEP-40': [43.96555556, -0.783888889],
                  'DEP-32': [43.69277778, 0.453333333],
                  'DEP-64': [43.25666667, -0.761388889],
                  'DEP-65': [43.05305556, 0.163888889],
                  'DEP-09': [42.92083333, 1.503888889],
                  'DEP-11': [43.10333333, 2.414166667],
                  'DEP-82': [44.08583333, 1.281944444],
                  'DEP-81': [43.78527778,2.166111111],
                  'DEP-34': [43.57972222, 3.367222222],
                  'DEP-13': [43.54333333, 5.086388889],
                  'DEP-83': [43.46055556, 6.218055556],
                  'DEP-05': [44.66361111, 6.263055556],
                  'DEP-26': [44.68416667, 5.168055556],
                  'DEP-43': [45.12805556, 3.806388889],
                  'DEP-69': [45.87027778, 4.641388889],
                  'DEP-74': [46.03444444, 6.428055],
                  'DEP-71': [46.64472222, 4.542222222],
                  'DEP-03': [46.39361111, 3.188333333],
                  'DEP-18': [47.06472222, 2.491111111],
                  'DEP-91': [48.52222222, 2.243055556],
                  'DEP-92': [48.84722222,2.245833333],
                  'DEP-94': [48.7775, 2.468888889],
                  'DEP-93': [48.9175, 2.478055556],  
                  'DEP-80': [49.95805556, 2.277777778],
                  'DEP-78': [48.815, 1.841666667],
                  'DEP-06': [43.9375, 7.116388889],
                  'DEP-04': [44.10611111, 6.243888889],
                  'DEP-07': [44.75166667, 4.424722222],
                  'DEP-11': [43.10333333, 2.414166667],
                  'DEP-12': [44.28027778, 2.679722222],
                  'DEP-15': [45.05111111, 2.668611111],
                  'DEP-19': [45.35694444, 1.876944444],
                  'DEP-23': [46.09027778, 2.018888889],
                  'DEP-24': [45.10416667, 0.741388889],
                  'DEP-25': [47.16527778, 6.361666667],
                  'DEP-30': [43.99333333, 4.180277778],
                  'DEP-31': [43.35861111, 1.172777778],
                  'DEP-36': [46.77777778, 1.575833333],
                  'DEP-38': [45.26333333, 5.576111111],
                  'DEP-39': [46.72833333, 5.697777778],
                  'DEP-41': [47.61666667, 1.429444444],
                  'DEP-42': [45.72694444, 4.165833333],
                  'DEP-45': [47.91194444, 2.344166667],
                  'DEP-46': [44.62416667, 1.604722222],
                  'DEP-48': [44.51722222, 3.500277778],
                  'DEP-50': [49.07944444, -1.3275],
                  'DEP-53': [48.1333, -0.6833],
                  'DEP-58': [47.11527778, 3.504722222],
                  'DEP-60': [49.41027778, 2.425277778],
                  'DEP-63': [45.72583333, 3.140833333],
                  'DEP-65': [42.6,2.522222222],
                  'DEP-70': [47.64111111, 6.086111111],
                  'DEP-73': [45.4775, 6.443611111],
                  'DEP-75': [48.85666667, 2.342222222],
                  'DEP-76': [49.655, 1.026388889],
                  'DEP-77': [48.62666667, 2.933333333],
                  'DEP-82': [44.08583333, 1.281944444],
                  'DEP-85': [43.99388889, 5.186111111],
                  'DEP-87': [45.89166667, 1.235277778],
                  'DEP-89': [47.83972222, 3.564444444],
                  'DEP-90': [47.63166667, 6.928611111],
                  'DEP-95': [49.08277778, 2.131111111],
                  'DEP-2B': [42.39416667, 9.206388889],
                  'DEP-2A': [41.86361111, 8.988055556]
                  } 
         
         self.Regions={'REG-52': [47.4667, -0.7833],
                  'REG-27': [47.24, 4.818],
                  'REG-32': [49.9667, 2.7833],      
                  'REG-84': [45.5167, 4.5333],
                  'REG-76': [43.7073, 2.1385],
                  'REG-53': [48.2, -2.85],
                  'REG-24': [47.5, 1.6833],
                  'REG-94': [42.1667, 9.1667],
                  'REG-44': [48.6833, 5.6167],
                  'REG-11': [48.7, 2.5],
                  'REG-28': [49.1333, 0.1],
                  'REG-75': [45.2, 0.1833],
                  'REG-93': [43.9333, 6.0333]
                  }
         
         self.Coordinates=pd.DataFrame.from_dict(self.Departements, orient='index')
         self.Coordinates['maille_code']=self.Coordinates.index
         
         self.map = folium.Map(location=[46,2],
              tiles = 'Stamen Terrain',
              zoom_start=6)
         
         self.merged_data_last = None
         self.merged_data_penultimate = None


    def merge_data_and_coordinates(self):
         self.merged_data=self.Confirmed_Cases.merge(self.Coordinates, left_on='maille_code', right_on='maille_code')

        
    def drop_rows_for_which_confirmed_cases_are_missing(self):
         self.merged_data=self.merged_data.dropna(subset=['hospitalises'])

    def select_last_date(self):
         self.merged_data_last=self.merged_data.sort_values('date').groupby('maille_code').tail(1)

    def select_penultimate_date(self):
         merged_data_penultimate_temp=self.merged_data.sort_values('date').groupby('maille_code').tail(2)
         self.merged_data_penultimate=merged_data_penultimate_temp.sort_values('date').groupby('maille_code').head(1)

    def compute_change_in_cases(self):
          self.merged_data_diff=self.merged_data_last.merge(self.merged_data_penultimate, left_on='maille_code', right_on='maille_code')
          self.merged_data_diff['difference']=self.merged_data_diff['hospitalises_x']-self.merged_data_diff['hospitalises_y']
          self.merged_data_diff.to_csv('difftest.csv')

    def plot_departements(self,data,custom_color):
         radius = data['hospitalises_x'].values.astype('float')
         latitude = data['0_x'].values.astype('float')
         longitude = data['1_y'].values.astype('float')
         nom = data['maille_nom_x'].values.astype('str')   
         latest_date = data['date_x'].values.astype('str')
         penultimate_date = data['date_y'].values.astype('str')         
         difference = data['difference'].values.astype('str')
         for la,lo,ra,no,di,ld,pd in zip(latitude,longitude,radius,nom,difference,latest_date,penultimate_date):
              label=unidecode.unidecode(no.replace("'","-"))+': '+str(ra)[:-2]+ ' patients hospitalises au '+str(ld)+'. +'+str(di)[:-2]+' cas depuis le '+str(pd)+'.'
              folium.Circle(
                       location=[la,lo],
                       radius=5000*np.log(ra),
                       fill=True,
                       color='grey',
                       fill_color=colormap(ra),
                       fill_opacity=0.8
                   ).add_child(folium.Popup(label)).add_to(self.map)
#              if ra<50:
#                   folium.Circle(
#                       location=[la,lo],
#                       radius=17000,
#                       fill=True,
#                       opacity = 0.5,
#                       color='white',
#                       fill_color='white',
#                       fill_opacity=0.5
#                   ).add_child(folium.Popup(label)).add_to(self.map)
#              elif ra<500:
#                   folium.Circle(
#                       location=[la,lo],
#                       radius=5000*np.log(ra),
#                       fill=True,
#                       color='orange',
#                       fill_color=colormap(ra),
#                       fill_opacity=0.8
#                   ).add_child(folium.Popup(label)).add_to(self.map)
#              else:
#                  folium.Circle(
#                       location=[la,lo],
#                       radius=31073,
#                       fill=True,
#                       color='red',
#                       fill_color='red',
#                       fill_opacity=1
#                   ).add_child(folium.Popup(label)).add_to(self.map)

               

def create_map():
            
     CODA=CovidData()
     CODA.merge_data_and_coordinates()
     CODA.drop_rows_for_which_confirmed_cases_are_missing()
     CODA.select_penultimate_date()
     CODA.select_last_date()
     CODA.compute_change_in_cases()     
     CODA.plot_departements(CODA.merged_data_diff,'grey')

     CODA.map.get_root().html.add_child(folium.Element(legend_html))
     colormap.caption = 'Nombre de cas de COVID-19 par departement (Source: opencovid19-fr)'
     CODA.map.add_child(colormap)

     return CODA



#CODA.map.save("./test_map.html")

page_template = '''<!doctype html>

<html lang="fr">
<head>
  <meta charset="utf-8">

  <title>Carte de la France du Covid-19</title>
</head>

<body>
{map}
</body>
</html>
'''

Coda = None

def update_map():
     global Coda
     Coda = create_map()

app = Flask(__name__)
@app.route("/")
def display_map():
     return page_template.format(map=Coda.map._repr_html_())

update_prefix = os.environ.get('UPDATE_PREFIX', '')
@app.route("/{prefix}update".format(prefix=update_prefix), methods=['POST'])
def update_data():
     update_map()
     return ""


form_template = '''<!doctype html>

<html lang="fr">
<head>
  <meta charset="utf-8">

  <title>Mettre à jour la carte de la France du Covid-19</title>
</head>

<body>
<form action="/{prefix}update" method="POST">
<input type="submit" value="Update!">
</body>
</html>
'''

@app.route("/{prefix}updateform".format(prefix=update_prefix))
def update_form():
     return form_template.format(prefix=update_prefix)


update_map()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 80))