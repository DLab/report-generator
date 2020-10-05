# -*- coding: utf-8 -*-
"""
dlab
Computational Biology Lab
Fundación Ciencia y Vida
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import numpy as np
import datetime as dtime
import locale
from math import ceil
import gc
import os
import requests
import json
#logos
logos = mpimg.imread('logos/uss_cinv_udd.png')
logo_sochimi = mpimg.imread('logos/logo_sochimi.png')
logo_fcv = mpimg.imread('logos/logos.png')
logofcv = mpimg.imread('logos/logo_fcv.png')
logofinis = mpimg.imread('logos/logo_finis.png')
# popu = pd.read_excel("sochimi/poblacion2020_nacional.xlsx",  index_col = 0)
popu =pd.read_json('http://192.168.2.223:5006/getComunas')
popu = popu[['state', 'state_name', 'county', 'county_name', 'province_name', 'male_pop', 'female_pop', 'total_pop']]
#counties_info.index = counties_info['county'].astype(str).apply(lambda x:x.zfill(5))
popu = popu.set_index('county_name')

# list and dicts
regiones = ['Arica y Parinacota',
            'Tarapacá',
            'Antofagasta',
            'Atacama',
            'Coquimbo',
            'Valparaíso',
            'Libertador General Bernardo O\'Higgins',
            'Maule',
            'Ñuble',
            'Biobío',
            'La Araucanía',
            'Los Ríos',
            'Los Lagos',
            'Aysén del General Carlos Ibáñez del Campo',
            'Magallanes y de la Antártica Chilena',
            'Metropolitana de Santiago']

region_names_dict = {
                        'Tarapaca':'Tarapacá',
                        'Valparaiso':'Valparaíso',
                        'Metropolitana':'Metropolitana de Santiago',
                         'Del Libertador General Bernardo O’Higgins':"Libertador General Bernardo O'Higgins",
                         'Nuble':'Ñuble',
                         'Biobio':'Biobío',
                         'La Araucania':'La Araucanía',
                         'Los Rios':'Los Ríos',
                         'Aysen':'Aysén del General Carlos Ibáñez del Campo',
                         'Magallanes y la Antartica':'Magallanes y de la Antártica Chilena'
                     }

order = [
        'SS ARICA',
        'SS IQUIQUE',
        'SS ANTOFAGASTA',
        'SS ATACAMA',
        'SS COQUIMBO',
        'SS ACONCAGUA',
        'SS VIÑA DEL MAR QUILLOTA',
        'SS VALPARAISO SAN ANTONIO',
        'SS LIBERTADOR B. O\'HIGGINS',
        'SS DEL MAULE',
        'SS ÑUBLE',
        'SS BÍO BÍO',
        'SS CONCEPCIÓN',
        'SS TALCAHUANO',
        'SS ARAUCO',
        'SS ARAUCANÍA NORTE',
        'SS ARAUCANÍA SUR',
        'SS VALDIVIA',
        'SS OSORNO',
        'SS DEL RELONCAVÍ',
        'SS CHILOÉ',
        'SS AISÉN',
        'SS MAGALLANES',
        'SS METROPOLITANO NORTE',
        'SS METROPOLITANO OCCIDENTE',
        'SS METROPOLITANO CENTRAL',
        'SS METROPOLITANO ORIENTE',
        'SS METROPOLITANO SUR',
        'SS METROPOLITANO SUR ORIENTE'
]

indices_dict={'Til Til':'Tiltil',
                      'Ránqui':'Ránquil',
                      'Pitrufquén':'Pitrufquen',
                      'Paihuano':'Paiguano',
                      'Los Ángeles':'Los Angeles',
                      'Llay-Llay':'Llaillay',
                      'San Pedro de La Paz':'San Pedro de la Paz',
                      'La Calera': 'Calera',
                      'Copiapo': 'Copiapó',
                      'Vicuna': 'Vicuña',
                      'Concon': 'Concón',
                      'Vina del Mar':'Viña del Mar',
                      'Valparaiso':'Valparaíso',
                      'Quilpue':'Quilpué',
                      'Curico':'Curicó',
                      'Longavi':'Longaví',
                      'Hualpen':'Hualpén',
                      'Machali':'Machalí',
                      'Chillan':'Chillán',
                      'Camina':'Camiña',
                      'Concepcion':'Concepción',
                      'Requinoa':'Requínoa',
                      'Alhue':'Alhué',
                      'Maria Elena':'María Elena',
                      'Maria Pinto':'María Pinto',
                      'Donihue':'Doñihue',
                      'Colbun':'Colbún',
                      'Constitucion':'Constitución',
                      'Chillan Viejo':'Chillán Viejo',
                      'Canete':'Cañete',
                      'Alto Biobio':'Alto Biobío',
                      'Tome':'Tomé',
                      'Los Alamos':'Los Álamos',
                      'Vilcun':'Vilcún',
                      'Mulchen':'Mulchén',
                      'Santa Barbara':'Santa Bárbara',
                      'Conchali':'Conchalí',
                      'Curacavi':'Curacaví',
                      'Estacion Central':'Estación Central',
                      'Maipu':'Maipú',
                      'Nunoa':'Ñuñoa',
                      'Penaflor':'Peñaflor',
                      'Penalolen':'Peñalolén',
                      'San Joaquin':'San Joaquín',
                      'San Jose de Maipo':'San José de Maipo',
                      'San Ramon':'San Ramón',
                      'Olmue':'Olmué',
                      'Puchuncavi':'Puchuncaví',
                      'Coinco':'Coinco',
                      'Chepica':'Chépica',
                      'Rio Claro':'Río Claro',
                      'Quillon':'Quillón',
                      'Niquen':'Ñiquén',
                      'San Nicolas':'San Nicolás',
                      'Vilcun':'Vilcún',
                      'Chanaral':'Chañaral',
                      'Combarbala':'Combarbalá',
                      'Rio Hurtado': 'Río Hurtado',
                      'Santa Maria': 'Santa María',
                      'Licanten':'Licantín',
                      'San Fabian':'San Fabián',
                      'Ranquil':'Ránquil',
                      'Tirua':'Tirúa',
                      'Traiguen':'Traiguén',
                      'Pucon':'Pucón',
                      'Curacautin':'Curacautín',
                      'Puren':'Purén',
                      'Tolten':'Toltén',
                      'Rio Bueno':'Río Bueno',
                      'Mafil':'Máfil',
                      'La Union':'La Unión',
                      'Maullin':'Maullín',
                      'Cochamo':'Cochamó',
                      'Rio Negro':'Río Negro',
                      'Chaiten' :'Chaitén',
                      'Aysen':'Aysén',
                      'Licanten':'Licantén',
                      'Quellon':'Quellón',
                      'Hualaihue': 'Hualaihué',
                      'Coihaique':'Coyhaique'}

regiones_short = ['Arica y Parinacota',
            'Tarapacá',
            'Antofagasta',
            'Atacama',
            'Coquimbo',
            'Valparaíso',
            'O’Higgins',
            'Maule',
            'Ñuble',
            'Biobío',
            'Araucanía',
            'Los Ríos',
            'Los Lagos',
            'Aysén',
            'Magallanes',
            'Metropolitana']

def __iso_handler(x): #overk
    for i, item in enumerate(x.values):
        s = item.split('T')
    return s[0]

def color_rate(data):
    if data <= .25: color = '#00cc66'
    elif (data < .30): color = '#ffcc00'
    else: color = '#ff0000'
    return color

def color_prvlnc(data):
    if data <= 4.: color = '#00cc66'
    elif data < 5.: color = '#ffcc00'
    else: color = 'red'
    return color

def color_r0(data):
    if data == 0.0: color = 'w'
    elif data <= .8: color = '#00cc66'
    elif data < 1.00: color = '#ffcc00'
    else: color = 'red'
    return color

def color_im(data):
    if data <= 2.: color = '#00cc66'
    elif data < 4.: color = '#ffcc00'
    else: color = 'red'
    return color

def color_dim(data):#23, 41, 58
    if data <= .3: color = '#00cc66'
    elif data < .4: color = '#ffcc00'
    else: color = '#ff0000'
    return color

def color_camas(data):#23, 41, 58
    if data <= .25: color = '#00cc66'
    elif data < .75: color = '#ffcc00'
    else: color = '#ff0000'
    return color

def report_date():
    endpoint_R = requests.get('http://192.168.2.223:5006/getNationalEffectiveReproduction' )
    R = json.loads(endpoint_R.text)
    year, month, day = str(R['dates'][-1].split('T')[0]).split('-')
    date = dtime.datetime(int(year),int(month),int(day))
    date += dtime.timedelta(days=1)

    report_day = date.strftime("%d/%m")
    return date.date() , report_day
    # return str(date).split(' ')[0]#.replace("-","_")

def last_data_day():
    '''
    It calculates the nearest past Tuesday or Saturday
    output:

    data_day , report_day

    data_day: datetime object
    report_day: "day/month" string format
    '''
    weekday =  dtime.date.today().weekday()
    if weekday>=1 and weekday<5: # nearest Tu
        dif = weekday-1
    else:
        dif = (weekday-5)%7

    data_day = dtime.date.today() - dtime.timedelta(days=dif)
    report_day = data_day.strftime("%d/%m")
    return data_day, report_day

def cover(report_day, delta):
    logos = mpimg.imread('logos/uss_cinv_udd.png')
    logo_sochimi = mpimg.imread('logos/logo_sochimi.png')
    logo_fcv = mpimg.imread('logos/logos.png')
    logofcv = mpimg.imread('logos/logo_fcv.png')
    logofinis= mpimg.imread('logos/logo_finis.png')
    sns.set_context("paper", font_scale=1)
    figcover = plt.figure(edgecolor='k', figsize=(11,8.5))
    axlogos = figcover.add_axes([0.05,.67,.3*1.1,.3*1.1]) # [0.05,.7,.3,.3]
    axsochi = figcover.add_axes([0.30,.8,.2*1.2,.085*1.2])
    axfcv = figcover.add_axes([.8,.75,.15,.2])
    axmain = figcover.add_axes([.0,.0,1,.9])
    axlogos.imshow(logos)
    axsochi.imshow(logo_sochimi)
    axfcv.imshow(logo_fcv[:,:1000])
    axmain.axis('off')
    axlogos.axis('off')
    axsochi.axis('off')
    axfcv.axis('off')
    authors = 'César Ravello$^{1,3}$, Felipe Castillo¹, Soraya Mora$^{1,3}$, Alejandra Barrios¹, César Valdenegro¹, Tomás Veloz¹, Tomás Pérez-Acle$^{1,2,3}$'
    affiliations = '¹Computational Biology Lab, Fundación Ciencia & Vida, Santiago, Chile\n²Centro Interdisciplinario de Neurociencia de Valparaíso, Universidad de Valparaíso, Chile\n³Universidad San Sebastián, Chile\n'
    axmain.text(.5,.7, 'Impacto de la pandemia Covid19 en Chile', ha='center', fontsize='xx-large')
    axmain.text(.5,.6, 'Reporte al ' + report_day + '\nSemana epidemiológica {}'.format(ceil(delta.days/7)), ha='center', fontsize='xx-large')
    axmain.text(.5,.25, authors, ha='center')
    axmain.text(.5,.15, affiliations, ha='center', fontsize='small')
    filename = 'Report/cover_{}_R.pdf'.format(report_day.replace('/','_'))
    figcover.savefig(filename, dpi=600)
    return filename

def hospitales_page(report_day, camas, camas2, chile_avg_rate, chile_prvlnc, sochi_dates):
    sochi_date2, sochi_date = pd.to_datetime(sochi_dates[0]).strftime("%d/%m"),pd.to_datetime(sochi_dates[1]).strftime("%d/%m")
    sns.set_context("paper", font_scale=.6)
    fig = plt.figure(figsize=(11, 8.5))
    fig.text(0.95,0.095,
             'Dato uso de camas por Servicio de Salud al '+sochi_date+'. Fuente: SOCHIMI.\n'+
             'Flechas indican cambio en el uso de camas con respecto al '+sochi_date2+'\n'
             'Datos epidemiológicos https://github.com/MinCiencia/Datos-COVID19', ha='right')
    fig.text(0.95,0.06, '©2020, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha='right', fontsize='large')
    ax_logo = fig.add_axes([.85,.875,.1,.1])
    ax_logo.imshow(logofcv)
    ax_logo.axis('off')
    ax_cinv = fig.add_axes([.08,.875,.25,.08])
    ax_sochi = fig.add_axes([.775,.885,.07,.07])
    ax_finis = fig.add_axes([.775,.885,.07,.07])
    ax_cinv.imshow(logos)
    ax_sochi.imshow(logo_sochimi)
    ax_cinv.axis('off')
    ax_sochi.axis('off')


    fig.text(.5, .935, 'Uso de camas según Servicio de Salud',
             horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='x-large')

    fig.text(.375, .89, 'Uso camas \u2264 25%', color='#00cc66', horizontalalignment='center', verticalalignment='center', weight = 'bold')
    fig.text(.5, .89, '25% < Uso camas < 75%', color='#ffcc00', horizontalalignment='center', verticalalignment='center', weight = 'bold')
    fig.text(.625, .89, 'Uso camas \u2265 75%', color='#ff0000', horizontalalignment='center', verticalalignment='center', weight = 'bold')

    ax = fig.add_axes([.2, .0, .7, .85])
    make_camas(ax, camas, camas2)
    fig.savefig('Report/Report_{}_P17.pdf'.format(report_day.replace('/','_')), dpi=1200)
    filename = 'Report/Report_{}_RP17.pdf'.format(report_day.replace('/','_'))
    fig.savefig(filename, dpi=1200)
    return filename

def otras_provincias_page(report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last, im1,im2,death_rate1,death_rate2, sochi_date, im_dates ):
    sns.set_context("paper", font_scale=.6)
    every_nth = 7

    ## Encabezados, pies de página y leyendas
    fig = plt.figure(figsize=(11, 8.5))
    ## Logos
    fig.text(0.95,0.06, '©2020, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha='right', fontsize='large')
    ax_logo = fig.add_axes([.85,.875,.1,.1])
    ax_logo.imshow(logofcv)
    ax_logo.axis('off')
    ax_cinv = fig.add_axes([.05,.875,.25,.08])
    ax_sochi = fig.add_axes([.775,.885,.07,.07])
    ax_cinv.imshow(logos)
    ax_sochi.imshow(logo_sochimi)
    ax_cinv.axis('off')
    ax_sochi.axis('off')

    ## Encabezado
    region = 'Metropolitana de Santiago'
    r = 15
    fig.text(.5, .935, 'Región Metropolitana: otras provincias', horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='xx-large')
    fig.text(.5, .9, 'Datos últimos 14 días\nPrevalencia región: {} / Tasa región: {}%\nEstimación de infectados sintomáticos detectados: {}'.format('{:.2f}'.format(prevalencia_region.loc[3,'Metropolitana de Santiago']).replace('.',','), '{:.2f}'.format(region_avg_rate.loc[3,'Metropolitana de Santiago']*100).replace('.',','), subrep.underreporting_estimate_clean.loc['Metropolitana de Santiago']),
         horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='x-large')

    ## Leyendas
    fig.text(.187, .825, '1', fontsize='small')
    fig.text(.2335, .825, '2', fontsize='small')
    fig.text(.2775, .825, '3', fontsize='small')
    fig.text(.3405, .825, '4', fontsize='small')
    fig.text(.4225, .825, '5', fontsize='small')
    fig.text(.4825, .825, '6', fontsize='small')
    fig.text(.5275, .825, '7', fontsize='small')
    fig.text(.5875, .825, '7', fontsize='small')
    fig.text(.605, .52, 'Prevalencia \u2264 4', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .51, '4 < Prevalencia < 5', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .5, 'Prevalencia \u2265 5', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

    fig.text(.605, .47, 'Tasa \u2264 25%', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .46, '25% < Tasa < 30%', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .45, 'Tasa \u2265 30%', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

    fig.text(.605, .42, 'R_e \u2264 0,8', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .41, '0,8 < R_e < 1,0', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .4, 'R_e \u2265 1,0', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

    fig.text(.605, .37, 'Movilidad remanente \u2264 30%', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .36, '30% < Movilidad remanente < 40%', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .35, 'Movilidad remanente \u2265 40%', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

    fig.text(0.605,0.06,
             '1 Infectados activos / 10.000 habitantes.\n'+
             '2 Tasa diaria de nuevos infectados (promedio acumulado).\n'+
             '3 R_e últimos 14 días según Cori et al. (2019)\n'
             '4 Datos epidemiológicos\nhttps://github.com/MinCiencia/Datos-COVID19\n'+
             '5 De acuerdo a subreporte según\nhttps://cmmid.github.io/topics/covid19/global_cfr_estimates.html\n'+
             '6 Fallecimientos acumulados COVID19 / 100.000 habitantes\n'+
             '7 Datos movilidad '+im_dates+' vs. 09/03-15/03.\n'+
                 'https://github.com/MinCiencia/Datos-COVID19, producto 33.\n'+
             '8 Datos regionales incluyen casos de comuna desconocida\n'+'\n'+
             '- ND no hay suficientes datos para calcular R_e.\n'+
             '- Uso de camas por Servicio de Salud al ' + sochi_date + ' según SOCHIMI.\n'+
             '- Flechas R_e: cambio mayor/menor a 5% vs ultimos 7 días.\n'+
             '- Otras flechas: cambio mayor/menor a 5% vs semana anterior.\n'
             , ha='left',fontsize='x-large')

    ax = fig.add_axes([.125, .01, .475, .84])
    selection = pop[(pop['state_name']=='Metropolitana de Santiago')&(pop['province_name']!='Santiago')].index.values
    #make_table(display.loc[selection], display_values.loc[selection], ax, True)
    make_table(display.loc[selection], display_values.loc[selection],
                   reg_display[reg_display.index==region].rename(index={region:'VALOR REGIONAL ⁸'}), reg_display_values[reg_display.index==region], ax, True)
    add_arrows(display_values.loc[selection], muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last, im1,im2,death_rate1,death_rate2, ax, 0.49, .935, .18, .06, .29,.68,.905,.0315, .0205)
    #fig.text(.12, .85, 'Región de ' + regiones[r], horizontalalignment='left', verticalalignment='center', weight = 'bold')

    ax2 = fig.add_axes([.645, .595, .3, .22])
    comuna = regiones_short[r]
    comuna = region

    ax2.plot(data[data.name==comuna]['MEAN'][1:])
    ax2.fill_between(data[data.name==comuna].index[1:],
                     data[data.name==comuna]['Low_95'][1:], data[data.name==comuna]['High_95'][1:], alpha=.4)
    ax2.hlines(data[data.name==comuna]['MEAN'][-14:].mean(), data[data.name==comuna].iloc[-14].name,data[data.name==comuna].iloc[-1].name, color='C4')
    ax2.hlines(data[data.name==comuna]['MEAN'][-7:].mean(), data[data.name==comuna].iloc[-7].name,data[data.name==comuna].iloc[-1].name, color='C2')
    ax2.hlines(1, data[data.name==comuna].iloc[1].name,data[data.name==comuna].iloc[-1].name, ls='--',color='k')
    ax2.annotate('R_e 14d = {:.2f}'.format(data[data.name==comuna]['MEAN'][-14:].mean()), (.75,.7), color='C4',xycoords='axes fraction')
    ax2.annotate('R_e 7d = {:.2f}'.format(data[data.name==comuna]['MEAN'][-7:].mean()), (.75,.65), color='C2',xycoords='axes fraction')
    ax2.annotate('R_e inst. = {:.2f}'.format(data[data.name==comuna]['MEAN'][-1]), (.75,.60), color='k',xycoords='axes fraction')
    matplotlib.pyplot.sca(ax2)
    plt.xticks(rotation=45)
    ax2.tick_params(bottom=False, left=True, labelleft=True, labelbottom=True)
    for n, label in enumerate(ax2.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    ax2.set_ylabel('R efectivo')
    ax2.set_ylim([0,3])

    filename = 'Report/Report_{}_RP{}.pdf'.format(report_day.replace('/','_'), r+1)
    fig.savefig(filename, dpi=1200) # faltan reg display y sus copias values
    return filename

def metropolitana_page(report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last, im1,im2,death_rate1,death_rate2, sochi_date, im_dates):
    sns.set_context("paper", font_scale=.6)
    every_nth = 7

    ## Encabezados, pies de página y leyendas
    fig = plt.figure(figsize=(11, 8.5))
    ## Logos
    fig.text(0.95,0.06, '©2020, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha='right', fontsize='large')
    ax_logo = fig.add_axes([.85,.875,.1,.1])
    ax_logo.imshow(logofcv)
    ax_logo.axis('off')
    ax_cinv = fig.add_axes([.05,.875,.25,.08])
    ax_sochi = fig.add_axes([.775,.885,.07,.07])
    ax_cinv.imshow(logos)
    ax_sochi.imshow(logo_sochimi)
    ax_cinv.axis('off')
    ax_sochi.axis('off')

    ## Encabezado
    region = 'Metropolitana de Santiago'
    r = 15
    fig.text(.5, .935, 'Región Metropolitana: Provincia de Santiago', horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='xx-large')
    fig.text(.5, .9, 'Datos últimos 14 días\nPrevalencia región: {} / Tasa región: {}%\nEstimación de infectados sintomáticos detectados: {}'.format('{:.2f}'.format(prevalencia_region.loc[3,'Metropolitana de Santiago']).replace('.',','), '{:.2f}'.format(region_avg_rate.loc[3,'Metropolitana de Santiago']*100).replace('.',','), subrep.underreporting_estimate_clean.loc['Metropolitana de Santiago']),
         horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='x-large')
    ## Leyendas
    fig.text(.187, .825, '1', fontsize='small')
    fig.text(.2335, .825, '2', fontsize='small')
    fig.text(.2775, .825, '3', fontsize='small')
    fig.text(.3405, .825, '4', fontsize='small')
    fig.text(.4225, .825, '5', fontsize='small')
    fig.text(.4825, .825, '6', fontsize='small')
    fig.text(.5275, .825, '7', fontsize='small')
    fig.text(.5875, .825, '7', fontsize='small')
    fig.text(.605, .52, 'Prevalencia \u2264 4', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .51, '4 < Prevalencia < 5', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .5, 'Prevalencia \u2265 5', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

    fig.text(.605, .47, 'Tasa \u2264 25%', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .46, '25% < Tasa < 30%', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .45, 'Tasa \u2265 30%', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

    fig.text(.605, .42, 'R_e \u2264 0,8', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .41, '0,8 < R_e < 1,0', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .4, 'R_e \u2265 1,0', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

    fig.text(.605, .37, 'Movilidad remanente \u2264 30%', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .36, '30% < Movilidad remanente < 40%', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
    fig.text(.605, .35, 'Movilidad remanente \u2265 40%', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

    fig.text(0.605,0.06,
             '1 Infectados activos / 10.000 habitantes.\n'+
             '2 Tasa diaria de nuevos infectados (promedio acumulado).\n'+
             '3 R_e últimos 14 días según Cori et al. (2019)\n'
             '4 Datos epidemiológicos\nhttps://github.com/MinCiencia/Datos-COVID19\n'+
             '5 De acuerdo a subreporte según\nhttps://cmmid.github.io/topics/covid19/global_cfr_estimates.html\n'+
             '6 Fallecimientos acumulados COVID19 / 100.000 habitantes\n'+
             '7 Datos movilidad '+im_dates+' vs. 09/03-15/03.\n'+
                 'https://github.com/MinCiencia/Datos-COVID19, producto 33.\n'+
             '8 Datos regionales incluyen casos de comuna desconocida\n'+'\n'+
             '- ND no hay suficientes datos para calcular R_e.\n'+
             '- Uso de camas por Servicio de Salud al ' + sochi_date + ' según SOCHIMI.\n'+
             '- Flechas R_e: cambio mayor/menor a 5% vs ultimos 7 días.\n'+
             '- Otras flechas: cambio mayor/menor a 5% vs semana anterior.\n'
             , ha='left',fontsize='x-large')

    ax = fig.add_axes([.125, .01, .475, .84])
    selection = pop[pop['province_name']=='Santiago'].index.values
    make_table(display.loc[selection], display_values.loc[selection],
                   reg_display[reg_display.index==region].rename(index={region:'VALOR REGIONAL ⁸'}), reg_display_values[reg_display.index==region], ax, True)
    add_arrows(display_values.loc[selection], muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last, im1,im2,death_rate1,death_rate2, ax, 0.21, .935, .18, .06, .29,.68,.905,.0315, .0205)

    ax2 = fig.add_axes([.645, .595, .3, .22])
    comuna = regiones_short[r]
    comuna = region
    ax2.plot(data[data.name==comuna]['MEAN'][1:])
    ax2.fill_between(data[data.name==comuna].index[1:],
                     data[data.name==comuna]['Low_95'][1:], data[data.name==comuna]['High_95'][1:], alpha=.4)
    ax2.hlines(data[data.name==comuna]['MEAN'][-14:].mean(), data[data.name==comuna].iloc[-14].name,data[data.name==comuna].iloc[-1].name, color='C4')
    ax2.hlines(data[data.name==comuna]['MEAN'][-7:].mean(), data[data.name==comuna].iloc[-7].name,data[data.name==comuna].iloc[-1].name, color='C2')
    ax2.hlines(1, data[data.name==comuna].iloc[1].name,data[data.name==comuna].iloc[-1].name, ls='--',color='k')
    ax2.annotate('R_e 14d = {:.2f}'.format(data[data.name==comuna]['MEAN'][-14:].mean()), (.75,.7), color='C4',xycoords='axes fraction')
    ax2.annotate('R_e 7d = {:.2f}'.format(data[data.name==comuna]['MEAN'][-7:].mean()), (.75,.65), color='C2',xycoords='axes fraction')
    ax2.annotate('R_e inst. = {:.2f}'.format(data[data.name==comuna]['MEAN'][-1]), (.75,.60), color='k',xycoords='axes fraction')

    matplotlib.pyplot.sca(ax2)
    plt.xticks(rotation=45)
    ax2.tick_params(bottom=False, left=True, labelleft=True, labelbottom=True)
    for n, label in enumerate(ax2.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    ax2.set_ylabel('R efectivo')
    ax2.set_ylim([0,3])

    filename = 'Report/Report_{}_RP{}.pdf'.format(report_day.replace('/','_'), r)
    fig.savefig(filename, dpi=1200)
    return filename

def regiones_page(report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last, im1,im2,death_rate1,death_rate2, sochi_date, im_dates):

    sns.set_context("paper", font_scale=.6)
    every_nth = 7
    filenames = []
    ######## Valores construir tabla de cada región
    ######## P1C1 ################################# P1C2 ### P2C1## P2C2
    ######## Arica # Tarapa Antofag Atacama Coquimb Valpo # Liberta Maule # Ñuble # Biobio  Arauca  Ríos ## Lagos # Aisen # Maga
    heights=[.1,	.35,	.45,	.45,	.50,	.84,	.84,	.84,	.84,	.84,	.84,	.30,	.84,	.30,	.30,	.8]
    pos_x = [.175,	.175,	.175,	.58,	.58,	.175,	.58,	.175,	.58,	.175,	.58,	.175,	.58,	.175,	.175,	.40]
    pos_y = [.73,	.55,	.55,	.39,	.10,	.01,	.01,	.01,	.01,	.01,	.01,	.5375,	.01,	.25,	.01,	.01]
    y_text = [.85,	.705,	.505,	.85,	.60,	.85,	.85,	.85,	.85,	.85,	.85,	.85,	.85,	.56,	.315,	.85]
    labels = [True,	True,	True,	True,	True,	True,	True,	True,	True,	True,	True,	True,	True,	True]

    ########### Valores para dibujar flechas
    ########### l_lim, h_lim, x_t, x_p, x_m, dx,  dy    lower limit, high limit pos x tasa, pos x prevalencia,
    arrow_props = [
                [0.865, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Arica
                [0.795, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Tarapacá
                [0.7475, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Antofagasta
                [0.7475, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Atacama
                [0.6075, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Coquimbo
                [0.0715, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Valparaíso
                [0.1875, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Libertador
                [0.2575, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Maule
                [0.4675, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Ñuble
                [0.1875, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Biobio
                [0.2100, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Araucanía
                [0.6775, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Los Ríos
                [0.2575, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Los Lagos
                [0.7270, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Aisén
                [0.6985, .935, .18, .06, .29,.68,.905,.0325, .0215],    #Magallanes
                [0.050, .9, .235, .055, .29,.68 ,.015, .0215],    #Metropolitana
    ]

    ## Encabezados, pies de página y leyendas
    for r, region in enumerate(regiones[:-1]):
        fig = plt.figure(figsize=(11, 8.5))
        ## Logos
        fig.text(0.95,0.06, '©2020, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha='right', fontsize='large')
        ax_logo = fig.add_axes([.85,.875,.1,.1])
        ax_logo.imshow(logofcv)
        ax_logo.axis('off')
        ax_cinv = fig.add_axes([.05,.875,.25,.08])
        ax_sochi = fig.add_axes([.775,.885,.07,.07])
        ax_cinv.imshow(logos)
        ax_sochi.imshow(logo_sochimi)
        ax_cinv.axis('off')
        ax_sochi.axis('off')

        ## Encabezado
        fig.text(.5, .935, 'Región de ' + regiones[r], horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='xx-large')
        if region in subrep.index:
            fig.text(.5, .9, 'Datos últimos 14 días\nPrevalencia región: {} / Tasa región: {}%\nEstimación de infectados sintomáticos detectados: {}'.format('{:.2f}'.format(prevalencia_region.loc[3,region]).replace('.',','), '{:.2f}'.format(region_avg_rate.loc[3,region]*100).replace('.',','), subrep.underreporting_estimate_clean.loc[region]),
                 horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='x-large')
        else:
            fig.text(.5, .9, 'Datos últimos 14 días\nPrevalencia región: {} / Tasa región: {}%\nEstimación de infectados sintomáticos detectados: ND'.format('{:.2f}'.format(prevalencia_region.loc[3,region]).replace('.',','), '{:.2f}'.format(region_avg_rate.loc[3,region]*100).replace('.',',')),
                 horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='x-large')
        ## Leyendas
        fig.text(.187, .825, '1', fontsize='small')
        fig.text(.2335, .825, '2', fontsize='small')
        fig.text(.2775, .825, '3', fontsize='small')
        fig.text(.3405, .825, '4', fontsize='small')
        fig.text(.4225, .825, '5', fontsize='small')
        fig.text(.4825, .825, '6', fontsize='small')
        fig.text(.5275, .825, '7', fontsize='small')
        fig.text(.5875, .825, '7', fontsize='small')
        fig.text(.605, .52, 'Prevalencia \u2264 4', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .51, '4 < Prevalencia < 5', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .5, 'Prevalencia \u2265 5', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

        fig.text(.605, .47, 'Tasa \u2264 25%', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .46, '25% < Tasa < 30%', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .45, 'Tasa \u2265 30%', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

        fig.text(.605, .42, 'R_e \u2264 0,8', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .41, '0,8 < R_e < 1,0', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .4, 'R_e \u2265 1,0', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

        fig.text(.605, .37, 'Movilidad remanente \u2264 30%', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .36, '30% < Movilidad remanente < 40%', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .35, 'Movilidad remanente \u2265 40%', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

        fig.text(0.605,0.06,
             '1 Infectados activos / 10.000 habitantes.\n'+
             '2 Tasa diaria de nuevos infectados (promedio acumulado).\n'+
             '3 R_e últimos 14 días según Cori et al. (2019)\n'
             '4 Datos epidemiológicos\nhttps://github.com/MinCiencia/Datos-COVID19\n'+
             '5 De acuerdo a subreporte según\nhttps://cmmid.github.io/topics/covid19/global_cfr_estimates.html\n'+
             '6 Fallecimientos acumulados COVID19 / 100.000 habitantes\n'+
             '7 Datos movilidad '+im_dates+' vs. 09/03-15/03.\n'+
                 'https://github.com/MinCiencia/Datos-COVID19, producto 33.\n'
             '8 Datos regionales incluyen casos de comuna desconocida\n'+'\n'+
             '- ND no hay suficientes datos para calcular R_e.\n'+
             '- Uso de camas por Servicio de Salud al ' + sochi_date + ' según SOCHIMI.\n'+
             '- Flechas R_e: cambio mayor/menor a 5% vs ultimos 7 días.\n'+
             '- Otras flechas: cambio mayor/menor a 5% vs semana anterior.\n'
             , ha='left',fontsize='x-large')

        ax = fig.add_axes([.125, .01, .475, .84])
        selection = comun_per_region[comun_per_region == region].index

        make_table(display.loc[selection], display_values.loc[selection],
                   reg_display[reg_display.index==region].rename(index={region:'VALOR REGIONAL ⁸'}), reg_display_values[reg_display.index==region], ax, True)
        add_arrows(display_values.loc[selection], muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last, im1,im2,death_rate1,death_rate2, ax, *arrow_props[r])

        ax2 = fig.add_axes([.645, .595, .3, .22])
        comuna = regiones_short[r]
        comuna = region

        ax2.plot(data[data.name==comuna]['MEAN'][1:])
        ax2.fill_between(data[data.name==comuna].index[1:],
                         data[data.name==comuna]['Low_95'][1:], data[data.name==comuna]['High_95'][1:], alpha=.4)

        ax2.hlines(data[data.name==comuna]['MEAN'][-14:].mean(), data[data.name==comuna].iloc[-14].name,data[data.name==comuna].iloc[-1].name, color='C4')
        ax2.hlines(data[data.name==comuna]['MEAN'][-7:].mean(), data[data.name==comuna].iloc[-7].name,data[data.name==comuna].iloc[-1].name, color='C2')
        ax2.hlines(1, data[data.name==comuna].iloc[1].name,data[data.name==comuna].iloc[-1].name, ls='--',color='k')
        ax2.annotate('R_e 14d = {:.2f}'.format(data[data.name==comuna]['MEAN'][-14:].mean()), (.75,.7), color='C4',xycoords='axes fraction')
        ax2.annotate('R_e 7d = {:.2f}'.format(data[data.name==comuna]['MEAN'][-7:].mean()), (.75,.65), color='C2',xycoords='axes fraction')
        ax2.annotate('R_e inst. = {:.2f}'.format(data[data.name==comuna]['MEAN'][-1]), (.75,.60), color='k',xycoords='axes fraction')
        matplotlib.pyplot.sca(ax2)
        plt.xticks(rotation=45)
        ax2.tick_params(bottom=False, left=True, labelleft=True, labelbottom=True)
        for n, label in enumerate(ax2.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
        ax2.set_ylabel('R efectivo')
        ax2.set_ylim([0,3])
        filename = 'Report/Report_{}_RP{}.pdf'.format(report_day.replace('/','_'), r)
        fig.savefig(filename, dpi=1200)
        filenames. append(filename)
    return filenames

def make_table(datos, values, total, total_values, ax, label=True):
    ax.set_axis_off()
    selection = datos.loc[values.sort_values(by=['Prevalencia','Tasa'], ascending=[False,False]).index]
    selection = pd.concat([selection, total], axis=0, join='outer')
    values = values.sort_values(by=['Prevalencia','Tasa'], ascending=[False,False]).values
    values = np.concatenate([values, total_values.values])


    if label:
        table = ax.table(
            cellText=selection.values,
            rowLabels=selection.index,
            colLabels=selection.columns,
            colWidths=[.125,.125,.075,.125,.175,.125,.1,.125],
            cellColours=[[color_prvlnc(c[0]), color_rate(c[1]), color_r0(c[2]),'w', 'w', 'w','w', color_dim(c[7])] for c in values],
            cellLoc='center',
            loc='upper left')
    else:
        table = ax.table(
        cellText=selection.values,
        rowLabels=selection.index,
        colWidths=[.15,.15,.15,.15,.15],
        cellColours=[[color_prvlnc(c[0]), color_rate(c[1]), 'w', color_im(c[3]), color_dim(c[4])] for c in values.sort_values(by=['Prevalencia','Tasa'], ascending=[False,False]).values],
        cellLoc='center',
        loc='upper left')

def add_arrows(datos, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last, im1,im2,death_rate1,death_rate2, ax, l_lim=0, h_lim=.9, x_t=.275, x_p=.075, x_r = 0.282 ,x_d = .6 ,x_m=.975, dx=.015, dy=.03): #faltan inputs
    selection = datos.loc[datos.sort_values(by=['Prevalencia','Tasa'], ascending=[False,False]).index].index
    y_ = np.linspace(h_lim, l_lim,len(selection))
    for y, comuna in enumerate(selection):

        com = popu[popu.index==comuna].county.values[0] #com = popu[popu['county_name']==comuna].county.values[0]
        #1
        if muni_raw1.loc[com] < muni_raw2.loc[com]*.95:
            ax.annotate("", xy=(x_t+.09, y_[y]+dy), xytext=(x_t-dx+.09, y_[y]), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        elif muni_raw1.loc[com] > muni_raw2.loc[com]*.105:
            ax.annotate("", xy=(x_t, y_[y]), xytext=(x_t-dx, y_[y]+dy), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        else:
            ax.annotate("_", xy=(x_t-dx, y_[y]+dy/2),annotation_clip=False, xycoords='axes fraction')
        #2
        if weekly_prev1.loc[comuna] < weekly_prev2.loc[comuna]*.95:
            ax.annotate("", xy=(x_p+.08, y_[y]+dy), xytext=(x_p-dx+.08, y_[y]), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        elif weekly_prev1.loc[comuna] > weekly_prev2.loc[comuna]*.105:
            ax.annotate("", xy=(x_p, y_[y]), xytext=(x_p-dx, y_[y]+dy), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        else:
            ax.annotate("_", xy=(x_p-dx, y_[y]+dy/2),annotation_clip=False, xycoords='axes fraction')
        #3
        if R_arrow_past.loc[comuna] < R_arrow_last.loc[comuna]:
            ax.annotate("", xy=(x_r+.09*0.6, y_[y]+dy), xytext=(x_r-dx*0.5+.09*0.6, y_[y]), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        elif R_arrow_past.loc[comuna] > R_arrow_last.loc[comuna]:
            ax.annotate("", xy=(x_r, y_[y]), xytext=(x_r-dx*0.5, y_[y]+dy), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')

        #4
        if im1.loc[comuna]['remanente'] < im2.loc[comuna]['remanente']*.95:
            ax.annotate("", xy=(x_m+.09, y_[y]+dy), xytext=(x_m-dx+.09, y_[y]), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        elif im1.loc[comuna]['remanente'] > im2.loc[comuna]['remanente']*.105:
            ax.annotate("", xy=(x_m, y_[y]), xytext=(x_m-dx, y_[y]+dy), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        else:
            ax.annotate("_", xy=(x_m-dx, y_[y]+dy/2),annotation_clip=False, xycoords='axes fraction')
        #5
        if death_rate1.loc[comuna] < death_rate2.loc[comuna]*.95:
            ax.annotate("", xy=(x_d+.09, y_[y]+dy), xytext=(x_d-dx+.09, y_[y]), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        elif death_rate1.loc[comuna] > death_rate2.loc[comuna]*.105:
            ax.annotate("", xy=(x_d, y_[y]), xytext=(x_d-dx, y_[y]+dy), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        else:
            ax.annotate("_", xy=(x_d-dx, y_[y]+dy/2),annotation_clip=False, xycoords='axes fraction')

def make_camas(ax, camas, camas2):
    ax.set_axis_off()
    camasi = camas.copy()
    camasi = camasi.fillna(0)
    camasi['Camas Intermedio'] = camasi['Camas Intermedio'].map('{:.0f}'.format)
    camasi['Camas Intensivo'] = camasi['Camas Intensivo'].map('{:.0f}'.format)
    camasi['Número VMI'] = camasi['Número VMI'].map('{:.0f}'.format)
    camasi['Pacientes en Intermedio'] = camasi['Pacientes en Intermedio'].map('{:.0f}'.format)
    camasi['Pacientes en Intensivo'] = camasi['Pacientes en Intensivo'].map('{:.0f}'.format)
    camasi['Pacientes en VMI'] = camasi['Pacientes en VMI'].map('{:.0f}'.format)
    camasi_value = camasi.copy()
    camasi['Uso Intermedias'] = camasi['Uso Intermedias'].map('{:,.2%}'.format)
    camasi['Uso Intensivas'] = camasi['Uso Intensivas'].map('{:,.2%}'.format)
    camasi['Uso VMI'] = camasi['Uso VMI'].map('{:,.2%}'.format)
    camasi = camasi[['Camas Intermedio','Camas Intensivo','Número VMI','Pacientes en Intermedio','Pacientes en Intensivo','Pacientes en VMI','Uso Intermedias','Uso Intensivas','Uso VMI']]
    camasi = camasi.apply(lambda x: x.str.replace('.',','))



    table = ax.table(
        cellText=camasi.values,
        fontsize=2,
        rowLabels=camas.index,
        colLabels=['Camas Intermedio','Camas Intensivo','Número VMI','Pctes. Intermedio','Pctes. Intensivo','Pctes. VMI','Uso Intermedias','Uso Intensivas','Uso VMI'],
        colWidths=[.111,.111,.111,.111,.111,.111,.111,.111,.111],
        cellColours=[['w','w','w','w','w','w',color_camas(c[6]),color_camas(c[7]),color_camas(c[8])] for c in camas[['Camas Intermedio','Camas Intensivo','Número VMI','Pacientes en Intermedio','Pacientes en Intensivo','Pacientes en VMI','Uso Intermedias','Uso Intensivas','Uso VMI']].values],
        cellLoc='center',
        loc='upper left')

    ### arrows
    y_ = np.linspace(.95-0.01-0.005,.25-0.01+0.005,len(camasi.index)) #.95-0.01-0.005,.25-0.01+0.005
    l = len(camasi.index)
    x_inter, x_inten, x_vmi, dx, dy = 0.720,.83 ,.94 ,0.03, .02 #0.720,.83 ,.94 ,0.03, .02
    for y, SS in enumerate(camasi.index):
        if camas2.loc[SS,'Uso Intermedias'] < camasi_value.loc[SS,'Uso Intermedias']:
            ax.annotate("", xy=(x_inter+0.07, y_[y]+dy), xytext=(x_inter-dx+0.07, y_[y]), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        elif camas2.loc[SS,'Uso Intermedias'] > camasi_value.loc[SS,'Uso Intermedias']:
            ax.annotate("", xy=(x_inter, y_[y]), xytext=(x_inter-dx, y_[y]+dy), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        else:
            ax.annotate("_", xy=(x_inter-dx, y_[y]+dy/2),annotation_clip=False, xycoords='axes fraction')

        if camas2.loc[SS,'Uso Intensivas'] < camasi_value.loc[SS,'Uso Intensivas']:
            ax.annotate("", xy=(x_inten+0.07, y_[y]+dy), xytext=(x_inten-dx+0.07, y_[y]), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        elif camas2.loc[SS,'Uso Intensivas'] > camasi_value.loc[SS,'Uso Intensivas']:
            ax.annotate("", xy=(x_inten, y_[y]), xytext=(x_inten-dx, y_[y]+dy), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        else:
            ax.annotate("_", xy=(x_inten-dx, y_[y]+dy/2),annotation_clip=False, xycoords='axes fraction')

        if camas2.loc[SS,'Uso VMI'] < camasi_value.loc[SS,'Uso VMI']:
            ax.annotate("", xy=(x_vmi+0.07, y_[y]+dy), xytext=(x_vmi-dx+0.07, y_[y]), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        elif camas2.loc[SS,'Uso VMI'] > camasi_value.loc[SS,'Uso VMI']:
            ax.annotate("", xy=(x_vmi, y_[y]), xytext=(x_vmi-dx, y_[y]+dy), arrowprops=dict(arrowstyle="->"),annotation_clip=False, xycoords='axes fraction')
        else:
            ax.annotate("_", xy=(x_vmi-dx, y_[y]+dy/2),annotation_clip=False, xycoords='axes fraction')

def hospitales_from_excel(hospitales, hospitales_lastweek):
    #### HOSPITALES ###
    hospitales = hospitales.iloc[:125] # Descartando tabla flotante
    ## Renombramos variables
    dict_camas = {'Número camas disponibles: Intermedio':'Camas Intermedio',
                                            'Número camas disponibles: Intensivo':'Camas Intensivo',
                                            'Número de ventiladores mecánicos invasivos (VMI)':'Número VMI',
                                            'Pacientes en VMI totales':'Pacientes en VMI',
                                            'Pacientes Hospitalizado Intermedio':'Pacientes en Intermedio',
                                            'Pacientes Hospitalizado Intensivo':'Pacientes en Intensivo',
                                            'Servicio de Salud Asignado':'Servicio de Salud'}
    hospitales = hospitales.rename(columns=dict_camas)

    ## Agrupamos por Servicio de Salud
    camas = hospitales.pivot_table(index='Servicio de Salud', values=['Número VMI','Pacientes en VMI','Camas Intensivo','Pacientes en Intensivo','Camas Intermedio','Pacientes en Intermedio'],aggfunc=np.sum)
    camas['Uso VMI'] = camas['Pacientes en VMI'] / camas['Número VMI']
    camas['Uso Intermedias'] = camas['Pacientes en Intermedio'] / camas['Camas Intermedio']
    camas['Camas Intensivo'] = hospitales.pivot_table(index='Servicio de Salud', values=['Camas Intensivo'],aggfunc=np.sum)
    camas['Uso Intensivas'] = camas['Pacientes en Intensivo'] / camas['Camas Intensivo']

    hospitales_lastweek = hospitales_lastweek.iloc[:125] # Descartando tabla flotante
    ## Renombramos variables
    hospitales_lastweek = hospitales_lastweek.rename(columns=dict_camas)

    ## Agrupamos por Servicio de Salud
    camas2 = hospitales_lastweek.pivot_table(index='Servicio de Salud', values=['Número VMI','Pacientes en VMI','Camas Intensivo','Pacientes en Intensivo','Camas Intermedio','Pacientes en Intermedio'],aggfunc=np.sum)
    camas2['Uso VMI'] = camas2['Pacientes en VMI'] / camas2['Número VMI']
    camas2['Uso Intermedias'] = camas2['Pacientes en Intermedio'] / camas2['Camas Intermedio']
    camas2['Camas Intensivo'] = hospitales_lastweek.pivot_table(index='Servicio de Salud', values=['Camas Intensivo'],aggfunc=np.sum)
    camas2['Uso Intensivas'] = camas2['Pacientes en Intensivo'] / camas2['Camas Intensivo']

    ## Corrigiendo nombres
    camas = camas.rename(index={'SSVALPARAISO SAN ANTONIO': 'SS VALPARAISO SAN ANTONIO', 'SS ACONGAGUA':'SS ACONCAGUA'})
    camas2 = camas2.rename(index={'SSVALPARAISO SAN ANTONIO': 'SS VALPARAISO SAN ANTONIO', 'SS ACONGAGUA':'SS ACONCAGUA'})


    camas = camas.reindex(order)
    camas2 = camas2.reindex(order)
    camas.loc['Total Nacional',:] = camas.sum(axis=0)
    camas2.loc['Total Nacional',:] = camas2.sum(axis=0)

    camas.loc['Total Nacional', 'Uso VMI'] = camas['Pacientes en VMI'].sum() / camas['Número VMI'].sum()
    camas.loc['Total Nacional', 'Uso Intermedias'] = camas['Pacientes en Intermedio'].sum() / camas['Camas Intermedio'].sum()
    camas.loc['Total Nacional', 'Uso Intensivas'] = camas['Pacientes en Intensivo'].sum() / camas['Camas Intensivo'].sum()

    camas2.loc['Total Nacional', 'Uso VMI'] = camas2['Pacientes en VMI'].sum() / camas2['Número VMI'].sum()
    camas2.loc['Total Nacional', 'Uso Intermedias'] = camas2['Pacientes en Intermedio'].sum() / camas2['Camas Intermedio'].sum()
    camas2.loc['Total Nacional', 'Uso Intensivas'] = camas2['Pacientes en Intensivo'].sum() / camas2['Camas Intensivo'].sum()

    RM = ['SS METROPOLITANO CENTRAL','SS METROPOLITANO ORIENTE','SS METROPOLITANO SUR','SS METROPOLITANO SUR ORIENTE','SS OCCIDENTE','SS NORTE']
    camas.loc['Total RM',:]= camas.iloc[23:29].sum(axis=0)
    camas.loc['Total RM', 'Uso VMI'] = camas.iloc[23:29]['Pacientes en VMI'].sum() / camas.iloc[23:29]['Número VMI'].sum()
    camas.loc['Total RM', 'Uso Intermedias'] = camas.iloc[23:29]['Pacientes en Intermedio'].sum() / camas.iloc[23:29]['Camas Intermedio'].sum()
    camas.loc['Total RM', 'Uso Intensivas'] = camas.iloc[23:29]['Pacientes en Intensivo'].sum() / camas.iloc[23:29]['Camas Intensivo'].sum()

    camas2.loc['Total RM',:]= camas2.iloc[23:29].sum(axis=0)
    camas2.loc['Total RM', 'Uso VMI'] = camas2.iloc[23:29]['Pacientes en VMI'].sum() / camas2.iloc[23:29]['Número VMI'].sum()
    camas2.loc['Total RM', 'Uso Intermedias'] = camas2.iloc[23:29]['Pacientes en Intermedio'].sum() / camas2.iloc[23:29]['Camas Intermedio'].sum()
    camas2.loc['Total RM', 'Uso Intensivas'] = camas2.iloc[23:29]['Pacientes en Intensivo'].sum() / camas2.iloc[23:29]['Camas Intensivo'].sum()
    camas2 = camas2.fillna(0)
    return camas, camas2

def Nacional_page(result, chile_avg_rate, chile_prvlnc, subrep, activos,report_day):

    sns.set_context("paper", font_scale=.6)
    fig = plt.figure(figsize=(8.5, 11)) #(8.5, 11)


    fig.text(0.1,0.06, 'R_e calculado de acuerdo a Cori et al. (2019) https://doi.org/10.1016/j.epidem.2019.100356\nValor mostrado corresponde a promedio últimos 7 días (línea verde) y 14 días (línea violeta) respectivamente.\nDatos epidemiológicos https://github.com/MinCiencia/Datos-COVID19', ha='left')
    fig.text(0.9,0.06, '©2020, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha='right')
    ax_logo = fig.add_axes([.8,.868,.1*1.2,.1*1.2])
    ax_logo.imshow(logofcv)
    ax_logo.axis('off')
    ax_cinv = fig.add_axes([.05,.89,.25*0.9,.08*0.9])
    ax_sochi = fig.add_axes([.74,.9,.05*1.2,.05*1.2])
    ax_cinv.imshow(logos)
    ax_sochi.imshow(logo_sochimi)
    ax_cinv.axis('off')
    ax_sochi.axis('off')

    probables = subrep.underreporting_estimate_clean.loc['Nacional'].split('%')
    probables_bajo =  int(probables[1][-2:])
    probables_alto =  int(probables[2][-2:])
    activos = int(activos)
    fig.text(.5, .9, 'Trayectoria de R_efectivo nacional a lo largo del tiempo \nPrevalencia País: {} / Tasa país: {}%\nEstimación de infectados sintomáticos detectados: {}\nInfectados activos: {} / Inf. Act. Probables: {} ~ {} '.format('{:.2f}'.format(chile_prvlnc.T.values[-1][0]).replace('.',','), '{:.2f}'.format(chile_avg_rate.values[-1]*100).replace('.',','), subrep.underreporting_estimate_clean.loc['Nacional'], '{:,}'.format(activos).replace(',','.'), '{:,}'.format(int(activos*100/probables_alto)).replace(',','.'),'{:,}'.format(int(activos*100/probables_bajo)).replace(',','.')), horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='x-large')

    result.index = pd.to_datetime(result['Fecha'])

    ax_regions = {}
    ax_coordinates = {}

    ax = fig.add_subplot(2,1,1)

    ax.plot(result.index[1:], result['MEAN'][1:])
    ax.fill_between(result.index[1:],
                 result['Low_95'][1:], result['High_95'][1:], alpha=.4)
    ax.set_title('Nacional')
    ax.hlines(result['MEAN'][-14:].mean(), result.iloc[-14].name,result.iloc[-1].name, color='C4')
    ax.hlines(result['MEAN'][-7:].mean(), result.iloc[-7].name,result.iloc[-1].name, color='C2')
    ax.hlines(1, result.iloc[1].name,result.iloc[-1].name, ls='--',color='k')
    ax.annotate('R_e 14d = {:.2f}'.format(result['MEAN'][-14:].mean()), (.8,.6), color='C4', xycoords='axes fraction')
    ax.annotate('R_e 7d = {:.2f}'.format(result['MEAN'][-7:].mean()), (.8,.56), color='C2', xycoords='axes fraction')
    ax.annotate('R_e inst. = {:.2f}'.format(result['MEAN'].values[-1]), (.8,.52), color='k', xycoords='axes fraction')
    ax.set_ylabel('R efectivo')
    ax.set_ylim([0,3])

    ticks = [result.index[1:][i]  for i in range(len(result.index[1:])) if i%14==0]
    ticks_labels = [result.index[1:][i].strftime("%d/%m")  for i in range(len(result.index[1:])) if i%14==0]
    ax.set_xticks(ticks)
    plt.xticks(rotation=45)
    ax.set_xticklabels(ticks_labels, fontdict = {'fontsize' : '8'})



    fig.subplots_adjust(hspace=.5, top = 0.84)
    filename = 'Report/Report_{}_RP18.pdf'.format(report_day.replace('/','_'))
    fig.savefig(filename, dpi=1200)

    return filename

def generate_table(file):
    date = file[-9:]
    Tabla = pd.read_csv(file, index_col = "county_name")
    Tabla.columns = ['Prevalencia', 'Tasa %', 'R_e', 'Activos', 'Probables',
           'Mortalidad', 'Viajes', 'Movilidad']
    Probables = Tabla['Probables'].copy()
    print(Probables.apply(lambda x: x.split('~')) )

    Tabla.drop('Probables', axis= 'columns', inplace = True)
    #Cambiar caracteres
    Tabla = Tabla.apply(lambda x: x.astype(str).str.replace(',','.'))
    Tabla = Tabla.apply(lambda x: x.astype(str).str.replace('ND','0'))
    Tabla = Tabla.apply(lambda x: x.astype(str).str.replace('%',''))
    print(Tabla)

    # Pasar de string a float
    columns = Tabla.columns
    for column in columns:

        Tabla[column] = pd.to_numeric(Tabla[column])

    #Renombrar columna
    Tabla = Tabla.rename(columns={'Tasa': 'Tasa %'})
    Tabla.to_csv('Tables/Tabla_'+date)

def sex_age_ajusted_death_rates(deaths):
    pass
