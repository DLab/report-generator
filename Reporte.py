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
import datetime as dt
import locale
from math import ceil
import gc
from report_utils import *
from data_loader import *

def reporte():
    corrected_day, report_day = last_data_day()
    #report_day = '05/09'
    day, month = report_day.split('/')
    fecha = dt.date(2019,12,30)
    delta = corrected_day - fecha # Semana epidemiologica


    ############### Lectura de datos ######################
    sochi_dates, camas2, camas = hospitales_from_db()
    sochi_date2, sochi_date = pd.to_datetime(sochi_dates[0]).strftime("%d/%m"),pd.to_datetime(sochi_dates[1]).strftime("%d/%m")

    popu = population_from_db()

    # erre, erre_reg = r_comunas_and_regions()
    erre = r_comunas_db()
    erre_reg = r_regions_db()
    erre_national = r_national_db()
    im1, im2, im_dates = movility_from_db()
    active_comunas = active_cases_from_db()
    muertos_comunas = deaths_comunas_from_db()
    # for custom dates slice here

    subrep = pd.read_csv('under_reporting/output/reportDataFinal_week.csv')
    # slicing of subrep currently not possible



    data_region = active_comunas[active_comunas.Comuna!='Total'].pivot_table(index=['Region','Fecha'], values='Casos activos', aggfunc=sum)

    ## Creando nueva estructura que contendrá los datos de las dos últimas semanas

    datos_comunas = pd.DataFrame(index=[0,1,2,3], columns=active_comunas['Codigo comuna'].unique())
    muerte_comunas = pd.DataFrame(index=[0,1,2,3], columns=muertos_comunas['Codigo comuna'].unique())
    datos_region = pd.DataFrame(index=[0,1,2,3], columns=active_comunas['Region'].unique())
    del datos_comunas[0.0]

    for reg in datos_region.columns:
        datos_region[reg] = data_region.loc[reg]['Casos activos'].iloc[-4:].values
    for com in datos_comunas.columns:
        datos_comunas[com] = active_comunas[active_comunas['Codigo comuna']==com]['Casos activos'].iloc[-4:].values
        muerte_comunas[com] = muertos_comunas[muertos_comunas['Codigo comuna']==com]['Casos fallecidos'].iloc[-4:].values

    ##?
    pop = popu.set_index('Nombre Comuna')#?
    indices = pop.index.values
    indices[-1] = 'Chile'

    ## by region
    pop_reg = pop.pivot_table(index='Nombre Region', values='Poblacion 2020', aggfunc=sum)
    muertos_region = muertos_comunas.pivot_table(index=['Region','Fecha'], values = 'Casos fallecidos', aggfunc=sum)
    ########################## calculo de tasa  de crecimiento ############################

    muni_rate = 1 - datos_comunas.shift(1) / datos_comunas
    muni_rate.loc[0] = 1
    muni_rate = muni_rate.fillna(0)
    muni_avg_rate = muni_rate.expanding().mean()

    region_rate = 1 - datos_region.shift(1) / datos_region
    region_rate.loc[0] = 1
    region_rate = region_rate.fillna(0)
    region_avg_rate = region_rate.expanding().mean()

    chile_rate = 1 - datos_comunas.sum(axis=1).shift(1) / datos_comunas.sum(axis=1)
    chile_rate.loc[0] = 1
    chile_rate = chile_rate
    chile_avg_rate = chile_rate.expanding().mean()

    rate_diff = muni_avg_rate.sub(chile_avg_rate, axis=0)

    ########################## calculo de prevalencia y mortalidad diaria ############################
    prevalencia = pd.DataFrame()
    mortalidad = pd.DataFrame()
    for com in datos_comunas.columns:
        comuna = popu[popu.Comuna==com]['Nombre Comuna'].values[0]
        prevalencia[comuna] = datos_comunas[com]*10000 / pop.loc[comuna, 'Poblacion 2020']
        mortalidad[comuna] = muerte_comunas[com]*100000 / pop.loc[comuna, 'Poblacion 2020']

    prevalencia_region = pd.DataFrame()
    mortalidad_region = pd.DataFrame(index=[0,1,2,3])
    for reg in datos_region.columns:

        prevalencia_region[reg] = datos_region[reg]*10000 / pop_reg.loc[reg,'Poblacion 2020']
        for i in range(4):
            mortalidad_region.loc[i,reg] = muertos_region.loc[reg].iloc[i-4].values*100000 / pop_reg.loc[reg,'Poblacion 2020']

    chile_prvlnc = pd.DataFrame([(datos_comunas.sum(axis=1) *10000 / pop.loc['Chile', 'Poblacion 2020'])])

    prvlnc_diff = prevalencia.sub(chile_prvlnc.T.mean(axis=1), axis=0)
    ########################## calculo tasa, prevalencia y mortalidad semanal ############################
    muni_raw_rate = 1 - datos_comunas.shift(1) / datos_comunas
    muni_raw1, muni_raw2 = muni_raw_rate.iloc[0:2].mean(axis=0), muni_raw_rate.iloc[2:4].mean(axis=0)

    weekly_prev1, weekly_prev2 = prevalencia.iloc[0:2].mean(axis=0), prevalencia.iloc[2:4].mean(axis=0)
    death_rate1, death_rate2 = mortalidad[0:2].diff(axis = 0).iloc[1], mortalidad[2:4].diff(axis = 0).iloc[1]

    erre = erre.replace({'comuna': indices_dict})
    ## Reestructurando R efectivo
    R_p = erre.pivot_table(index=['comuna','Fecha'])

    ## Calculando el R_e promedio de los últimos 14 días ¿?
    R0 = pd.Series(data=np.zeros(len(pop.drop(['Chile']).index)), index=pop.drop(['Chile']).index)

    for comuna in pop.drop(['Chile']).index:
        try:
            if R_p.MEAN.loc[comuna][-1]==0:
                R0.loc[comuna] = 0
            elif len(R_p.MEAN.loc[comuna]) > 13:
                R0.loc[comuna] = R_p.MEAN.loc[comuna].iloc[-14:].mean()

        except:
            print(comuna,'not found')
            R0.loc[comuna] = np.nan

    ## Calculando el R_e promedio regional de los últimos 14 días
    erre_reg = erre_reg.replace({'region':
                        {'Metropolitana':'Metropolitana de Santiago',
                        "Lib. Gral. Bernardo O'Higgins":"Libertador General Bernardo O'Higgins",
                        'Araucanía':'La Araucanía',
                        'Aysén del Gral. C. Ibáñez del Campo':'Aysén del General Carlos Ibáñez del Campo',
                        'Magallanes y Antártica Chilena':'Magallanes y de la Antártica Chilena'}})
    R_p_reg = erre_reg.pivot_table(index=['region','Fecha'])

    # R_p_reg = R_p_reg.rename(index={
    #                     'Metropolitana':'Metropolitana de Santiago',
    #                     "Lib. Gral. Bernardo O'Higgins":"Libertador General Bernardo O'Higgins",
    #                     'Araucanía':'La Araucanía',
    #                     'Aysén del Gral. C. Ibáñez del Campo':'Aysén del General Carlos Ibáñez del Campo',
    #                     'Magallanes y Antártica Chilena':'Magallanes y de la Antártica Chilena'})

    R0_reg = pd.Series(data=np.zeros(16), index=regiones)
    for region in R0_reg.index:
        try:
            if len(R_p_reg.MEAN.loc[region]) > 13:##?
                R0_reg.loc[region] = R_p_reg.MEAN.loc[region].iloc[-14:].mean()
        except:
            print('Reg Exception', region)
            R0_reg.loc[region] = np.nan

    comun_per_region = pop['Nombre Region'].drop(['Chile'])

    #### MOVILIDAD
    im1.loc[im1.index.max() + 1] = ['R11',"O'Higgins", 0, 0]
    im1.loc[im1.index.max() + 1] = ['R12',"Antártica", 0, 0]
    im1 = im1.set_index('comuna')
    im1 = im1.rename(index=indices_dict)
    im2.loc[im2.index.max() + 1] = ['R11',"O'Higgins", 0, 0]
    im2.loc[im2.index.max() + 1] = ['R12',"Antártica", 0, 0]
    im2 = im2.set_index('comuna')
    im2 = im2.rename(index=indices_dict)
    im_reg = im2.pivot_table(index='region', values=['IM','remanente'],aggfunc=np.mean)
    im_reg2 = im_reg.set_index(pop.drop(['Chile'])['Nombre Region'].unique())

    #### Subreporte
    subrep = subrep.set_index('country')
    subrep = subrep.rename(index={'O’Higgins':'Libertador General Bernardo O\'Higgins',
                                 'Metropolitana':'Metropolitana de Santiago'})

    ########################## Creando dataFrame de visualización ############################
    display = pd.DataFrame(index=pop.drop(['Chile']).index)

    display['Prevalencia'] = [prevalencia.T[3].loc[c] for c in display.index]
    display['Tasa'] = [muni_avg_rate.T[3].loc[pop[pop.index==c].Comuna.values[0]] for c in display.index]
    display['R_e'] = R0
    display['Inf. Activos'] = [datos_comunas[int(pop[pop.index==c].Comuna.values[0])].loc[3] for c in display.index]
    for c in display.index:
        if comun_per_region[c] in subrep.index:
            infected = datos_comunas[int(pop[pop.index==c].Comuna.values[0])].loc[3]
            display.loc[c,'Inf. Act. Probables'] = '{:.0f} ~ {:.0f}'.format(infected / subrep.upper[comun_per_region[c]], infected / subrep.lower[comun_per_region[c]])
        else:
            display.loc[c,'Inf. Act. Probables'] = '-'
    display['Mortalidad'] = [mortalidad.T[3].loc[c] for c in display.index]
    display['Viajes'] = [im2['IM'].loc[c] for c in display.index]
    display['Movilidad'] = [(im2['remanente'].loc[c]) / 100 for c in display.index]
    display = display.fillna(0)


    reg_display = pd.DataFrame(index=pop.drop(['Chile'])['Nombre Region'].unique())
    reg_display['Prevalencia'] = [prevalencia_region.loc[3,r] for r in reg_display.index]
    reg_display['Tasa'] = [region_avg_rate.loc[3,r] for r in reg_display.index]
    reg_display['R_e'] = R0_reg
    for r in reg_display.index:
        infected = data_region.loc[r].iloc[-1].values[0]
        reg_display.loc[r,'Inf. Activos'] = infected
        if r in subrep.index:
            reg_display.loc[r,'Inf. Act. Probables'] = '{:.0f} ~ {:.0f}'.format(infected / subrep.upper[r], infected / subrep.lower[r])
        else:
            reg_display.loc[r,'Inf. Act. Probables'] = '-'
    reg_display['Mortalidad'] = [mortalidad_region[r].loc[3] for r in reg_display.index]
    reg_display['Viajes'] = [im_reg2['IM'].loc[r] for r in reg_display.index]
    reg_display['Movilidad'] = [(im_reg2['remanente'].loc[r]) / 100 for r in reg_display.index]


    ## R arrow represent R rate of change
    R_arrow_last = pd.Series(data=np.zeros(len(pop.drop(['Chile']).index)), index=pop.drop(['Chile']).index)
    R_arrow_past = pd.Series(data=np.zeros(len(pop.drop(['Chile']).index)), index=pop.drop(['Chile']).index)
    for comuna in pop.drop(['Chile']).index:
        try:
            if R_p.MEAN.loc[comuna].iloc[-1]!=0 and int(display[display.index == comuna]['Inf. Activos'])!=0:
                R_arrow_last.loc[comuna] = R_p.MEAN.loc[comuna].iloc[-7:].mean()
                R_arrow_past.loc[comuna] = R_p.MEAN.loc[comuna].iloc[-14:].mean()
            else:
                R_arrow_last.loc[comuna] = 0
                R_arrow_past.loc[comuna] = 0
        except:
            R_arrow_last.loc[comuna] = 0
            R_arrow_past.loc[comuna] = 0
    ## Si la prevalencia es 0, entonces la tasa se setea en 0 también
    for i in range(len(display)):
        if display.iloc[i].Prevalencia == 0.0:
            display.iloc[i,display.columns.get_loc('Tasa')] = 0.0

    for i in range(len(reg_display)):
        if reg_display.iloc[i].Prevalencia == 0.0:
            reg_display.iloc[i,reg_display.columns.get_loc('Tasa')] = 0.0

    for i in range(len(display.R_e)):
        if display.values[i,3] == 0.0:
            display['R_e'][i] = 0

    ## Duplicando los datos, una versión contendrá los datos formateados para visualización como strings, la otra guarda los valores
    display_values = display.copy()
    reg_display_values = reg_display.copy()
    ########################## Formateando tabla para visualización ############################
    display['Prevalencia'] = display['Prevalencia'].map('{:,.2f}'.format)
    display['Tasa'] = display['Tasa'].map('{:,.2%}'.format)    # filenames.append(Nacional_page(pd.read_csv('time_series/R_Efectivo_nacional_'+report_day.replace('/','_')+'.csv'), chile_avg_rate, chile_prvlnc, subrep, activos, report_day))

    display['R_e'] = display['R_e'].map('{:,.2f}'.format)
    display['Inf. Activos'] = display['Inf. Activos'].map('{:,.0f}'.format)
    display['Mortalidad'] = display['Mortalidad'].map('{:,.2f}'.format)
    display['Viajes'] = display['Viajes'].map('{:,.2f}'.format)
    display['Movilidad'] = display['Movilidad'].map('{:,.2%}'.format)

    reg_display['Prevalencia'] = reg_display['Prevalencia'].map('{:,.2f}'.format)
    reg_display['Tasa'] = reg_display['Tasa'].map('{:,.2%}'.format)
    reg_display['R_e'] = reg_display['R_e'].map('{:,.2f}'.format)
    reg_display['Inf. Activos'] = reg_display['Inf. Activos'].map('{:,.0f}'.format)
    reg_display['Mortalidad'] = reg_display['Mortalidad'].map('{:,.2f}'.format)
    reg_display['Viajes'] = reg_display['Viajes'].map('{:,.2f}'.format)
    reg_display['Movilidad'] = reg_display['Movilidad'].map('{:,.2%}'.format)

    ## Cambiamos el indicador de decimal de puntos a comas
    display = display.apply(lambda x: x.str.replace('.',','))
    reg_display = reg_display.apply(lambda x: x.str.replace('.',','))

    ## Reemplazamos los R_e de 0 por "no definido"
    for i in range(len(display)):
        if display.iloc[i][3] == '0':
            display.iloc[i].R_e = '0,00'
        if display.iloc[i].R_e == '0,00':
            display.iloc[i,display.columns.get_loc('R_e')] = 'ND'

    for i in range(len(reg_display)):
        if reg_display.iloc[i].R_e == '0,00':
            reg_display.iloc[i,reg_display.columns.get_loc('R_e')] = 'ND'
    ## guardamos la tabla
    display.to_csv('Report/display_{}.csv'.format(report_day.replace('/','_')))
    # funcion display
    ####################################################################################################
    data = erre_reg #?
    data = data.set_index('Fecha')
    data.index = pd.to_datetime(data.index)
    data.index = [x.strftime("%d/%m/%y") for x in data.index]
    data = data.rename(columns={'Mean(R)': 'MEAN','Quantile.0.025(R)': 'Low_95','Quantile.0.975(R)': 'High_95'})
    ####################################################################################################
    ##### REPORT PAGES ###
    filenames = []
    #########  COVER
    filenames.append(cover(report_day, delta))
    ######### Regiones
    filenames += regiones_page(report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last, im1,im2,death_rate1,death_rate2, sochi_date)
    ######### Metropolitana Page
    filenames.append(metropolitana_page(report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last, im1,im2,death_rate1,death_rate2, sochi_date))
    #### Otras Provincias ###
    filenames.append(otras_provincias_page(report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last, im1,im2,death_rate1,death_rate2, sochi_date))
    ### Hospitales
    filenames.append(hospitales_page(report_day, camas, camas2, chile_avg_rate, chile_prvlnc, sochi_dates))
    ### Nacional
    activos = np.sum(reg_display_values['Inf. Activos'])
    filenames.append(Nacional_page(erre_national, chile_avg_rate, chile_prvlnc, subrep, activos, report_day))

    ######### Merging
    from PyPDF2 import PdfFileMerger
    day, month = report_day.split('/')
    folder = 'pages/'
    merger = PdfFileMerger()
    #print(filenames)
    for pdf in filenames:
        merger.append(pdf)
    name = 'Reporte'

    with open(name+'_'+day+'_'+month+".pdf", "wb") as fout:
        merger.write(fout)
        merger.close()


if __name__ == '__main__':
    reporte()
