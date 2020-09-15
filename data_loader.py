# -*- coding: utf-8 -*-
"""
dlab
Computational Biology Lab
Fundación Ciencia y Vida
"""
import pandas as pd
import numpy as np
import datetime as dtime
import gc
import requests
import json
from report_utils import __iso_handler, last_data_day

data_day, report_day = last_data_day()

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

def hospitales_from_db():
    endpoint_HEALTH_SERVICE = requests.get('http://192.168.2.223:5006/getDetailedBedsAndVentilationByHealthService' )
    HEALTH_SERVICE = json.loads(endpoint_HEALTH_SERVICE.text)
    HEALTH_SERVICE = pd.DataFrame(HEALTH_SERVICE['data'])

    HEALTH_SERVICE.columns = HEALTH_SERVICE.loc['name']
    HEALTH_SERVICE = HEALTH_SERVICE.transpose()
    HEALTH_SERVICE.drop('name', axis =1, inplace = True)
    HEALTH_SERVICE.drop('vmi_covid19_sospechosos', axis =1, inplace = True)
    HEALTH_SERVICE.drop('vmi_covid19_confirmados', axis =1, inplace = True)

    HEALTH_SERVICE_newest = pd.DataFrame(index =HEALTH_SERVICE.index , columns = HEALTH_SERVICE.columns)
    HEALTH_SERVICE_prev = pd.DataFrame(index =HEALTH_SERVICE.index , columns = HEALTH_SERVICE.columns)

    for i in HEALTH_SERVICE.columns:
        for j in HEALTH_SERVICE.index:
            HEALTH_SERVICE_newest.loc[j,i] = HEALTH_SERVICE.loc[j,i][-1]
            HEALTH_SERVICE_prev.loc[j,i] = HEALTH_SERVICE.loc[j,i][-8]




    HEALTH_SERVICE_newest['dates'] = pd.DataFrame(HEALTH_SERVICE_newest['dates']).apply(__iso_handler, axis=1)
    HEALTH_SERVICE_prev['dates'] = pd.DataFrame(HEALTH_SERVICE_prev['dates']).apply(__iso_handler, axis=1)

    columns_dict = {'camas_ocupadas_intensivo': 'Pacientes en Intensivo', 'camas_ocupadas_intermedio':'Pacientes en Intermedio',
           'camas_totales_intensivo': 'Camas Intensivo', 'camas_totales_intermedio': 'Camas Intermedio',
           'vmi_ocupados':'Pacientes en VMI','vmi_totales':'Número VMI'}

    HEALTH_SERVICE_newest = HEALTH_SERVICE_newest.rename(columns = columns_dict)#, inplace = True)
    HEALTH_SERVICE_prev = HEALTH_SERVICE_prev.rename(columns = columns_dict)#, inplace = True)

    days = [HEALTH_SERVICE_prev['dates'][0], HEALTH_SERVICE_newest['dates'][0]]

    HEALTH_SERVICE_prev.drop('dates', axis = 1, inplace = True)
    HEALTH_SERVICE_newest.drop('dates', axis = 1, inplace = True)


    for hs in HEALTH_SERVICE_prev.index:
        if HEALTH_SERVICE_newest.loc[hs, 'Pacientes en VMI'] != 0 and HEALTH_SERVICE_newest.loc[hs,'Número VMI'] != 0:
            HEALTH_SERVICE_newest.loc[hs, 'Uso VMI'] = HEALTH_SERVICE_newest.loc[hs,'Pacientes en VMI']/HEALTH_SERVICE_newest.loc[hs, 'Número VMI']
        else:
            HEALTH_SERVICE_newest.loc[hs, 'Uso VMI'] = 0

        if HEALTH_SERVICE_newest.loc[hs, 'Camas Intermedio'] != 0 and HEALTH_SERVICE_newest.loc[hs,'Pacientes en Intermedio'] != 0:
            HEALTH_SERVICE_newest.loc[hs, 'Uso Intermedias'] = HEALTH_SERVICE_newest.loc[hs,'Pacientes en Intermedio']/HEALTH_SERVICE_newest.loc[hs, 'Camas Intermedio']
        else:
            HEALTH_SERVICE_newest.loc[hs, 'Uso Intermedias'] = 0

        if HEALTH_SERVICE_newest.loc[hs, 'Camas Intensivo'] != 0 and HEALTH_SERVICE_newest.loc[hs,'Pacientes en Intensivo'] != 0:
            HEALTH_SERVICE_newest.loc[hs, 'Uso Intensivas'] = HEALTH_SERVICE_newest.loc[hs,'Pacientes en Intensivo']/HEALTH_SERVICE_newest.loc[hs, 'Camas Intensivo']
        else:
            HEALTH_SERVICE_newest.loc[hs, 'Uso Intensivas'] = 0

        ##
        if HEALTH_SERVICE_prev.loc[hs, 'Pacientes en VMI'] != 0 and HEALTH_SERVICE_prev.loc[hs,'Número VMI'] != 0:
            HEALTH_SERVICE_prev.loc[hs, 'Uso VMI'] = HEALTH_SERVICE_prev.loc[hs,'Pacientes en VMI']/HEALTH_SERVICE_prev.loc[hs, 'Número VMI']
        else:
            HEALTH_SERVICE_prev.loc[hs, 'Uso VMI'] = 0

        if HEALTH_SERVICE_prev.loc[hs, 'Camas Intermedio'] != 0 and HEALTH_SERVICE_prev.loc[hs,'Pacientes en Intermedio'] != 0:
            HEALTH_SERVICE_prev.loc[hs, 'Uso Intermedias'] = HEALTH_SERVICE_prev.loc[hs,'Pacientes en Intermedio']/HEALTH_SERVICE_prev.loc[hs, 'Camas Intermedio']
        else:
            HEALTH_SERVICE_prev.loc[hs, 'Uso Intermedias'] = 0

        if HEALTH_SERVICE_prev.loc[hs, 'Camas Intensivo'] != 0 and HEALTH_SERVICE_prev.loc[hs,'Pacientes en Intensivo'] != 0:
            HEALTH_SERVICE_prev.loc[hs, 'Uso Intensivas'] = HEALTH_SERVICE_prev.loc[hs,'Pacientes en Intensivo']/HEALTH_SERVICE_prev.loc[hs, 'Camas Intensivo']
        else:
            HEALTH_SERVICE_prev.loc[hs, 'Uso Intensivas'] = 0

    ###National and RM
    HEALTH_SERVICE_newest.loc['Total Nacional',:] = HEALTH_SERVICE_newest.sum(axis=0)
    HEALTH_SERVICE_prev.loc['Total Nacional',:] = HEALTH_SERVICE_prev.sum(axis=0)
    RM = ['SS METROPOLITANO CENTRAL','SS METROPOLITANO ORIENTE','SS METROPOLITANO SUR','SS METROPOLITANO SUR ORIENTE','SS METROPOLITANO OCCIDENTE','SS METROPOLITANO NORTE']
    HEALTH_SERVICE_newest.loc['Total Nacional', 'Uso VMI'] = HEALTH_SERVICE_newest['Pacientes en VMI'].sum() / HEALTH_SERVICE_newest['Número VMI'].sum()
    HEALTH_SERVICE_newest.loc['Total Nacional', 'Uso Intermedias'] = HEALTH_SERVICE_newest['Pacientes en Intermedio'].sum() / HEALTH_SERVICE_newest['Camas Intermedio'].sum()
    HEALTH_SERVICE_newest.loc['Total Nacional', 'Uso Intensivas'] = HEALTH_SERVICE_newest['Pacientes en Intensivo'].sum() / HEALTH_SERVICE_newest['Camas Intensivo'].sum()
    #
    HEALTH_SERVICE_prev.loc['Total Nacional', 'Uso VMI'] = HEALTH_SERVICE_prev['Pacientes en VMI'].sum() / HEALTH_SERVICE_prev['Número VMI'].sum()
    HEALTH_SERVICE_prev.loc['Total Nacional', 'Uso Intermedias'] = HEALTH_SERVICE_prev['Pacientes en Intermedio'].sum() / HEALTH_SERVICE_prev['Camas Intermedio'].sum()
    HEALTH_SERVICE_prev.loc['Total Nacional', 'Uso Intensivas'] = HEALTH_SERVICE_prev['Pacientes en Intensivo'].sum() / HEALTH_SERVICE_prev['Camas Intensivo'].sum()
    #


    idx = pd.IndexSlice
    HEALTH_SERVICE_newest.loc['Total RM',:] = HEALTH_SERVICE_newest.loc[idx[RM],:].sum(axis=0)
    HEALTH_SERVICE_prev.loc['Total RM',:] = HEALTH_SERVICE_prev.loc[idx[RM],:].sum(axis=0)

    HEALTH_SERVICE_newest.loc['Total RM', 'Uso VMI'] = HEALTH_SERVICE_newest.loc[idx[RM],'Pacientes en VMI'].sum() / HEALTH_SERVICE_newest.loc[idx[RM],'Número VMI'].sum()
    HEALTH_SERVICE_newest.loc['Total RM', 'Uso Intermedias'] = HEALTH_SERVICE_newest.loc[idx[RM],'Pacientes en Intermedio'].sum() / HEALTH_SERVICE_newest.loc[idx[RM],'Camas Intermedio'].sum()
    HEALTH_SERVICE_newest.loc['Total RM', 'Uso Intensivas'] = HEALTH_SERVICE_newest.loc[idx[RM],'Pacientes en Intensivo'].sum() / HEALTH_SERVICE_newest.loc[idx[RM],'Camas Intensivo'].sum()

    HEALTH_SERVICE_prev.loc['Total RM', 'Uso VMI'] = HEALTH_SERVICE_prev.loc[idx[RM],'Pacientes en VMI'].sum() / HEALTH_SERVICE_prev.loc[idx[RM],'Número VMI'].sum()
    HEALTH_SERVICE_prev.loc['Total RM', 'Uso Intermedias'] = HEALTH_SERVICE_prev.loc[idx[RM],'Pacientes en Intermedio'].sum() / HEALTH_SERVICE_prev.loc[idx[RM],'Camas Intermedio'].sum()
    HEALTH_SERVICE_prev.loc['Total RM', 'Uso Intensivas'] = HEALTH_SERVICE_prev.loc[idx[RM],'Pacientes en Intensivo'].sum() / HEALTH_SERVICE_prev.loc[idx[RM],'Camas Intensivo'].sum()

    report_order = ['SS ARICA', 'SS IQUIQUE', 'SS ANTOFAGASTA','SS ATACAMA', 'SS COQUIMBO', 'SS ACONGAGUA', 'SS VIÑA DEL MAR QUILLOTA', 'SS VALPARAISO SAN ANTONIO',
                        'SS LIBERTADOR B. O\'HIGGINS', 'SS DEL MAULE', 'SS ÑUBLE', 'SS BÍO BÍO', 'SS CONCEPCIÓN', 'SS TALCAHUANO', 'SS ARAUCO', 'SS ARAUCANÍA NORTE',
                        'SS ARAUCANÍA SUR', 'SS VALDIVIA', 'SS OSORNO','SS DEL RELONCAVÍ', 'SS CHILOÉ', 'SS AISÉN', 'SS MAGALLANES', 'SS METROPOLITANO NORTE', 'SS METROPOLITANO OCCIDENTE',
                        'SS METROPOLITANO CENTRAL', 'SS METROPOLITANO ORIENTE', 'SS METROPOLITANO SUR', 'SS METROPOLITANO SUR ORIENTE', 'Total Nacional', 'Total RM']
    # s = s.reindex(index = ['B','A','C'])
    HEALTH_SERVICE_prev = HEALTH_SERVICE_prev.reindex(report_order)
    HEALTH_SERVICE_newest = HEALTH_SERVICE_newest.reindex(report_order)
    HEALTH_SERVICE_prev = HEALTH_SERVICE_prev.rename(columns = {'SS ACONGAGUA': 'SS ACONCAGUA'})
    HEALTH_SERVICE_newest = HEALTH_SERVICE_newest.rename(columns = {'SS ACONGAGUA': 'SS ACONCAGUA'})
    global sochi_date, sochi_date2
    sochi_date2, sochi_date = pd.to_datetime(days[0]).strftime("%d/%m"),pd.to_datetime(days[1]).strftime("%d/%m")
    return days, HEALTH_SERVICE_prev, HEALTH_SERVICE_newest

def population_from_db():
    # not yet
    pop = pd.read_excel("sochimi/poblacion2020_nacional.xlsx",  index_col = 0)
    return pop

def r_comunas_and_regions():
    erre = pd.read_csv('time_series/R_Efectivo_comunas_'+report_day.replace('/','_')+'.csv')
    erre = erre.rename(columns={'Mean(R)': 'MEAN','Quantile.0.025(R)': 'Low_95','Quantile.0.975(R)': 'High_95'})
    erre_reg = pd.read_csv('time_series/R_Efectivo_regiones_'+report_day.replace('/','_')+'.csv')
    erre_reg = erre_reg.rename(columns={'Mean(R)': 'MEAN','Quantile.0.025(R)': 'Low_95','Quantile.0.975(R)': 'High_95'})
    return erre, erre_reg

def r_regions_db():
    endpoint_R_region = requests.get('http://192.168.2.223:5006/getEffectiveReproductionAllStates' )
    R_region = json.loads(endpoint_R_region.text)
    R_region_data = pd.DataFrame(R_region['data']).T
    dates = pd.DataFrame(R_region['dates'])
    R_region_data['region']=R_region_data.index
    R_region_data = R_region_data.set_index('region').apply(lambda x: x.apply(pd.Series).stack()).reset_index().drop('level_1', 1)
    for i in range(4):
        dates = pd.concat((dates, dates))
    dates = pd.DataFrame(dates).apply(__iso_handler, axis = 1)
    R_region_data['Fecha'] = dates.values
    R_region_data = R_region_data.replace({'region': region_dict()})
    R_region_data = R_region_data.rename(columns={'mean': 'MEAN','quantile0025': 'Low_95','quantile0975': 'High_95'})

    return R_region_data

def region_dict():
    r_df =pd.read_json('http://192.168.2.223:5006/getStates')
    r_df.index = r_df['id'].astype(str).apply(lambda x:x.zfill(2))
    r_dict = r_df['description'].to_dict()
    return r_dict

def r_comunas_db():
    endpoint_R_comuna = requests.get('http://192.168.2.223:5006/getEffectiveReproductionAllComunas' )
    R_comuna = json.loads(endpoint_R_comuna.text)
    R_comuna_data = pd.DataFrame(R_comuna['data']).T
    dates = pd.DataFrame(R_comuna['dates'])
    R_comuna_data['comuna']=R_comuna_data.index
    R_comuna_data = R_comuna_data.set_index('comuna').apply(lambda x: x.apply(pd.Series).stack()).reset_index().drop('level_1', 1)
    c_df =pd.read_json('http://192.168.2.223:5006/getComunas')
    c_df.index = c_df['cut'].astype(str).apply(lambda x:x.zfill(5))
    comunas_dict = c_df['description'].to_dict()
    comunas_region_dict =c_df['idState'].astype(str).apply(lambda x:x.zfill(2)).to_dict()
    R_comuna_data['region'] = R_comuna_data['comuna']
    R_comuna_data = R_comuna_data.replace({'region':comunas_region_dict})
    R_comuna_data = R_comuna_data.replace({'region': region_dict(), 'comuna': comunas_dict})
    n_comunas = int(R_comuna_data.shape[0]/dates.shape[0])
    dates_f = dates.copy()
    for n in range(n_comunas-1):
        dates_f = pd.concat((dates_f, dates))
    dates_f = pd.DataFrame(dates_f).apply(__iso_handler, axis = 1)
    R_comuna_data['Fecha'] = dates_f.values
    R_comuna_data = R_comuna_data.rename(columns={'mean': 'MEAN','quantile0025': 'Low_95','quantile0975': 'High_95'})
    return R_comuna_data

def r_national_db():
    endpoint_R_national = requests.get('http://192.168.2.223:5006/getNationalEffectiveReproduction' )
    R_national = pd.DataFrame(json.loads(endpoint_R_national.text))
    R_national['Fecha'] = pd.DataFrame(R_national['dates']).apply(__iso_handler, axis = 1)
    R_national = R_national.rename(columns={'mean': 'MEAN','quantile0025': 'Low_95','quantile0975': 'High_95'})
    return R_national

def movility_from_db():
    # not yet

    im = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto33/IndiceDeMovilidad-IM.csv')
    im1 = pd.DataFrame()
    im2 = pd.DataFrame()
    marzo = pd.DataFrame()
    im1['region'] = ['R'+f'{region:02}' for region in im['Codigo region']]
    im2['region'] = ['R'+f'{region:02}' for region in im['Codigo region']]
    im1['comuna'] = [comuna for comuna in im['Comuna']]
    im2['comuna'] = [comuna for comuna in im['Comuna']]
    marzo['IM'] = [np.mean(im[im['Comuna']==comuna].loc[im[im['Comuna']==comuna].index[0],'2020-03-09':'2020-03-15']) for comuna in im['Comuna']]
    im1['IM'] = [np.mean(im[im['Comuna']==comuna].loc[im[im['Comuna']==comuna].index[0],'2020-08-17':'2020-08-23']) for comuna in im['Comuna']]
    im2['IM'] = [np.mean(im[im['Comuna']==comuna].loc[im[im['Comuna']==comuna].index[0],'2020-08-24':'2020-08-30']) for comuna in im['Comuna']]
    im1['remanente'] = [100*im1.loc[i, 'IM']/marzo.loc[i, 'IM'] for i in range(len(im['Comuna']))]
    im2['remanente'] = [100*im2.loc[i, 'IM']/marzo.loc[i, 'IM'] for i in range(len(im['Comuna']))]
    im1.index += 1
    im2.index += 1
    im_dates = '24/08-30/08'
    return im1, im2, im_dates

def active_cases_from_db():
    # not yet
    endpoint = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna_std.csv'
    data_comunas = pd.read_csv(endpoint)
    data_comunas = data_comunas.fillna(0)
    data_comunas['Region'] = data_comunas['Region'].replace( region_names_dict)
    return data_comunas

def deaths_comunas_from_db():
    endpoint2 = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto38/CasosFallecidosPorComuna_std.csv'
    muertos_comunas = pd.read_csv(endpoint2)
    muertos_comunas = muertos_comunas.fillna(0)
    muertos_comunas['Region'] = muertos_comunas['Region'].replace( region_names_dict)
    return muertos_comunas
