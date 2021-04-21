import pandas as pd
import numpy as np
import datetime as dtime
import gc
import requests
import json

### Dictionaries and region names in different formats
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

###

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

def report_date():
    endpoint_R = requests.get('http://192.168.2.223:5006/getNationalEffectiveReproduction' )
    R = json.loads(endpoint_R.text)
    year, month, day = str(R['dates'][-1].split('T')[0]).split('-')
    date = dtime.datetime(int(year),int(month),int(day))
    date += dtime.timedelta(days=1)

    report_day = date.strftime("%d/%m")
    return date.date() , report_day

def color_dim(data):#23, 41, 58
    if data <= .3: color = '#00cc66'
    elif data < .4: color = '#ffcc00'
    else: color = '#ff0000'
    return color

def color_rate_summary(data):
    if data <= .25: color = '#00cc66'
    elif (data < .30): color = '#FFF333'
    else: color = '#DE2F2A'
    return color

def color_r0_summary(data):
    if data == 0.0: color = 'w'
    elif data <= .8: color = '#00cc66'
    elif data < 1.00: color = '#FFF333'
    else: color = '#DE2F2A'
    return color

def color_prvlnc_summary(data):
    if data <= 4.: color = '#00cc66'
    elif data < 5.: color = '#FFF333'
    else: color = '#DE2F2A'
    return color

def color_underreporting_summary(data):
    if data =='N':
        color = '#00cc66'
    elif float(data) == 0:
        color = '#00cc66'
    elif float(data) < 10:
        color = '#FFF333'
    else:
        color = '#DE2F2A'
    return color

def color_camas(data):#23, 41, 58
    if data <= .25: color = '#00cc66'
    elif data < .75: color = '#FFF333'
    elif data < .85: color = '#E3B500'
    else: color = '#DE2F2A'
    return color

def color_hos_sit(data_uti, data_uci, data_vmi):#23, 41, 58
    v = len([1 for data in [data_uti, data_uci, data_vmi] if data <= .25 ])
    a = len([1 for data in [data_uti, data_uci, data_vmi] if data <  .75 ])
    r = len([1 for data in [data_uti, data_uci, data_vmi] if data >= .75 ])

    if r>=2:
        color = '#DE2F2A'
    elif a == 2 and r == 1:
        color = '#E3B500'
    elif a == 2 and v == 1:
        color = '#FFF333'
    elif a == 3 :
        color = '#FFF333'
    elif v == 2 :
        color = '#27AE60'
    elif v == 3:
        color = '#00cc66'
    return color

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

def underreporting_by_region():
	endpoint = 'http://192.168.2.223:5006/getNewCasesUnderreportByState'
	req_end = requests.get(endpoint)
	data_ = json.loads(req_end.text)
	data = data_['data']
	return data

def underreporting_national():
        endpoint = 'http://192.168.2.223:5006/getNationalNewCasesUnderreport'
        req_end = requests.get(endpoint)
        data = json.loads(req_end.text)
        #data = data_['data']
        return data

def asp_national():
    endpoint = 'http://192.168.2.223:5006/getActiveCasesAllComunas'
    req_end = requests.get(endpoint)
    data_ = json.loads(req_end.text)
    #data = data_['data']
    endpoint2 = 'http://192.168.2.223:5006/getNationalNewCasesUnderreport'
    req_end2 = requests.get(endpoint2)
    data_2 = json.loads(req_end2.text)

    active_nat =np.sum(pd.DataFrame(data_['data']), axis = 1)
    under_nat = pd.DataFrame(data_2, index = data_2['date']).drop(columns = 'date')

    active_date_dt = pd.to_datetime(data_['dates'])
    under_date_dt = pd.to_datetime(data_2['date'])

    active_date_human = active_date_dt.strftime('%y-%m-%d')
    under_date_human = under_date_dt.strftime('%y-%m-%d')

    active_nat.index = active_date_human
    under_nat.index = under_date_human

    index = [i for i in active_date_human if i in under_date_human]
    asp_data_mean = [active_nat[ind]/(1-under_nat['mean'][ind]) for ind in index]
    asp_data_low = [active_nat[ind]/(1-under_nat['high'][ind]) for ind in index]
    asp_data_high = [active_nat[ind]/(1-under_nat['low'][ind]) for ind in index]
    return asp_data_mean, asp_data_low, asp_data_high,index

def asp_state(state):
    '''
    State must be a zero padded string
    '''
    endpoint = 'http://192.168.2.223:5006/getActiveCasesAllComunasByState?state='+state
    req_end = requests.get(endpoint)
    data_ = json.loads(req_end.text)
    data_2 = underreporting_by_region()[state]

    active_nat =np.sum(pd.DataFrame(data_['data']), axis = 1)
    under_nat = pd.DataFrame(data_2, index = data_2['date']).drop(columns = 'date')
    active_date_dt = pd.to_datetime(data_['dates'])
    under_date_dt = pd.to_datetime(data_2['date'])

    active_date_human = active_date_dt.strftime('%d/%m/%y')
    under_date_human = under_date_dt.strftime('%d/%m/%y')

    active_nat.index = active_date_human
    under_nat.index = under_date_human

    index = [i for i in active_date_human if i in under_date_human]

    asp_data_mean = [active_nat[ind]/(1- under_nat['mean'][ind]) for ind in index]
    asp_data_low = [active_nat[ind]/(1- under_nat['high'][ind]) for ind in index]
    asp_data_high = [active_nat[ind]/(1- under_nat['low'][ind]) for ind in index]

    return asp_data_mean, asp_data_low, asp_data_high, index

def __iso_handler(x): #overk
    for i, item in enumerate(x.values):
        s = item.split('T')
    return s[0]

def color_epi(data14, data7,data1):
    if data14 <= .8:
        if data7 <= .8:
            color = '#00cc66'
        elif data7 >.8:
            color = '#27AE60'


    elif data14 < 1.00:
        if data7 <= .8:
            color = '#FFF333'
        elif data7 < 1.00 and data1<1:
            color = '#FFF333'
        elif data7 < 1.00 and data1>=1 :
            color = '#E3B500'
        elif data7>=1:
            color = '#E3B500'

    else:
        if data7 <= data14:
            color = '#DE2F2A'
        elif  data7 > data14:
            color = '#A71B08'

    return color

def load_uci_data(slicing_date=None):
    url = 'http://192.168.2.223:5006/getRegionalIcuBedOccupation'
    endpoint = requests.get(url)
    data = json.loads(endpoint.text)
    regional_data = pd.DataFrame(data['data'])
    regional_data_newest = pd.DataFrame(index = regional_data.index, columns = regional_data.columns)
    regional_data_prev = pd.DataFrame(index = regional_data.index, columns = regional_data.columns)
    indices = [-1, -8]
    if slicing_date is not None:
        regional_dates = data['dates']
        formated = [s.split('T')[0] for s in regional_dates]
        indices = [formated.index(slicing_date), formated.index(slicing_date)-7]

    for i in range(1,17):
        for index_name in regional_data.index:
            regional_data_newest['{:02d}'.format(i)][index_name] = regional_data['{:02d}'.format(i)][index_name][indices[0]]
            regional_data_prev['{:02d}'.format(i)][index_name] = regional_data['{:02d}'.format(i)][index_name][indices[0]]
    order = ['15','01', '02', '03', '04', '05', '06', '07', '08', '16', '09', '14', '10', '11', '12', '13']
    regional_data_prev = regional_data_prev.T
    regional_data_newest = regional_data_newest.T
    regional_data_prev = regional_data_prev.reindex(order)
    regional_data_newest = regional_data_newest.reindex(order)
    return regional_data_prev, regional_data_newest

def r_regions_db(slicing_date = None):
    endpoint_R_region = requests.get('http://192.168.2.223:5006/getEffectiveReproductionAllStates' )
    R_region = json.loads(endpoint_R_region.text)
    R_region_data = pd.DataFrame(R_region['data']).T
    dates = pd.DataFrame(R_region['dates'])
    R_region_data['name']=R_region_data.index
    R_region_data = R_region_data.set_index('name').apply(lambda x: x.apply(pd.Series).stack()).reset_index().drop('level_1', 1)
    for i in range(4):
        dates = pd.concat((dates, dates))
    dates = pd.DataFrame(dates).apply(__iso_handler, axis = 1)
    R_region_data['Fecha'] = dates.values
    R_region_data = R_region_data.replace({'name': region_dict()})
    R_region_data = R_region_data.rename(columns={'mean': 'MEAN','quantile0025': 'Low_95','quantile0975': 'High_95'})

    if slicing_date is not None:
        indices = []
        start_slice_index = R_region_data.index[R_region_data['Fecha'] == "2020-04-07"].tolist()
        end_slice_index = R_region_data.index[R_region_data['Fecha'] == slicing_date].tolist()
        for i in range(len(start_slice_index)):
            inter =  range(start_slice_index[i], end_slice_index[i])
            indices += inter
        R_region_data = R_region_data.iloc[indices]
    return R_region_data

def region_dict():
    r_df =pd.read_json('http://192.168.2.223:5006/getStates')
    r_df.index = r_df['id'].astype(str).apply(lambda x:x.zfill(2))
    r_dict = r_df['name'].to_dict()
    return r_dict

def r_comunas_db(slicing_date = None):
    endpoint_R_comuna = requests.get('http://192.168.2.223:5006/getEffectiveReproductionAllComunas' )
    R_comuna = json.loads(endpoint_R_comuna.text)
    R_comuna_data = pd.DataFrame(R_comuna['data']).T
    dates = pd.DataFrame(R_comuna['dates'])
    R_comuna_data['comuna']=R_comuna_data.index
    R_comuna_data = R_comuna_data.set_index('comuna').apply(lambda x: x.apply(pd.Series).stack()).reset_index().drop('level_1', 1)
    c_df =pd.read_json('http://192.168.2.223:5006/getComunas')
    c_df.index = c_df['county'].astype(str).apply(lambda x:x.zfill(5))
    comunas_dict = c_df['county_name'].to_dict()
    comunas_region_dict =c_df['state'].astype(str).apply(lambda x:x.zfill(2)).to_dict()
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

    if slicing_date is not None:
        indices = []
        start_slice_index = R_comuna_data.index[R_comuna_data['Fecha'] == "2020-04-07"].tolist()
        end_slice_index = R_comuna_data.index[R_comuna_data['Fecha'] == slicing_date].tolist()
        for i in range(len(start_slice_index)):
            inter =  range(start_slice_index[i], end_slice_index[i])
            indices += inter
        R_comuna_data = R_comuna_data.iloc[indices]
    return R_comuna_data

def r_national_db(slicing_date = None):
    endpoint_R_national = requests.get('http://192.168.2.223:5006/getNationalEffectiveReproduction' )
    R_national = pd.DataFrame(json.loads(endpoint_R_national.text))
    R_national['Fecha'] = pd.DataFrame(R_national['dates']).apply(__iso_handler, axis = 1)
    R_national = R_national.rename(columns={'mean': 'MEAN','quantile0025': 'Low_95','quantile0975': 'High_95'})

    if slicing_date is not None:
        slice_index = R_national.index[R_national['Fecha'] == slicing_date].tolist()[0]
        R_national = R_national.iloc[:slice_index]

    return R_national

def active_cases_from_db(slicing_date = None):
    # not yet
    endpoint = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna_std.csv'
    data_comunas = pd.read_csv(endpoint)
    data_comunas = data_comunas.fillna(0)
    data_comunas['Region'] = data_comunas['Region'].replace( region_names_dict)

    if slicing_date is not None:
        year, month, day = slicing_date.split('-')
        weekday =  dtime.datetime(int(year), int(month), int(day)).weekday()
        if weekday>=0 and weekday<4: # nearest Tu
            dif = weekday#-1
        else:
            dif = weekday-4
        data_day = dtime.datetime(2020, 9, 21) - dtime.timedelta(days=dif)

        slice_index = data_comunas.index[data_comunas['Fecha'] == data_day.strftime("%Y-%m-%d")].tolist()[0]
        data_comunas = data_comunas.iloc[:slice_index]
        print('dc:' ,data_comunas, data_day.strftime("%y-%m-%d"), data_comunas.index[data_comunas['Fecha'] == data_day.strftime("%Y-%m-%d")].tolist())

    return data_comunas

def deaths_comunas_from_db(slicing_date = None):
    endpoint2 = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto38/CasosFallecidosPorComuna_std.csv'
    muertos_comunas = pd.read_csv(endpoint2)
    muertos_comunas = muertos_comunas.fillna(0)
    muertos_comunas['Region'] = muertos_comunas['Region'].replace( region_names_dict)

    if slicing_date is not None:
        year, month, day = slicing_date.split('-')
        weekday =  dtime.datetime(int(year), int(month), int(day)).weekday()
        if weekday>=0 and weekday<4: # nearest Tu
            dif = weekday#-1
        else:
            dif = weekday-4
        data_day = dtime.datetime(2020, 9, 21) - dtime.timedelta(days=dif)

        slice_index = data_comunas.index[muertos_comunas['Fecha'] == data_day.strftime("%Y-%m-%d")].tolist()[0]
        muertos_comunas = muertos_comunas.iloc[:slice_index]

    return muertos_comunas

def pcr_positivity_from_db(slicing_date = None):
    endpoint2 = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto49/Positividad_Diaria_Media_T.csv'
    pcr_positivity = pd.read_csv(endpoint2)
    pcr_positivity = pcr_positivity.dropna(axis='index', how = 'any')

    if slicing_date is not None:
        year, month, day = slicing_date.split('-')
        weekday =  dtime.datetime(int(year), int(month), int(day)).weekday()
        if weekday>=0 and weekday<4: # nearest Tu
            dif = weekday#-1
        else:
            dif = weekday-4
        data_day = dtime.datetime(2020, 9, 21) - dtime.timedelta(days=dif)

        slice_index = pcr_positivity.index[pcr_positivity.index == data_day.strftime("%Y-%m-%d")].tolist()[0]
        pcr_positivity = pcr_positivity.iloc[:slice_index]

    return pcr_positivity

def population_from_db():


    pop =pd.read_json('http://192.168.2.223:5006/getComunas')
    pop = pop[['state', 'state_name', 'county', 'county_name', 'province_name', 'male_pop', 'female_pop', 'total_pop']]
    #counties_info.index = counties_info['county'].astype(str).apply(lambda x:x.zfill(5))
    pop = pop.set_index('county_name')

    pop_reg = pop.pivot_table(index='state_name', values=['total_pop', 'male_pop', 'female_pop'], aggfunc=sum)
    return pop, pop_reg

def hospitales_reg():
    #dict = {"01":"Tarapacá", "02":"Antofagasta", "03":"Atacama","04":"Coquimbo","05":"Valparaíso", "06":"O'Higgins","07":"Maule","08":"Biobío",
    #"09":"La Araucanía","10":"Los Lagos","11":"Aysén", "12":"Magallanes","13","name":"Metropolitana", "14":"Los Ríos","15":"Arica","16":"Ñuble"]
    #order = ['15','01', '02', '03', '04', '05', '06', '07', '08', '16', '09', '14', '10', '11', '12', '13']
    dict_ss = {'Arica': 'SS ARICA',
            'Tarapacá': ' SS IQUIQUE',
            'Antofagasta': 'SS ANTOFAGASTA',
            'Atacama': 'SS ATACAMA',
            'Coquimbo': 'SS COQUIMBO',
            'Valparaíso': 'SS ACONCAGUA',
            'Valparaíso': 'SS VIÑA DEL MAR QUILLOTA',
            'Valparaíso': 'SS VALPARAISO SAN ANTONIO',
            "O'Higgins" : "SS LIBERTADOR B. O'HIGGINS ",
            'Maule' : 'SS MAULE',
            'Ñuble': 'SS ÑUBLE',
            'Bio-Bío': 'SS BÍO BÍO',
            'Bio-Bío' :'SS CONCEPCIÓN',
            'Bio-Bío' :'SS TALCAHUANO',
            'La Araucanía': 'SS ARAUCO',
            'La Araucania' :'SS ARAUCANÍA NORTE',
            'La Araucania' : 'SS ARAUCANÍA SUR',
            'Los Ríos' : 'SS VALDIVIA',
            'Los Lagos' :'SS OSORNO',
            'Los Lagos' :'SS RELONCAVÍ',
            'Los Lagos' : 'SS CHILOÉ',
            'Aysén' : 'SS AYSÉN',
            'Magallanes' : 'SS MAGALLANES',
            'Metropolitana': 'SS METROPOLITANO NORTE',
            'Metropolitana':'SS METROPOLITANO OCCIDENTE',
            'Metropolitana':'SS METROPOLITANO CENTRAL',
            'Metropolitana':'SS METROPOLITANO ORIENTE',
            'Metropolitana':'SS METROPOLITANO SUR',
            'Metropolitana':'SS METROPOLITANO SUR ORIENTE'
    }
    dict_ss = {'SS ARICA':'Arica',
            'SS IQUIQUE':'Tarapacá',
            'SS ANTOFAGASTA':'Antofagasta' ,
            'SS ATACAMA' : 'Atacama',
            'SS COQUIMBO': 'Coquimbo' ,
            'SS ACONGAGUA': 'Valparaíso',
            'SS VIÑA DEL MAR QUILLOTA': 'Valparaíso',
            'SS VALPARAISO SAN ANTONIO': 'Valparaíso',
            "SS LIBERTADOR B. O'HIGGINS" : "O'Higgins",
            'SS DEL MAULE' : 'Maule',
            'SS ÑUBLE' : 'Ñuble',
            'SS BÍO BÍO' : 'Bio-Bío',
            'SS CONCEPCIÓN' : 'Bio-Bío',
            'SS TALCAHUANO':'Bio-Bío',
            'SS ARAUCO' : 'La Araucanía',
            'SS ARAUCANÍA NORTE' : 'La Araucanía',
            'SS ARAUCANÍA SUR' : 'La Araucanía',
            'SS VALDIVIA' : 'Los Ríos' ,
            'SS OSORNO' : 'Los Lagos' ,
            'SS DEL RELONCAVÍ' : 'Los Lagos',
            'SS CHILOÉ' : 'Los Lagos' ,
            'SS AISÉN' : 'Aysén' ,
            'SS MAGALLANES' : 'Magallanes',
            'SS METROPOLITANO NORTE': 'Metropolitana',
            'SS METROPOLITANO OCCIDENTE' : 'Metropolitana',
            'SS METROPOLITANO CENTRAL' : 'Metropolitana',
            'SS METROPOLITANO ORIENTE' : 'Metropolitana',
            'SS METROPOLITANO SUR' : 'Metropolitana',
            'SS METROPOLITANO SUR ORIENTE' : 'Metropolitana'
    }

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

    HEALTH_SERVICE_prev = HEALTH_SERVICE_prev.rename(index = dict_ss)
    HEALTH_SERVICE_prev = HEALTH_SERVICE_prev.groupby(HEALTH_SERVICE_prev.index).sum()
    HEALTH_SERVICE_newest = HEALTH_SERVICE_newest.rename(index = dict_ss)
    HEALTH_SERVICE_newest = HEALTH_SERVICE_newest.groupby(HEALTH_SERVICE_newest.index).sum()


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


    summary_order = ["Arica","Tarapacá","Antofagasta","Atacama",
                    "Coquimbo","Valparaíso","O'Higgins","Maule",
                    "Ñuble","Bio-Bío","La Araucanía","Los Ríos",
                    "Los Lagos","Aysén","Magallanes","Metropolitana"]
    HEALTH_SERVICE_prev = HEALTH_SERVICE_prev.reindex(summary_order)
    HEALTH_SERVICE_newest = HEALTH_SERVICE_newest.reindex(summary_order)
    global sochi_date, sochi_date2
    sochi_date2, sochi_date = pd.to_datetime(days[0]).strftime("%d/%m"),pd.to_datetime(days[1]).strftime("%d/%m")
    HEALTH_SERVICE_newest = HEALTH_SERVICE_newest.drop(columns = ['Pacientes en Intensivo', 'Pacientes en Intermedio', 'Camas Intensivo', 'Camas Intermedio', 'Pacientes en VMI', 'Número VMI' ])
    HEALTH_SERVICE_prev = HEALTH_SERVICE_prev.drop(columns = ['Pacientes en Intensivo', 'Pacientes en Intermedio', 'Camas Intensivo', 'Camas Intermedio', 'Pacientes en VMI', 'Número VMI' ])

    print('b', HEALTH_SERVICE_newest)
    HEALTH_SERVICE_newest = HEALTH_SERVICE_newest[['Uso Intermedias','Uso Intensivas','Uso VMI']]
    HEALTH_SERVICE_prev = HEALTH_SERVICE_prev[['Uso Intermedias','Uso Intensivas','Uso VMI']]
    return days, HEALTH_SERVICE_prev, HEALTH_SERVICE_newest

def get_comunas_name():
    comunas =pd.read_json('http://192.168.2.223:5006/getComunas')
    comunas = comunas[['state', 'state_name', 'county', 'county_name', 'province_name', 'male_pop', 'female_pop', 'total_pop']]
    comunas = comunas.set_index('county_name')
    return comunas
