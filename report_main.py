from report_data_loader import *
from modular_report import *


def generate_table(file):
    date = file[-9:]
    Tabla = pd.read_csv(file, index_col = "county_name")
    Tabla.columns = ['Prevalencia', 'Tasa %', 'R_e', 'Activos', 'Probables',
           'Mortalidad']

    Tabla.drop('Probables', axis= 'columns', inplace = True)
    #Cambiar caracteres
    Tabla = Tabla.apply(lambda x: x.astype(str).str.replace(',','.'))
    Tabla = Tabla.apply(lambda x: x.astype(str).str.replace('ND','0'))
    Tabla = Tabla.apply(lambda x: x.astype(str).str.replace('%',''))

    # Pasar de string a float
    columns = Tabla.columns
    for column in columns:

        Tabla[column] = pd.to_numeric(Tabla[column])

    #Renombrar columna
    Tabla = Tabla.rename(columns={'Tasa': 'Tasa %'})
    Tabla.to_csv('Tables/Tabla_'+date)


def report_gen(slice_date = None):
    ### get date and check report type : latest/sliced; None = latest
    if slice_date == str(report_date()[0]).split(' ')[0]:
        corrected_day, report_day = report_date()
        day, month = report_day.split('/')
        fecha = dt.date(2019,12,30)
        delta = corrected_day- fecha # Semana epidemiologica
        slice_date = None

    elif slice_date is not None:
        fecha = dt.date(2019,12,30)
        year, month, day = slice_date.split('-')
        corrected_day = dt.date(int(year),int(month),int(day))
        report_day = corrected_day.strftime("%d/%m")
        delta = corrected_day - fecha

    ### Load data ###
    pop, pop_reg = population_from_db()

    erre = r_comunas_db(slice_date)
    erre_reg = r_regions_db(slice_date)
    erre_national = r_national_db(slice_date)

    active_comunas = active_cases_from_db() # slicing ready
    data_region = active_comunas[active_comunas.Comuna!='Total'].pivot_table(index=['Region','Fecha'], values='Casos activos', aggfunc=sum)
    muertos_comunas = deaths_comunas_from_db()

    subrep = pd.DataFrame(underreporting_by_region()).T
    subrep_national = underreporting_national()

    dict = {"01":"Tarapacá",    "02":"Antofagasta",
            "03":"Atacama",     "04":"Coquimbo",
            "05":"Valparaíso",  "06":"Libertador General Bernardo O\'Higgins",
            "07":"Maule",       "08":"Biobío",
            "09":"La Araucanía","10":"Los Lagos",
            "11":"Aysén del General Carlos Ibáñez del Campo",
            "12":"Magallanes y de la Antártica Chilena",
            "13":"Metropolitana de Santiago", "14":"Los Ríos",
            "15":"Arica y Parinacota","16":"Ñuble"}

    datos_comunas = pd.DataFrame(index=[0,1,2,3], columns=active_comunas['Codigo comuna'].unique())
    muerte_comunas = pd.DataFrame(index=[0,1,2,3], columns=muertos_comunas['Codigo comuna'].unique())
    datos_region = pd.DataFrame(index=[0,1,2,3], columns=active_comunas['Region'].unique())
    del datos_comunas[0.0]

    for reg in datos_region.columns:
        datos_region[reg] = data_region.loc[reg]['Casos activos'].iloc[-4:].values
    for com in datos_comunas.columns:
        datos_comunas[com] = active_comunas[active_comunas['Codigo comuna']==com]['Casos activos'].iloc[-4:].values
        muerte_comunas[com] = muertos_comunas[muertos_comunas['Codigo comuna']==com]['Casos fallecidos'].iloc[-4:].values

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
        comuna = pop[pop.county==com].index.values[0]
        prevalencia[comuna] = datos_comunas[com]*10000 / pop[pop.county==com]['total_pop'].values # /datos_comunas
        mortalidad[comuna] = muerte_comunas[com]*100000 / pop[pop.county==com]['total_pop'].values

    prevalencia_region = pd.DataFrame()
    mortalidad_region = pd.DataFrame(index=[0,1,2,3])
    for reg in datos_region.columns:

        prevalencia_region[reg] = datos_region[reg]*10000 / pop_reg.loc[reg,'total_pop']
        for i in range(4):
            mortalidad_region.loc[i,reg] = muertos_region.loc[reg].iloc[i-4].values*100000 / pop_reg.loc[reg,'total_pop']

    chile_prvlnc = pd.DataFrame([(datos_comunas.sum(axis=1) *10000 / pop_reg.total_pop.sum())])

    prvlnc_diff = prevalencia.sub(chile_prvlnc.T.mean(axis=1), axis=0)
    ########################## calculo tasa, prevalencia y mortalidad semanal ############################
    muni_raw_rate = 1 - datos_comunas.shift(1) / datos_comunas
    muni_raw1, muni_raw2 = muni_raw_rate.iloc[0:2].mean(axis=0), muni_raw_rate.iloc[2:4].mean(axis=0)

    weekly_prev1, weekly_prev2 = prevalencia.iloc[0:2].mean(axis=0), prevalencia.iloc[2:4].mean(axis=0)
    death_rate1, death_rate2 = mortalidad[0:2].diff(axis = 0).iloc[1], mortalidad[2:4].diff(axis = 0).iloc[1]
    ######################################################################################################
    erre = erre.replace({'comuna': indices_dict})
    R_p = erre.pivot_table(index=['comuna','Fecha'])

    R0 = pd.Series(data=np.zeros(len(pop.index)), index=pop.index)
    for comuna in pop.index:
        try:
            if R_p.MEAN.loc[comuna][-1]==0:
                R0.loc[comuna] = 0
            elif len(R_p.MEAN.loc[comuna]) > 13:
                R0.loc[comuna] = R_p.MEAN.loc[comuna].iloc[-14:].mean()

        except:
            print(comuna,'not found')
            R0.loc[comuna] = np.nan

    erre_reg = erre_reg.replace({'name':
                        {'Metropolitana':'Metropolitana de Santiago',
                        "Lib. Gral. Bernardo O'Higgins":"Libertador General Bernardo O'Higgins",
                        'Araucanía':'La Araucanía',
                        'Aysén del Gral. C. Ibáñez del Campo':'Aysén del General Carlos Ibáñez del Campo',
                        'Magallanes y Antártica Chilena':'Magallanes y de la Antártica Chilena'}})
    R_p_reg = erre_reg.pivot_table(index=['name','Fecha'])

    R0_reg = pd.Series(data=np.zeros(16), index=regiones)
    for region in R0_reg.index:
        try:
            if len(R_p_reg.MEAN.loc[region]) > 13:##?
                R0_reg.loc[region] = R_p_reg.MEAN.loc[region].iloc[-14:].mean()
        except:
            print('Reg Exception', region)
            R0_reg.loc[region] = np.nan

    comun_per_region = pop['state_name'] # try changing for pop

    subrep = subrep.rename(index=dict)
    ########################## Creando dataFrame de visualización ############################
    display = pd.DataFrame(index=pop.index)
    display['Prevalencia'] = [prevalencia.T[3].loc[c] for c in display.index]
    display['Tasa'] = [muni_avg_rate.T[3].loc[pop[pop.index==c].county.values[0]] for c in display.index]
    display['R_e'] = R0
    display['Inf. Activos'] = [datos_comunas[int(pop[pop.index==c].county.values[0])].loc[3] for c in display.index]
    for c in display.index:
        if comun_per_region[c] in subrep.index: #aqui
            infected = datos_comunas[int(pop[pop.index==c].county.values[0])].loc[3]

            high = (1-subrep.high[comun_per_region[c]][-1])
            if high>1: high = 1
            low = (1-subrep.low[comun_per_region[c]][-1])
            if low<0: low= 0

            display.loc[c,'Inf. Act. Probables'] = '{:.0f} ~ {:.0f}'.format(infected /high, infected /low)
        else:
            display.loc[c,'Inf. Act. Probables'] = '-'
    display['Mortalidad'] = [mortalidad.T[3].loc[c] for c in display.index]
    display = display.fillna(0)


    reg_display = pd.DataFrame(index=pop_reg.index)
    reg_display['Prevalencia'] = [prevalencia_region.loc[3,r] for r in reg_display.index]
    reg_display['Tasa'] = [region_avg_rate.loc[3,r] for r in reg_display.index]
    reg_display['R_e'] = R0_reg

    for r in reg_display.index:
        infected = data_region.loc[r].iloc[-1].values[0]
        reg_display.loc[r,'Inf. Activos'] = infected
        if r in subrep.index:
            high = (1-subrep.high[r][-1])
            if high>1: high = 1
            low = (1-subrep.low[r][-1])
            if low<0: low= 0
            reg_display.loc[r,'Inf. Act. Probables'] = '{:.0f} ~ {:.0f}'.format(infected /high, infected /low)
        else:
            reg_display.loc[r,'Inf. Act. Probables'] = '-'
    reg_display['Mortalidad'] = [mortalidad_region[r].loc[3] for r in reg_display.index]

    ## R arrow represent R rate of change
    R_arrow_last = pd.Series(data=np.zeros(len(pop.index)), index=pop.index)
    R_arrow_past = pd.Series(data=np.zeros(len(pop.index)), index=pop.index)
    for comuna in pop.index:
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

    ########################## Formateando tabla para visualización ############################
    display_values = display.copy()
    reg_display_values = reg_display.copy()
    display['Prevalencia'] = display['Prevalencia'].map('{:.2f}'.format)
    display['Tasa'] = display['Tasa'].map('{:,.2%}'.format)    # filenames.append(Nacional_page(pd.read_csv('time_series/R_Efectivo_nacional_'+report_day.replace('/','_')+'.csv'), chile_avg_rate, chile_prvlnc, subrep, activos, report_day))

    display['R_e'] = display['R_e'].map('{:,.2f}'.format)
    display['Inf. Activos'] = display['Inf. Activos'].map('{:,.0f}'.format)
    display['Mortalidad'] = display['Mortalidad'].map('{:,.2f}'.format)
    reg_display['Prevalencia'] = reg_display['Prevalencia'].map('{:,.2f}'.format)
    reg_display['Tasa'] = reg_display['Tasa'].map('{:,.2%}'.format)
    reg_display['R_e'] = reg_display['R_e'].map('{:,.2f}'.format)
    reg_display['Inf. Activos'] = reg_display['Inf. Activos'].map('{:,.0f}'.format)
    reg_display['Mortalidad'] = reg_display['Mortalidad'].map('{:,.2f}'.format)

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
    ## guardamos el display en 2 formatos
    display.to_csv('Tables/display_{}.csv'.format(report_day.replace('/','_')))
    #generate_table('Tables/display_{}.csv'.format(report_day.replace('/','_')))
    # funcion display
    ####################################################################################################
    data = erre_reg #?
    data = data.set_index('Fecha')
    data.index = pd.to_datetime(data.index)
    data.index = [x.strftime("%d/%m/%y") for x in data.index]
    data = data.rename(columns={'Mean(R)': 'MEAN','Quantile.0.025(R)': 'Low_95','Quantile.0.975(R)': 'High_95'})
    activos = np.sum(reg_display_values['Inf. Activos'])
    uci_data = load_uci_data(slice_date)
    ### generate report
    reporte = report(report_day.replace('/','_'))
    reporte.add_cover(report_day, delta)
    reporte.add_summary(reg_display, prevalencia_region, region_avg_rate, subrep,data, uci_data, report_day, chile_prvlnc, chile_avg_rate, subrep_national, erre_national)
    reporte.add_national_page(erre_national, chile_avg_rate, chile_prvlnc, subrep_national, activos, report_day)
    reporte.add_underreporting_page(subrep_national, report_day)
    reporte.add_regiones_page(report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last, death_rate1,death_rate2)
    reporte.add_metropolitana_page(report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last,death_rate1,death_rate2)
    reporte.add_otras_provincias_page(report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last,death_rate1,death_rate2)
    reporte.end_pages()
    pass
