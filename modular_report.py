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
import os
from zipfile import ZipFile
#from report_utils import *
from report_data_loader import *
from matplotlib.backends.backend_pdf import PdfPages


class report(object):
    """docstring"""

    def __init__(self, date):
        super(report, self).__init__()
        self.pages = []
        self.predefined_types = ['national', 'state', 'summary', 'cover']
        self.slicing_date = None
        self.simulate_report = False
        self.date = date
        self.pdf = PdfPages('reporte_'+date+'.pdf')#formatear
        self.logos = mpimg.imread('logos/uss_cinv_udd.png')
        self.logo_sochimi = mpimg.imread('logos/logo_sochimi.png')
        self.logo_fcv = mpimg.imread('logos/logos.png')
        self.logofcv = mpimg.imread('logos/logo_fcv.png')
        self.logofinis= mpimg.imread('logos/logo_finis.png')

    def current_r_date():
        endpoint_R = requests.get('http://192.168.2.223:5006/getNationalEffectiveReproduction' )
        R = json.loads(endpoint_R.text)
        year, month, day = str(R['dates'][-1].split('T')[0]).split('-')
        date = dtime.datetime(int(year),int(month),int(day))
        date += dtime.timedelta(days=1)

        r_day = date.strftime("%d/%m")
        return date.date() , r_day

    def current_report_day():
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

    ## PAGES
    def add_cover(self, report_day, delta):
        sns.set_context("paper", font_scale=1)
        figcover = plt.figure(edgecolor='k', figsize=(11,8.5))
        axlogos = figcover.add_axes([0.05,.67,.3*1.1,.3*1.1]) # [0.05,.7,.3,.3]
        axsochi = figcover.add_axes([0.30,.8,.2*1.2,.085*1.2])
        axfcv = figcover.add_axes([.8,.75,.15,.2])
        axmain = figcover.add_axes([.0,.0,1,.9])

        axlogos.imshow(self.logos)
        axsochi.imshow(self.logo_sochimi)
        axfcv.imshow(self.logo_fcv[:,:1000])
        axmain.axis('off')
        axlogos.axis('off')
        axsochi.axis('off')
        axfcv.axis('off')

        authors = r'César Ravello $^{1,3}$, Felipe Castillo $^{1,3}$, Tomás Villaseca¹, Samuel Ropert $^{1,3}$, Alejandro Bernardin $^{1,3}$, Tomás Pérez-Acle $^{1,2,3}$'
        affiliations = '¹Computational Biology Lab, Fundación Ciencia & Vida, Santiago, Chile\n²Centro Interdisciplinario de Neurociencia de Valparaíso, Universidad de Valparaíso, Chile\n³Universidad San Sebastián, Chile\n\nAgradecimientos: Proyecto CV19GM AFOSR grant number FA9550-20-1-0196'

        axmain.text(.5,.7, 'Impacto de la pandemia Covid19 en Chile', ha='center', fontsize='xx-large')
        axmain.text(.5,.6, 'Reporte al ' + report_day + '\nSemana epidemiológica {}'.format(ceil(delta.days/7)), ha='center', fontsize='xx-large')
        axmain.text(.5,.25, authors, ha='center')
        axmain.text(.5,.15, affiliations, ha='center', fontsize='small')

        figcover.savefig(self.pdf, format='pdf', dpi=600)
        plt.savefig('cover.png', format='png', dpi=600)
        pass

    def add_otras_provincias_page(self,report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last,death_rate1,death_rate2 ):
        sns.set_context("paper", font_scale=.6)
        every_nth = 21


        fig = plt.figure(figsize=(11, 8.5))
        fig.text(0.95,0.06, '©2020, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha='right', fontsize='large')
        ax_logo = fig.add_axes([.85,.875,.1,.1])
        ax_logo.imshow(self.logofcv)
        ax_logo.axis('off')
        ax_cinv = fig.add_axes([.05,.875,.25,.08])
        ax_sochi = fig.add_axes([.775,.885,.07,.07])
        ax_cinv.imshow(self.logos)
        ax_sochi.imshow(self.logo_sochimi)
        ax_cinv.axis('off')
        ax_sochi.axis('off')
        dates = pd.to_datetime(subrep['date']['Metropolitana de Santiago']).strftime('%d-%m-%y')
        ## Encabezado
        region = 'Metropolitana de Santiago'
        r = 15
        mean = (1-subrep['mean'][region][-1]) # reporte
        if mean>1: mean = 1
        high = (1-subrep['low'][region][-1])
        low = (1-subrep['high'][region][-1])
        if low<0: low = 0
        high = (1-subrep['low'][region][-1])
        if high > 1 : high = 1

        fig.text(.5, .935, 'Región Metropolitana: otras provincias', horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='xx-large')
        fig.text(.5, .9, 'Datos últimos 14 días\nPrevalencia región: {} / Tasa región: {}%\nEstimación de infectados sintomáticos detectados: {:.0f}% ({:.0f}% - {:.0f}%)'.format('{:.2f}'.format(prevalencia_region.loc[3,'Metropolitana de Santiago']).replace('.',','), '{:.2f}'.format(region_avg_rate.loc[3,'Metropolitana de Santiago']*100).replace('.',','), mean*100,low*100,high*100),
             horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='x-large')

        ## Leyendas def regional_legend
        fig.text(.187, .825, '1', fontsize='small')
        fig.text(.2335, .825, '2', fontsize='small')
        fig.text(.2775, .825, '3', fontsize='small')
        fig.text(.3405, .825, '4', fontsize='small')
        fig.text(.4225, .825, '5', fontsize='small')
        fig.text(.4825, .825, '6', fontsize='small')
        #fig.text(.5275, .825, '7', fontsize='small')
        #fig.text(.5875, .825, '7', fontsize='small')
        fig.text(.605, .27, 'Prevalencia \u2264 4', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .26, '4 < Prevalencia < 5', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .25, 'Prevalencia \u2265 5', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

        fig.text(.705, .27, 'Tasa \u2264 25%', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.705, .26, '25% < Tasa < 30%', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.705, .25, 'Tasa \u2265 30%', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

        fig.text(.805, .27, 'R_e \u2264 0,8', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.805, .26, '0,8 < R_e < 1,0', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.805, .25, 'R_e \u2265 1,0', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

        fig.text(0.605,0.06,
                 '1 Infectados activos / 10.000 habitantes.\n'+
                 '2 Tasa diaria de nuevos infectados (promedio acumulado).\n'+
                 '3 R_e últimos 14 días según Cori et al. (2019)\n'
                 '4 Datos epidemiológicos\nhttps://github.com/MinCiencia/Datos-COVID19\n'+
                 '5 De acuerdo a subreporte según\nhttps://cmmid.github.io/topics/covid19/global_cfr_estimates.html\n'+
                 '6 Fallecimientos acumulados COVID19 / 100.000 habitantes\n'+
                 #'7 Datos movilidad '+im_dates+' vs. 09/03-15/03.\n'+
                #     'https://github.com/MinCiencia/Datos-COVID19, producto 33.\n'+
                 '7 Datos regionales incluyen casos de comuna desconocida\n'+'\n'+
                 '- ND no hay suficientes datos para calcular R_e.\n'+
                 #'- Uso de camas por Servicio de Salud al ' + sochi_date + ' según SOCHIMI.\n'+
                 '- Flechas R_e: cambio mayor/menor a 5% vs ultimos 7 días.\n'+
                 '- Otras flechas: cambio mayor/menor a 5% vs semana anterior.\n'
                 , ha='left',fontsize='large')

        ax = fig.add_axes([.125, .01, .475, .84])
        selection = pop[(pop['state_name']=='Metropolitana de Santiago')&(pop['province_name']!='Santiago')].index.values
        #make_table(display.loc[selection], display_values.loc[selection], ax, True)
        self._make_table(display.loc[selection], display_values.loc[selection],
                       reg_display[reg_display.index==region].rename(index={region:'VALOR REGIONAL ⁷'}), reg_display_values[reg_display.index==region], ax, True)
        self._add_arrows(display_values.loc[selection], muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last,death_rate1,death_rate2, ax, 0.49, .935, .18, .06, .29,.68,.905,.0315, .0205)
        #fig.text(.12, .85, 'Región de ' + regiones[r], horizontalalignment='left', verticalalignment='center', weight = 'bold')

        ax2 = fig.add_axes([.645, .625, .3, .22])#.645, .595, .3, .22])
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

        r_dates = pd.to_datetime(data.index[1:])
        ticks_labels = [r_dates[i].strftime("%d-%m-%y")  for i in range(len(r_dates))]
        ax2.tick_params(axis='x',rotation=45, bottom=False, left=True, labelleft=True, labelbottom=True)
        ax2.set_xticklabels(ticks_labels)#, fontdict = {'fontsize' : '8'})

        #plt.xticks(rotation=45)
        #ax2.tick_params(bottom=False, left=True, labelleft=True, labelbottom=True)
        for n, label in enumerate(ax2.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
        ax2.set_ylabel('R efectivo')
        ax2.set_ylim([0,3])

        ax3 = fig.add_axes([.645, .335, .3, .22])
        ax3.plot(dates, np.asarray(subrep['mean'][region])*100)
        ax3.fill_between(dates, np.asarray(subrep['low'][region])*100, np.asarray(subrep['high'][region])*100, alpha=0.4)
        ax3.set_ylim([0,100])
        ax3.set_ylabel('% Subreporte')
        ax3.tick_params(axis = 'x', rotation=45)
        ax3.tick_params(bottom=False, left=True, labelleft=True, labelbottom=True)
        color = 'purple'
        m, l, h, i = asp_state(region, subrep)
        pos = []
        for j, ind in enumerate(i):
            pos +=[dates.get_loc(ind)]
        ax2 = ax3.twinx()
        ax2.set_ylabel('Infectados sintomáticos activos probables', color='black', fontsize = 7)
        p2, = ax2.plot(pos,m,color=color)
        ax2.tick_params(axis='y', labelcolor='black')
        ax2.set_ylim(bottom =0)
        for n, label in enumerate(ax3.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)

        fig.savefig(self.pdf, format='pdf', dpi=1200)
        plt.savefig('otras_provincias.png', format = 'png', dpi = 600)
        pass

    # FOR TABLES
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

    def color_dim(data):#23, 41, 58
        if data <= .3: color = '#00cc66'
        elif data < .4: color = '#ffcc00'
        else: color = '#ff0000'
        return color

    def add_regiones_page(self, report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last,death_rate1,death_rate2):

        sns.set_context("paper", font_scale=.6)
        every_nth = 21
        filenames = []
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
        underreporting = underreporting_by_region()
        dict = {"01":"Tarapacá",    "02":"Antofagasta",
                "03":"Atacama",     "04":"Coquimbo",
                "05":"Valparaíso",  "06":"Libertador General Bernardo O\'Higgins",
                "07":"Maule",       "08":"Biobío",
                "09":"La Araucanía","10":"Los Lagos",
                "11":"Aysén del General Carlos Ibáñez del Campo",
                "12":"Magallanes y de la Antártica Chilena",
                "13":"Metropolitana", "14":"Los Ríos",
                "15":"Arica y Parinacota","16":"Ñuble"}
        inv_map = {v: k for k, v in dict.items()}
        for r, region in enumerate(regiones[:-1]):

            fig = plt.figure(figsize=(11, 8.5))
            ## Logos
            fig.text(0.95,0.06, '©2020, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha='right', fontsize='large')
            ax_logo = fig.add_axes([.85,.875,.1,.1])
            ax_logo.imshow(self.logofcv)
            ax_logo.axis('off')
            ax_cinv = fig.add_axes([.05,.875,.25,.08])
            ax_sochi = fig.add_axes([.775,.885,.07,.07])
            ax_cinv.imshow(self.logos)
            ax_sochi.imshow(self.logo_sochimi)
            ax_cinv.axis('off')
            ax_sochi.axis('off')

            ## Encabezado
            fig.text(.5, .935, 'Región de ' + regiones[r], horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='xx-large')
            if region in subrep.index and region != "Aysén del General Carlos Ibáñez del Campo":
                reg_num = inv_map[region]
                dates = pd.to_datetime(underreporting.loc[reg_num]['date']).strftime('%d-%m-%y')
                mean = (1-underreporting.loc[reg_num]['mean'][-1]) #reporte
                if mean>1: mean = 1
                low = (1-underreporting.loc[reg_num]['high'][-1]) #estan al revés
                if low <0: low = 0
                high = (1-underreporting.loc[reg_num]['low'][-1])
                if high > 1: high = 1
                fig.text(.5, .9, 'Datos últimos 14 días\nPrevalencia región: {} / Tasa región: {}%\nEstimación de infectados sintomáticos detectados: {:.0f}% ({:.0f}% - {:.0f}%)'.format('{:.2f}'.format(prevalencia_region.loc[3,region]).replace('.',','), '{:.2f}'.format(region_avg_rate.loc[3,region]*100).replace('.',','), mean*100, low*100, high*100),
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
            #fig.text(.5275, .825, '7', fontsize='small')
            #fig.text(.5875, .825, '7', fontsize='small')  605, 52 51 50 - - 47...
            fig.text(.605, .27, 'Prevalencia \u2264 4', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
            fig.text(.605, .26, '4 < Prevalencia < 5', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
            fig.text(.605, .25, 'Prevalencia \u2265 5', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

            fig.text(.705, .27, 'Tasa \u2264 25%', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
            fig.text(.705, .26, '25% < Tasa < 30%', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
            fig.text(.705, .25, 'Tasa \u2265 30%', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

            fig.text(.805, .27, 'R_e \u2264 0,8', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
            fig.text(.805, .26, '0,8 < R_e < 1,0', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
            fig.text(.805, .25, 'R_e \u2265 1,0', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

            #fig.text(.705, .23, 'Movilidad remanente \u2264 30%', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
            #fig.text(.705, .22, '30% < Movilidad remanente < 40%', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
            #fig.text(.705, .21, 'Movilidad remanente \u2265 40%', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

            fig.text(0.605,0.06,
                 '1 Infectados activos / 10.000 habitantes.\n'+
                 '2 Tasa diaria de nuevos infectados (promedio acumulado).\n'+
                 '3 R_e últimos 14 días según Cori et al. (2019)\n'
                 '4 Datos epidemiológicos\nhttps://github.com/MinCiencia/Datos-COVID19\n'+
                 '5 De acuerdo a subreporte según\nhttps://cmmid.github.io/topics/covid19/global_cfr_estimates.html\n'+
                 '6 Fallecimientos acumulados COVID19 / 100.000 habitantes\n'+
                 #'7 Datos movilidad '+im_dates+' vs. 09/03-15/03.\n'+
                 #    'https://github.com/MinCiencia/Datos-COVID19, producto 33.\n'
                 '7 Datos regionales incluyen casos de comuna desconocida\n'+'\n'+
                 '- ND no hay suficientes datos para calcular R_e.\n'+
                 #'- Uso de camas por Servicio de Salud al ' + sochi_date + ' según SOCHIMI.\n'+
                 '- Flechas R_e: cambio mayor/menor a 5% vs ultimos 7 días.\n'+
                 '- Otras flechas: cambio mayor/menor a 5% vs semana anterior.\n'
                 , ha='left',fontsize='large')#'x-large')

            ax = fig.add_axes([.125, .01, .475, .84])
            selection = comun_per_region[comun_per_region == region].index

            self._make_table(display.loc[selection], display_values.loc[selection],
                       reg_display[reg_display.index==region].rename(index={region:'VALOR REGIONAL ⁷'}), reg_display_values[reg_display.index==region], ax, True)
            self._add_arrows(display_values.loc[selection], muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last,death_rate1,death_rate2, ax, *arrow_props[r])

            ax2 = fig.add_axes([.645, .625, .3, .22])
            # comuna = regiones_short[r]
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

            r_dates = pd.to_datetime(data.index[1:])
            ticks_labels = [r_dates[i].strftime("%d-%m-%y")  for i in range(len(r_dates))]
            ax2.tick_params(axis='x',rotation=45, bottom=False, left=True, labelleft=True, labelbottom=True)
            ax2.set_xticklabels(ticks_labels)#, fontdict = {'fontsize' : '8'})

            plt.xticks(rotation=45)
            ax2.tick_params(bottom=False, left=True, labelleft=True, labelbottom=True)
            for n, label in enumerate(ax2.xaxis.get_ticklabels()):
                if n % every_nth != 0:
                    label.set_visible(False)
            ax2.set_ylabel('R efectivo')
            ax2.set_ylim([0,3])
    	    # if data != None
            if region in subrep.index and region !="Aysén del General Carlos Ibáñez del Campo":
                ax3 = fig.add_axes([.645, .335, .3, .22])
                ax3.plot(dates,np.asarray(underreporting.loc[reg_num]['mean'])*100)
                ax3.fill_between(dates,np.asarray(underreporting.loc[reg_num]['low'])*100,np.asarray(underreporting.loc[reg_num]['high'])*100, alpha=0.4)
                ax3.tick_params(axis = 'x', rotation=45)
                ax3.set_ylim([0,100])
                ax3.set_ylabel('% Subreporte')
                ax3.tick_params(bottom=False, left=True, labelleft=True, labelbottom=True)
                color = 'purple'
                m, l, h, i = asp_state(region, subrep)
                pos = []
                for j, ind in enumerate(i):
                    pos +=[dates.get_loc(ind)]
                ax2 = ax3.twinx()
                ax2.set_ylabel('Infectados sintomáticos activos probables', color='black', fontsize = 7)
                p2, = ax2.plot(pos,m,color=color)
                ax2.tick_params(axis='y', labelcolor='black')
                ax2.set_ylim(bottom =0)
                for n, label in enumerate(ax3.xaxis.get_ticklabels()):
                    if n % every_nth != 0:
                        label.set_visible(False)


            filename = 'Report/Report_{}_RP{}.pdf'.format(report_day.replace('/','_'), r)
            fig.savefig(self.pdf, format='pdf', dpi=1200)
            plt.savefig('region'+region+'.png', format = 'png', dpi = 600)

        pass

    def add_metropolitana_page(self, report_day, pop, display, display_values, reg_display, reg_display_values, data, subrep, region_avg_rate,prevalencia_region, comun_per_region, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last,death_rate1,death_rate2):
        sns.set_context("paper", font_scale=.6)
        logos = mpimg.imread('logos/uss_cinv_udd.png')
        logo_sochimi = mpimg.imread('logos/logo_sochimi.png')
        logo_fcv = mpimg.imread('logos/logos.png')
        logofcv = mpimg.imread('logos/logo_fcv.png')
        logofinis= mpimg.imread('logos/logo_finis.png')
        every_nth = 21
        dates = pd.to_datetime(subrep['date']['Metropolitana de Santiago']).strftime('%d/%m/%y')
        ## Encabezados, pies de página y leyendas
        fig = plt.figure(figsize=(11, 8.5))
        ## Logos
        fig.text(0.95,0.06, '©2020, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha='right', fontsize='large')
        ax_logo = fig.add_axes([.85,.875,.1,.1])
        ax_logo.imshow(self.logofcv)
        ax_logo.axis('off')
        ax_cinv = fig.add_axes([.05,.875,.25,.08])
        ax_sochi = fig.add_axes([.775,.885,.07,.07])
        ax_cinv.imshow(self.logos)
        ax_sochi.imshow(self.logo_sochimi)
        ax_cinv.axis('off')
        ax_sochi.axis('off')

        ## Encabezado
        region = 'Metropolitana de Santiago'
        r = 15

        mean = (1-subrep['mean']['Metropolitana de Santiago'][-1]) # reporte
        if mean>1: mean = 1
        low = (1-subrep['high']['Metropolitana de Santiago'][-1])
        if low<0: low = 0
        high = (1-subrep['low']['Metropolitana de Santiago'][-1])
        if high > 1 : high = 1
        fig.text(.5, .935, 'Región Metropolitana: Provincia de Santiago', horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='xx-large')
        fig.text(.5, .9, 'Datos últimos 14 días\nPrevalencia región: {} / Tasa región: {}%\nEstimación de infectados sintomáticos detectados: {:.0f}% ({:.0f}% - {:.0f}%)'.format('{:.2f}'.format(prevalencia_region.loc[3,'Metropolitana de Santiago']).replace('.',','), '{:.2f}'.format(region_avg_rate.loc[3,'Metropolitana de Santiago']*100).replace('.',','), mean*100,low*100,high*100),
             horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='x-large')
        ## Leyendas
        fig.text(.187, .825, '1', fontsize='small')
        fig.text(.2335, .825, '2', fontsize='small')
        fig.text(.2775, .825, '3', fontsize='small')
        fig.text(.3405, .825, '4', fontsize='small')
        fig.text(.4225, .825, '5', fontsize='small')
        fig.text(.4825, .825, '6', fontsize='small')
        #fig.text(.5275, .825, '7', fontsize='small')
        #fig.text(.5875, .825, '7', fontsize='small')
        fig.text(.605, .27, 'Prevalencia \u2264 4', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .26, '4 < Prevalencia < 5', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.605, .25, 'Prevalencia \u2265 5', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

        fig.text(.705, .27, 'Tasa \u2264 25%', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.705, .26, '25% < Tasa < 30%', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.705, .25, 'Tasa \u2265 30%', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

        fig.text(.805, .27, 'R_e \u2264 0,8', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.805, .26, '0,8 < R_e < 1,0', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        fig.text(.805, .25, 'R_e \u2265 1,0', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

        #fig.text(.605, .37, 'Movilidad remanente \u2264 30%', color='#00cc66', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        #fig.text(.605, .36, '30% < Movilidad remanente < 40%', color='#ffcc00', horizontalalignment='left', verticalalignment='center', weight = 'bold')
        #fig.text(.605, .35, 'Movilidad remanente \u2265 40%', color='#ff0000', horizontalalignment='left', verticalalignment='center', weight = 'bold')

        fig.text(0.605,0.06,
                 '1 Infectados activos / 10.000 habitantes.\n'+
                 '2 Tasa diaria de nuevos infectados (promedio acumulado).\n'+
                 '3 R_e últimos 14 días según Cori et al. (2019)\n'
                 '4 Datos epidemiológicos\nhttps://github.com/MinCiencia/Datos-COVID19\n'+
                 '5 De acuerdo a subreporte según\nhttps://cmmid.github.io/topics/covid19/global_cfr_estimates.html\n'+
                 '6 Fallecimientos acumulados COVID19 / 100.000 habitantes\n'+
                 #'7 Datos movilidad '+im_dates+' vs. 09/03-15/03.\n'+
                #     'https://github.com/MinCiencia/Datos-COVID19, producto 33.\n'+
                 '7 Datos regionales incluyen casos de comuna desconocida\n'+'\n'+
                 '- ND no hay suficientes datos para calcular R_e.\n'+
                 #'- Uso de camas por Servicio de Salud al ' + sochi_date + ' según SOCHIMI.\n'+
                 '- Flechas R_e: cambio mayor/menor a 5% vs ultimos 7 días.\n'+
                 '- Otras flechas: cambio mayor/menor a 5% vs semana anterior.\n'
                 , ha='left',fontsize='large')

        ax = fig.add_axes([.125, .01, .475, .84])
        selection = pop[pop['province_name']=='Santiago'].index.values
        self._make_table(display.loc[selection], display_values.loc[selection],
                       reg_display[reg_display.index==region].rename(index={region:'VALOR REGIONAL ⁷'}), reg_display_values[reg_display.index==region], ax, True)
        self._add_arrows(display_values.loc[selection], muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last,death_rate1,death_rate2, ax, 0.21, .935, .18, .06, .29,.68,.905,.0315, .0205)

        ax2 = fig.add_axes([.645, .625, .3, .22])#.645, .595, .3, .22])
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
        ax3 = fig.add_axes([.645, .335, .3, .22])
        ax3.plot(dates,np.asarray(subrep['mean']['Metropolitana de Santiago'])*100)
        ax3.fill_between(dates, np.asarray(subrep['low']['Metropolitana de Santiago'])*100, np.asarray(subrep['high']['Metropolitana de Santiago'])*100, alpha=0.4)
        ax3.tick_params(axis = 'x', rotation=45)
        ax3.set_ylim([0,100])
        ax3.set_ylabel('% Subreporte')
        ax3.tick_params(bottom=False, left=True, labelleft=True, labelbottom=True)
        color = 'purple'
        m, l, h, i = asp_state(region, subrep)
        pos = []
        for j, ind in enumerate(i):
            pos +=[dates.get_loc(ind)]
        ax2 = ax3.twinx()
        ax2.set_ylabel('Infectados sintomáticos activos probables', color='black', fontsize = 7)
        p2, = ax2.plot(pos,m,color=color)
        ax2.tick_params(axis='y', labelcolor='black')
        ax2.set_ylim(bottom =0)
        for n, label in enumerate(ax3.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)


        filename = 'Report/Report_{}_RP{}.pdf'.format(report_day.replace('/','_'), r)
        fig.savefig(self.pdf, format='pdf', dpi=1200)
        plt.savefig('metropolitana.png', format = 'png', dpi = 600)
        pass

    def add_underreporting_page(self, national_underrep, report_day):
        logos = mpimg.imread('logos/uss_cinv_udd.png')
        logo_sochimi = mpimg.imread('logos/logo_sochimi.png')
        logo_fcv = mpimg.imread('logos/logos.png')
        logofcv = mpimg.imread('logos/logo_fcv.png')
        logofinis= mpimg.imread('logos/logo_finis.png')
        sns.set_context("paper", font_scale=.6)
        #fig, axs = plt.subplots(6,1,figsize=(8.5, 13), gridspec_kw={'height_ratios': [0.5,15,0.1, 0.5,15,4.5]})
        fig, axs = plt.subplots(7,1,figsize=(8.5, 13), gridspec_kw={'height_ratios': [0.5,0.5,15,2, 2,15,4.5]})
        fig.text(0.9,0.04, '©2020, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha='right')
        ax_logo = fig.add_axes([.8,.868,.1*1.2,.1*1.2])
        ax_logo.imshow(self.logofcv)
        ax_logo.axis('off')
        ax_cinv = fig.add_axes([.05,.89,.25*0.9,.08*0.9])
        ax_sochi = fig.add_axes([.74,.9,.05*1.2,.05*1.2])
        ax_cinv.imshow(self.logos)
        ax_sochi.imshow(self.logo_sochimi)
        ax_cinv.axis('off')
        ax_sochi.axis('off')

        fig.text(.5, .88, 'Trayectoria de subreporte a nivel nacional', horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='x-large')

        ax_regions = {}
        ax_coordinates = {}

        axs[0].axis('off')
        axs[1].axis('off')
        axs[3].axis('off')
        axs[4].axis('off')
        #axs[4].axis('off')
        axs[6].axis('off')
        dates = pd.to_datetime(national_underrep['date']).strftime('%d-%m-%y')
        p_under, = axs[2].plot(dates, np.asarray(national_underrep['mean'])*100, color ='#006699')
        axs[2].fill_between(dates, np.asarray(national_underrep['low'])*100, np.asarray(national_underrep['high'])*100, alpha=.4, color ='#006699')
        axs[2].set_ylabel('% Subreporte')
        axs[2].set_ylim([0,100])
        axs[2].set_yticks(np.arange(0, 101, 10))
        axs[2].tick_params(axis='x',rotation=45)
        #plt.xticks(rotation=45)
        axs[2].tick_params(bottom=False, left=True, labelleft=True, labelbottom=True)
        axs[2].grid(axis='y')
        m, l, h, i = asp_national(national_underrep)
        pos = []
        for j, ind in enumerate(i):
            pos +=[dates.get_loc(ind)]
        ax2 = axs[2].twinx()
        ax2.set_ylabel('Infectados sintomáticos activos probables', color='black', fontsize = 7)
        p_act, = ax2.plot(pos,m,color='#df4d38')
        ax2.fill_between(pos, l, h, alpha=.4, color='#df4d38')
        ax2.set_yticks(np.arange(0, 300001, 30000))
        ax2.tick_params(axis='y', labelcolor='black')
        ax2.set_ylim(bottom =0)
        axs[1].legend([p_under, p_act],["Porcentaje de subreporte", "Casos activos probables"], bbox_to_anchor=(0.29,1.85), fontsize = 8)


        positivity = pcr_positivity_from_db() # take out
        dates = pd.to_datetime(positivity['Fecha'].values)
        dates = dates.strftime('%d-%m-%y')
        p2, = axs[5].plot(dates, 100*positivity['positividad pcr'].values, color='#f49819')
        p1, = axs[5].plot(dates, 100*positivity['mediamovil_positividad_pcr'].values, color='#000000')
        axs[5].set_ylabel('Positividad PCR %', color='black', fontsize = 7)
        pos = []
        axs[5].grid(axis='y')
        axs[5].set_yticks(np.arange(0, 101, 10))
        for j, ind in enumerate(i):
                pos +=[dates.get_loc(ind)]

        ax3 = axs[5].twinx()
        p3, = ax3.plot(pos, m, color='#df4d38')
        ax3.set_ylabel('Infectados sintomáticos activos probables', color='black', fontsize = 7)
        ax3.fill_between(pos, l, h, alpha=.4, color='#df4d38')
        ax3.set_yticks(np.arange(0, 300001, 30000))
        ax3.set_ylim(bottom = 0)
        axs[4].legend([p1, p2, p3],["Positividad PCR media movil 7 días", "Positividad PCR diaria", "Casos activos probables"], bbox_to_anchor=(0.37,0.75), fontsize = 8)
        axs[4].set_title('Casos activos probables y positividad diaria de exámenes PCR a nivel nacional',loc='center', weight = 'bold', fontsize = 8)

        axs[5].tick_params(axis='x',rotation=45)
        axs[5].tick_params(bottom=False, left=True, labelleft=True, labelbottom=True)

        if len(axs[2].xaxis.get_ticklabels())%2==0:
            every_nth = 14
        elif len(axs[2].xaxis.get_ticklabels())%2==1:
            every_nth = 14
        for n, label in enumerate(axs[2].xaxis.get_ticklabels()):
                if n % every_nth != 0:
                    label.set_visible(False)
        if len(axs[5].xaxis.get_ticklabels())%2==0:
            every_nth = 14
        elif len(axs[5].xaxis.get_ticklabels())%2==1:
            every_nth = 14
        for n, label in enumerate(axs[5].xaxis.get_ticklabels()):
                if n % every_nth != 0:
                    label.set_visible(False)

        #fig.tight_layout(h_pad = 0.1)
        # fig.subplots_adjust(hspace=.5, top = 0.84)
        filename = 'Report/Report_{}_national_underrep.pdf'.format(report_day.replace('/','_'))
        fig.savefig(self.pdf, format='pdf', dpi=1200)
        plt.savefig('subreporte.png', format = 'png', dpi = 600)
        pass

    def add_summary(self, reg_data, prevalencia_region, region_avg_rate, subr, R_reg,hs_occupation, report_date, national_prev, national_rate, national_underreporting, national_r):
        hospital_available = False
        UCI_available = True
        if hospital_available:
            _, camas_prev, camas_now = hs_occupation
        if UCI_available:
            UCI_prev, UCI_newest = load_uci_data()
        reg_dict = {''}
        first = reg_data[['Prevalencia', 'Tasa']].rename(index= {'Arica y Parinacota':'Arica', 'Aysén del General Carlos Ibáñez del Campo':'Aysén',
        'Biobío':'Bio-Bío',"Libertador General Bernardo O'Higgins":"O'Higgins", 'Magallanes y de la Antártica Chilena': 'Magallanes', 'Metropolitana de Santiago':'Metropolitana'})
        first['Región'] = first.index
        first['Región'] = first.index
        subrep_arrow = [subr['mean'][i][-1]-subr['mean'][i][-7] for i in subr.index]
        data_sub = [subr['mean'][i][-1] for i in subr.index]
        for j, item in enumerate(data_sub):
            if item < 0:
                data_sub[j] = 0
            elif item > 1:
                data_sub[j] = 1
        Subreporte = pd.DataFrame(data = data_sub,index= subr.index, columns = ['mean'])
        Subreporte = Subreporte.rename(index= {'Arica y Parinacota':'Arica', 'Aysén del General Carlos Ibáñez del Campo':'Aysén', 'Araucanía': 'La Araucanía',
        'Biobío':'Bio-Bío',"Libertador General Bernardo O'Higgins":"O'Higgins", 'Magallanes y de la Antártica Chilena': 'Magallanes', 'Metropolitana de Santiago':'Metropolitana'})

        #first['Subreporte'] = 1 - first['Subreporte']

        first['Subreporte'] = Subreporte
        first['Subreporte'] = first['Subreporte'].map('{:,.2%}'.format)
        first['Subreporte'] = first['Subreporte'].apply(lambda x: x.replace('nan%','ND'))

        R_reg.index.names = ["dates"]
        last_day = R_reg.index[-1]
        last_seven = list(R_reg.index[-7:])
        last_fourteen =list(R_reg.index[-14:])

        last_r = R_reg.loc[last_day]
        last_r = last_r.groupby(last_r.name).mean()
        last_r = last_r.rename(index= {'Arica y Parinacota':'Arica', 'Aysén del General Carlos Ibáñez del Campo':'Aysén', 'Araucanía': 'La Araucanía',
        'Biobío':'Bio-Bío',"Libertador General Bernardo O'Higgins":"O'Higgins", 'Magallanes y de la Antártica Chilena': 'Magallanes', 'Metropolitana de Santiago':'Metropolitana'})

        seven_r = R_reg.loc[last_seven]
        seven_r = seven_r.groupby(seven_r.name).mean()
        seven_r = seven_r.rename(index= {'Arica y Parinacota':'Arica', 'Aysén del General Carlos Ibáñez del Campo':'Aysén', 'Araucanía': 'La Araucanía',
        'Biobío':'Bio-Bío',"Libertador General Bernardo O'Higgins":"O'Higgins", 'Magallanes y de la Antártica Chilena': 'Magallanes', 'Metropolitana de Santiago':'Metropolitana'})

        fourteen_r = R_reg.loc[last_fourteen]
        fourteen_r = fourteen_r.groupby(fourteen_r.name).mean()
        fourteen_r = fourteen_r.rename(index= {'Arica y Parinacota':'Arica', 'Aysén del General Carlos Ibáñez del Campo':'Aysén', 'Araucanía': 'La Araucanía',
        'Biobío':'Bio-Bío',"Libertador General Bernardo O'Higgins":"O'Higgins", 'Magallanes y de la Antártica Chilena': 'Magallanes', 'Metropolitana de Santiago':'Metropolitana'})

        first['14 días'] = fourteen_r['MEAN'].map('{:,.2f}'.format)
        first['7 días'] = seven_r['MEAN'].map('{:,.2f}'.format)
        first['Último día'] = last_r['MEAN'].map('{:,.2f}'.format)
        first = first[['Región', 'Prevalencia', 'Tasa', 'Subreporte', '14 días', '7 días', 'Último día' ]]
        #first = first.apply(lambda x: x.str.replace('.',','))

        ########################################################################################
        fig = plt.figure(figsize=(11, 8.5))
        fig.text(0.95,0.06, '©2020, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha='right', fontsize=8)
        fig.text(0.0325, .900, 'Tabla resumen al '+report_date,
                 horizontalalignment='left', verticalalignment='center', weight = 'bold', fontsize='12')
        fig.text(0.0325,0.195, 'Flechas en prevalencia y uso de camas indican cambio respecto a reporte anterior \n'
                                +'Prevalencia infectados activos / 10.000 habitantes. Códigos colores: verdes \u2264 4; 4 <amarillo<5; rojo \u2265 5(Criterio OMS)\n'
                                +'Tasa promedio acumulada de nuevos infectados últimos 14 días. Código colores: verdes \u2264 25%; 25% <amarillo< 30%; rojo \u2265 5\n'
                                +'Subreporte infectados sintomáticos. Código colores según media de subreporte: verde = ND y 0; 1 <amarillo< 10; rojo \u2265 10\n'
                                +'Código colores uso de camas: verde(fuera de riesgo) \u2264 25%; 75% <amarillo(estable)\u2264 85%; 75% <naranja(saturación)\u2264 85%; rojo(colapso) > 95% \n',
                                 ha='left', fontsize=8)
        ########################################################################################
        if hospital_available or UCI_available:
            ax1_pos = [0.02, 0.0, 0.73, 0.9]
            ax2_pos = [0.525, 0.0, 0.14, 0.9]
        else:
            delta = 0.35
            ax1_pos = [0.02, 0.0, 0.73+delta, 0.9]
            ax2_pos = [0.525+delta*0.7, 0.0, 0.25, 0.9]

        ax1 = fig.add_axes(ax1_pos)
        ax1.set_axis_off()

        regions = ["Arica","Tarapacá","Antofagasta","Atacama",
                            "Coquimbo","Valparaíso","O'Higgins","Maule",
                            "Ñuble","Bio-Bío","La Araucanía","Los Ríos",
                            "Los Lagos","Aysén","Magallanes","Metropolitana", "Nacional"]
        first = first.reindex(regions)
        first = first.replace({"Arica":"(15) Arica","Tarapacá":"(01) Tarapacá","Antofagasta": "(02) Antofagasta","Atacama":"(03) Atacama",
                            "Coquimbo":"(04) Coquimbo","Valparaíso":"(05) Valparaíso","O'Higgins": "(06) O'Higgins","Maule": "(07) Maule",
                            "Ñuble":"(08) Ñuble","Bio-Bío":"(16) Bio-Bío","La Araucanía": "(09) La Araucanía","Los Ríos":"(14) Los Ríos",
                            "Los Lagos":"(10) Los Lagos","Aysén":"(11) Aysén","Magallanes":"(12) Magallanes","Metropolitana":"(13) Metropolitana"})
        data = np.ones((16,7))
        nacional = pd.DataFrame({'Región' :['(N) Nacional'],
        'Prevalencia': ['{:.2f}'.format(national_prev.T.values[-1][0]) ],
        'Tasa': [ '{:.2f}'.format(national_rate.values[-1]*100)+'%'],
        'Subreporte':['{:.2f}%'.format(national_underreporting['mean'][-1]*100)],
        '14 días': ['{:.2f}'.format(national_r['MEAN'][-14:].mean())],
        '7 días':['{:.2f}'.format(national_r['MEAN'][-7:].mean())],
        'Último día':['{:.2f}'.format(national_r['MEAN'].values[-1])]}, index = ['Nacional'])
        first =first.append(nacional)
        first.dropna(inplace=True)

        colLabels=['region', 'Camas Intermedio','Camas Intensivo','Número VMI','Pctes. Intermedio','Pctes. Intensivo','Pctes. VMI']
        table1 = ax1.table(
            cellText=first.values,
            fontsize=2,
            colLabels=first.columns,
            colWidths=[.130,.090,.090,.090,.090,.090,.090],
            cellColours=[['w', color_prvlnc_summary(float(first['Prevalencia'].iloc[c].replace(',','.'))),
                                color_rate_summary(float(first['Tasa'].iloc[c].replace(',','.')[:-1])/100),
                                color_underreporting_summary(first['Subreporte'].iloc[c].replace(',','.')[:-1]),
                                color_r0_summary(float(first['14 días'].iloc[c].replace(',','.'))),
                                color_r0_summary(float(first['7 días'].iloc[c].replace(',','.'))),
                                color_r0_summary(float(first['Último día'].iloc[c].replace(',','.'))) ] for c in range(17)],
            cellLoc='center',
            loc='upper left')
        table1.auto_set_font_size(False)
        table1.set_fontsize(7)

        cellDict1 = table1.get_celld()
        for i in range(0,len(colLabels)):
            cellDict1[(0,i)].set_height(.15)
            for j in range(1,len(data)+2):
                cellDict1[(j,i)].set_height(.03)
        for i in range(1,18):
            cellDict1[i,0].set_text_props(ha ='left')

        self._arrow_summary_1(prevalencia_region, region_avg_rate, national_prev, national_rate, subr, national_underreporting,ax1)
        ########################################################################################

        ax2 = fig.add_axes(ax2_pos)
        ax2.set_axis_off()
        ax2.annotate( 'Situación \nEpidemiológica', xy=(0.18,0.84),
                xycoords='axes fraction', ha='center', va='bottom',
                     fontweight = 'black',
                rotation=90, size=8)
        #for i in range 17 arrow_summary_1(first, second)
        table2 = ax2.table(
            cellText=[' ']*17,
            fontsize=2,
            #rowLabels=regions,
            colLabels=[' '],
            colWidths=[.111*2.5],

            cellColours=[[color_epi(float(first['14 días'].iloc[c].replace(',','.')),
                                    float(first['7 días'].iloc[c].replace(',','.')),
                                    float(first['Último día'].iloc[c].replace(',','.')))] for c in range(17)],
            cellLoc='center',
            loc='upper left')

        cellDict2 = table2.get_celld()
        for i in range(0,1):
            cellDict2[(0,i)].set_height(.15)
            cellDict2[(0,i)].set_linewidth(2)
            for j in range(1,len(data)+2):
                cellDict2[(j,i)].set_height(.03)
                cellDict2[(j,i)].set_linewidth(2)

        ########################################################################################
        if hospital_available:
            ax3 = fig.add_axes([0.595, 0.0, 0.50, 0.9])
            ax3.set_axis_off()
            self.arrow_summary_2(camas_prev, camas_now, ax3)
            camas_num = camas_now.copy()
            camas_now['Uso VMI'] =camas_now['Uso VMI'].map('{:,.2%}'.format)
            camas_now['Uso Intermedias'] =camas_now['Uso Intermedias'].map('{:,.2%}'.format)
            camas_now['Uso Intensivas'] =camas_now['Uso Intensivas'].map('{:,.2%}'.format)
            table3 = ax3.table(
                cellText=camas_now.values,
                fontsize= 10,
                rowLabels=  ['15','01', '02', '03', '04', '05', '06', '07', '08', '16', '09', '14', '10', '11', '12', '13'],
                colLabels=['UTI', 'UCI', 'VMI'],
                colWidths=[.100*2,.100*2,.100*2],
                cellColours=[[color_camas(camas_num['Uso Intermedias'].iloc[c]) ,
                              color_camas(camas_num['Uso Intensivas'].iloc[c]) ,
                              color_camas(camas_num['Uso VMI'].iloc[c] )] for c in range(16)],
                 #             'w','w']
                cellLoc='center',
                loc='upper left'
            )
            table3.auto_set_font_size(False)
            table3.set_fontsize(7)
            cellDict3 = table3.get_celld()
            for i in range(0,3):
                cellDict3[(0,i)].set_height(.15)
                for j in range(1,len(data)+1):
                    cellDict3[(j,i)].set_height(.03)
            for i in range(1,17):
                cellDict3[(i,-1)].set_height(.03)
            ########################################################################################

            ax4 = fig.add_axes([0.908, 0.0, 0.14, 0.9])
            ax4.set_axis_off()
            ax4.annotate(' Situación \nHospitalaría', xy=(0.2,0.855),

                xycoords='axes fraction', ha='center', va='bottom',
                fontweight = 'black',
                rotation=90, size=8)

            table4 = ax4.table(
                cellText=[' ']*16,
                fontsize=3,
                colLabels=[' '],
                colWidths=[.111*3],
                cellColours=[[color_hos_sit(camas_num['Uso Intermedias'].iloc[c],
                                            camas_num['Uso Intensivas'].iloc[c] ,
                                            camas_num['Uso VMI'].iloc[c]) ] for c in range(16)],
                cellLoc='center',
                loc='upper left')
            cellDict4 = table4.get_celld()
            for i in range(0,1):
                cellDict4[(0,i)].set_height(.15)
                cellDict4[(0,i)].set_linewidth(2)
                for j in range(1,len(data)+1):
                    cellDict4[(j,i)].set_height(.03)
                    cellDict4[(j,i)].set_linewidth(2)

        if UCI_available:
            ax3 = fig.add_axes([0.595, 0.0, 0.50, 0.9])
            ax3.set_axis_off()
            #arrow_summary_uci_2(UCI_prev, UCI_newest, ax3)
            # UCI_num = UCI_newest.copy() #numeric
            UCI_newest.loc['17']= UCI_newest.sum()
            table_values = pd.DataFrame(index = UCI_newest.index)
            table_values['per_covid'] = UCI_newest['occupied_covid']/UCI_newest['capacity']
            table_values['per_non_covid'] = UCI_newest['occupied_non_covid']/UCI_newest['capacity']
            table_values['per_total'] =  table_values['per_covid'] + table_values['per_non_covid']
            # table_values.loc['17'] =
            table_numeric = table_values.copy()
            table_values['per_covid'] = table_values['per_covid'].map('{:,.2%}'.format)
            table_values['per_non_covid'] = table_values['per_non_covid'].map('{:,.2%}'.format)
            table_values['per_total'] =  table_values['per_total'].map('{:,.2%}'.format)


            # UCI_newest['capacity'] = UCI_newest['capacity'].map('{:,.2%}'.format)
            # UCI_newest['occupied_covid'] = UCI_newest['occupied_covid'].map('{:,.2%}'.format)
            # UCI_newest['occupied_non_covid'] = UCI_newest['occupied_non_covid'].map('{:,.2%}'.format)

            table3 = ax3.table(
                cellText=table_values.values,
                fontsize= 10,
                rowLabels=  ['15','01', '02', '03', '04', '05', '06', '07', '08', '16', '09', '14', '10', '11', '12', '13', 'N'],
                colLabels=['Ocupación UCI\nPacientes Covid', 'Ocupación UCI\nPacientes no Covid', 'Ocupación total UCI'],
                colWidths=[.100*2,.100*2,.100*2],
                cellColours=[['white' ,
                              'white' ,
                              color_camas(table_numeric['per_total'].iloc[c] )] for c in range(17)],
                 #             'w','w']
                cellLoc='center',
                loc='upper left'
            )
            table3.auto_set_font_size(False)
            table3.set_fontsize(7)
            cellDict3 = table3.get_celld()
            for i in range(0,3):
                cellDict3[(0,i)].set_height(.15)
                for j in range(1,len(data)+2):
                    cellDict3[(j,i)].set_height(.03)
            for i in range(1,18):
                cellDict3[(i,-1)].set_height(.03)

        fig.savefig(self.pdf, format='pdf', dpi=1200)
        plt.savefig('summary.png', format = 'png', dpi = 600)
        pass

    def add_national_page(self, result, chile_avg_rate, chile_prvlnc, subrep, activos,report_day):
        logos = mpimg.imread('logos/uss_cinv_udd.png')
        logo_sochimi = mpimg.imread('logos/logo_sochimi.png')
        logo_fcv = mpimg.imread('logos/logos.png')
        logofcv = mpimg.imread('logos/logo_fcv.png')
        logofinis= mpimg.imread('logos/logo_finis.png')
        sns.set_context("paper", font_scale=.6)

        fig, axs = plt.subplots(6,1,figsize=(8.5, 13), gridspec_kw={'height_ratios': [4,15,0.1, 0.5,15,4.5]})

        #fig = plt.figure(figsize=(8.5, 11)) #(8.5, 11)
        fig.text(0.1,0.04, 'R_e calculado de acuerdo a Cori et al. (2019) https://doi.org/10.1016/j.epidem.2019.100356\nValor mostrado corresponde a promedio últimos 7 días (línea verde) y 14 días (línea violeta) respectivamente.\nDatos epidemiológicos https://github.com/MinCiencia/Datos-COVID19', ha='left')
        fig.text(0.9,0.04, '©2020, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha='right')
        ax_logo = fig.add_axes([.8,.868,.1*1.2,.1*1.2])
        ax_logo.imshow(logofcv)
        ax_logo.axis('off')
        ax_cinv = fig.add_axes([.05,.89,.25*0.9,.08*0.9])
        ax_sochi = fig.add_axes([.74,.9,.05*1.2,.05*1.2])
        ax_cinv.imshow(logos)
        ax_sochi.imshow(logo_sochimi)
        ax_cinv.axis('off')
        ax_sochi.axis('off')

        probables = (1-subrep['mean'][-1])
        if probables<0: probables = 0
        if probables>1: probables = 1
        probables_bajo =(1 -  subrep['low'][-1])
        if probables_bajo <0: probables_bajo = 0
        probables_alto =  (1 - subrep['high'][-1])
        if probables_alto>1: probables_alto = 1
        activos = int(activos)
        fig.text(.5, .9, 'Trayectoria de R_efectivo nacional a lo largo del tiempo \nPrevalencia País: {} / Tasa país: {}%\nEstimación de infectados sintomáticos detectados: {}% ({}% - {}%)\nInfectados activos: {} / Inf. Act. Probables: {} ~ {}'.format('{:.2f}'.format(chile_prvlnc.T.values[-1][0]).replace('.',','), '{:.2f}'.format(chile_avg_rate.values[-1]*100).replace('.',','), '{:.2f}'.format(probables*100).replace('.',','), '{:.2f}'.format(probables_bajo*100).replace('.',','), '{:.2f}'.format(probables_alto*100).replace('.',',') , '{:,}'.format(activos).replace(',','.'), '{:,}'.format(int(activos/probables_alto)).replace(',','.'),'{:,}'.format(int(activos/probables_bajo)).replace(',','.')), horizontalalignment='center', verticalalignment='center', weight = 'bold', fontsize='x-large')

        result.index = pd.to_datetime(result['Fecha'])

        ax_regions = {}
        ax_coordinates = {}

        axs[0].axis('off')

        axs[1].plot(result.index[1:], result['MEAN'][1:])
        axs[1].fill_between(result.index[1:],
                     result['Low_95'][1:], result['High_95'][1:], alpha=.4)
        # axs[1].set_title('Nacional')
        axs[1].hlines(result['MEAN'][-14:].mean(), result.iloc[-14].name,result.iloc[-1].name, color='C4')
        axs[1].hlines(result['MEAN'][-7:].mean(), result.iloc[-7].name,result.iloc[-1].name, color='C2')
        axs[1].hlines(1, result.iloc[1].name,result.iloc[-1].name, ls='--',color='k')
        axs[1].annotate('R_e 14d = {:.2f}'.format(result['MEAN'][-14:].mean()), (.8,.6), color='C4', xycoords='axes fraction')
        axs[1].annotate('R_e 7d = {:.2f}'.format(result['MEAN'][-7:].mean()), (.8,.56), color='C2', xycoords='axes fraction')
        axs[1].annotate('R_e inst. = {:.2f}'.format(result['MEAN'].values[-1]), (.8,.52), color='k', xycoords='axes fraction')
        axs[1].set_ylabel('R efectivo')
        axs[1].set_ylim([0.5,2.5])

        ticks = [result.index[1:][i]  for i in range(len(result.index[1:])) if i%14==0]
        ticks_labels = [result.index[1:][i].strftime("%d-%m-%y")  for i in range(len(result.index[1:])) if i%14==0]
        axs[1].set_xticks(ticks)
        axs[1].tick_params(axis='x',rotation=45)
        #plt.xticks(rotation=45)
        axs[1].set_xticklabels(ticks_labels, fontdict = {'fontsize' : '8'})
        ##data
        url_all_cases = 'http://192.168.2.223:5006/getTotalCasesAllComunas'
        url_active_cases = 'http://192.168.2.223:5006/getActiveCasesAllComunas'
        # data = pd.read_csv(url)
        endpoint_all = requests.get(url_all_cases)
        endpoint_active = requests.get(url_active_cases)

        data_all = json.loads(endpoint_all.text)
        data_active = json.loads(endpoint_active.text)
        all_data = pd.DataFrame(data_all['data'])
        active_data = pd.DataFrame(data_active['data'])
        con_cases = pd.DataFrame(index = pd.to_datetime(data_all['dates']).strftime('%d-%m-%y'))
        con_cases['total'] = all_data.sum(axis = 1).values

        act_cases = pd.DataFrame(index = pd.to_datetime(data_active['dates']).strftime('%d-%m-%y'))
        act_cases['total'] = active_data.sum(axis = 1).values
        #data
        axs[2].axis('off')

        color = 'red'
        axs[4].set_xlabel('Fecha')
        axs[4].set_ylabel('casos activos', color='black', fontsize = 7)
        p1, = axs[4].plot(act_cases,color=color , marker='o', markerfacecolor='white', markeredgecolor  = color, label='as')
        axs[4].tick_params(axis='y', labelcolor='black')

        ax2 = axs[4].twinx()  # instantiate a second axes that shares the same x-axis

        color = 'purple'
        ax2.set_ylabel('Casos confirmados', color='black', fontsize = 7)  # we already handled the x-label with ax1
        p2, = ax2.plot(con_cases[6:],color=color, marker='o', markerfacecolor='white', markeredgecolor  = color)
        ax2.tick_params(axis='y', labelcolor='black')

        axs[4].tick_params(axis='x',rotation=45)
        axs[4].tick_params(bottom=False, left=True, labelleft=True, labelbottom=True)
        if len(axs[4].xaxis.get_ticklabels())%2==0:
            every_nth = 3
        elif len(axs[4].xaxis.get_ticklabels())%2==1:
            every_nth = 4
        for n, label in enumerate(axs[4].xaxis.get_ticklabels()):
                if n % every_nth != 0:
                    label.set_visible(False)

          # otherwise the right y-label is slightly clipped
        #
        axs[3].axis('off')

        axs[3].legend([p1, p2],["Casos Activos", "Casos confirmados"], bbox_to_anchor=(0.21,0.3), fontsize = 8)#8)
        axs[3].set_title('Casos activos y confirmados a nivel nacional',loc='left', weight = 'bold', fontsize = 8)#8)

        for i, txt in enumerate(act_cases.values):
            if i%every_nth==0:
                axs[4].annotate(str("{:.1f}".format(int(txt)/1000))+'k', (p1.get_data()[0][i], p1.get_data()[1][i]+1000), fontsize=5,bbox=dict(boxstyle='square,pad=-0.1', fc='white', ec='none'), weight='bold', ha ='center')

        for i, txt in enumerate(con_cases[6:].values):
            if i%7==0:
                ax2.annotate(str("{:.1f}".format(int(txt)/1000))+'k', (p2.get_data()[0][i], p2.get_data()[1][i]+1000), fontsize=5,bbox=dict(boxstyle='square,pad=-0.1', fc='white', ec='none'), weight='bold', ha ='center')

        axs[5].axis('off')

        ####
        fig.tight_layout(h_pad = 0.1)
        # fig.subplots_adjust(hspace=.5, top = 0.84)
        filename = 'Report/Report_{}_RP18.pdf'.format(report_day.replace('/','_'))
        fig.savefig(self.pdf, format='pdf', dpi=1200)
        plt.savefig('nacional.png', format = 'png', dpi = 600)
        pass

    def end_pages(self):
        # closing pdf file
        self.pdf.close()
        # Compressing png files
        self.compress_pngs_pdf()

        pass

    def compress_pngs_pdf(self):
        files = ['reporte_'+self.date+'.pdf']#[file in os.listdir('./') if file.endswith('.png')]
        for file in os.listdir("./"):
            if file.endswith(".png"):
                files.append(file)
        zipobj = ZipFile('reporte_'+self.date+".zip", 'w')
        for png_files in files:
        	zipobj.write(png_files)
        zipobj.close()
        for png_files in files:
            os.remove(png_files)
        pass

    def _make_table(self, datos, values, total, total_values, ax, label=True):
        ax.set_axis_off()
        selection = datos.loc[values.sort_values(by=['Prevalencia','Tasa'], ascending=[False,False]).index]
        selection = pd.concat([selection, total], axis=0, join='outer')

        values = values.sort_values(by=['Prevalencia','Tasa'], ascending=[False,False]).values
        values = np.concatenate([values, total_values.values])
        values = values[:,:-2]




        if label:
            table = ax.table(
                cellText=selection.values,
                rowLabels=selection.index,
                colLabels=selection.columns,
                colWidths=[.125,.125,.075,.125,.175,.125,.1,.125],
                cellColours=[[color_prvlnc(c[0]), color_rate(c[1]), color_r0(c[2]),'w', 'w', 'w'] for c in values], #parche ,'w', color_dim(c[7])
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
        pass

    def _add_arrows(self, datos, muni_raw1, muni_raw2 ,weekly_prev1, weekly_prev2, R_arrow_past,R_arrow_last,death_rate1,death_rate2, ax, l_lim=0, h_lim=.9, x_t=.275, x_p=.075, x_r = 0.282 ,x_d = .6 ,x_m=.975, dx=.015, dy=.03): #faltan inputs
        selection = datos.loc[datos.sort_values(by=['Prevalencia','Tasa'], ascending=[False,False]).index].index
        y_ = np.linspace(h_lim, l_lim,len(selection))
        for y, comuna in enumerate(selection):
            all_comunas = get_comunas_name()
            com = all_comunas[all_comunas.index==comuna].county.values[0]
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
            movilidad = False
            if movilidad:
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
        pass

    @staticmethod
    def _generate_table(file):
        date = file[-9:]
        Tabla = pd.read_csv(file, index_col = "county_name")
        Tabla.columns = ['Prevalencia', 'Tasa %', 'R_e', 'Activos', 'Probables',
               'Mortalidad', 'Viajes', 'Movilidad']
        Tabla.drop('Movilidad', axis= 'columns', inplace = True)
        # Probables = Tabla['Probables'].copy()
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
        pass

    @staticmethod
    def _hospitales_reg():
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
        HEALTH_SERVICE_newest = HEALTH_SERVICE_newest[['Uso Intermedias','Uso Intensivas','Uso VMI']]
        HEALTH_SERVICE_prev = HEALTH_SERVICE_prev[['Uso Intermedias','Uso Intensivas','Uso VMI']]
        return days, HEALTH_SERVICE_prev, HEALTH_SERVICE_newest

    def _arrow_summary_1(self, prevalencia_region, region_avg_rate, national_prev, national_rate, subrep, subrep_nac,ax):

        first_column = prevalencia_region.rename(columns= {'Arica y Parinacota':'Arica', 'Aysén del General Carlos Ibáñez del Campo':'Aysén',
        'Biobío':'Bio-Bío',"Libertador General Bernardo O'Higgins":"O'Higgins", 'Magallanes y de la Antártica Chilena': 'Magallanes', 'Metropolitana de Santiago':'Metropolitana'})
        second_column = region_avg_rate.rename(columns= {'Arica y Parinacota':'Arica', 'Aysén del General Carlos Ibáñez del Campo':'Aysén',
        'Biobío':'Bio-Bío',"Libertador General Bernardo O'Higgins":"O'Higgins", 'Magallanes y de la Antártica Chilena': 'Magallanes', 'Metropolitana de Santiago':'Metropolitana'})
        first_column = first_column.loc[3]- first_column.loc[2]
        second_column = second_column.loc[3]- second_column.loc[2]

        regions = ["Arica","Tarapacá","Antofagasta","Atacama",
                            "Coquimbo","Valparaíso","O'Higgins","Maule",
                            "Ñuble","Bio-Bío","La Araucanía","Los Ríos",
                            "Los Lagos","Aysén","Magallanes","Metropolitana"]

        first_column = first_column.reindex(regions)
        second_column = second_column.reindex(regions)
        subrep = subrep.rename(index={'Arica y Parinacota':'Arica', 'Aysén del General Carlos Ibáñez del Campo':'Aysén',
        'Biobío':'Bio-Bío',"Libertador General Bernardo O'Higgins":"O'Higgins", 'Magallanes y de la Antártica Chilena': 'Magallanes',
        'Metrolitana de Santiago':'Metropolitana'})
        subrep = subrep.drop('Aysén')
        third_column = pd.DataFrame(data = [subrep['mean'][i][-1]-subrep['mean'][i][-7] for i in subrep.index],index= subrep.index, columns = ['mean'])
        third_column = pd.concat([third_column, pd.DataFrame(data = [0], index = ['Aysén'],    columns = ['mean'])])
        third_column = pd.concat([third_column, pd.DataFrame(data = [subrep_nac['mean'][-1]-subrep_nac['mean'][-7]], index = ['Nacional'], columns = ['mean'])])
        third_column = third_column.reindex(regions)

        #negativo =  bajando
        x_inter = 0.165
        y_ = np.linspace(0.802, 0.352-(0.802-0.352)/16, 17)
        dy = 0.025
        for region in range(16):
            if first_column[region]>0:
                ax.annotate("", xy=(x_inter, y_[region]+dy), xytext=(x_inter, y_[region]),
                    arrowprops=dict(facecolor='black', ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
            elif first_column[region]<0:
                ax.annotate("", xy=(x_inter, y_[region]), xytext=(x_inter, y_[region]+dy),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
            else:
                ax.annotate("", xy=(x_inter-0.002, y_[region]+0.012), xytext=(x_inter+0.002, y_[region]+0.012),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 0.5, width= 10.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')

            if second_column[region]>0:
                ax.annotate("", xy=(x_inter+0.088, y_[region]+dy), xytext=(x_inter+0.088, y_[region]),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
            elif second_column[region]<0:
                ax.annotate("", xy=(x_inter+0.088, y_[region]), xytext=(x_inter+0.088, y_[region]+dy),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
            else:
                ax.annotate("", xy=(x_inter-0.086, y_[region]+0.012), xytext=(x_inter+0.090, y_[region]+0.012),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 0.5, width= 10.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')

            if third_column.iloc[region]['mean']>0:
                ax.annotate("", xy=(x_inter+0.177, y_[region]+dy), xytext=(x_inter+0.177, y_[region]),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
            elif third_column.iloc[region]['mean']<0:
                ax.annotate("", xy=(x_inter+0.177, y_[region]), xytext=(x_inter+0.177, y_[region]+dy),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
            else:
                ax.annotate("", xy=(x_inter+0.175, y_[region]+0.012), xytext=(x_inter+0.179, y_[region]+0.012),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 0.5, width= 10.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')

        ##national
        if national_prev.T.values[-1][0] > national_prev.T.values[-2][0]: #hoy mas que ayer
            ax.annotate("", xy=(x_inter, y_[16]+dy), xytext=(x_inter, y_[16]),
                arrowprops=dict(facecolor='black', ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
        elif national_prev.T.values[-1][0]< national_prev.T.values[-2][0]:
            ax.annotate("", xy=(x_inter, y_[16]), xytext=(x_inter, y_[16]+dy),
                arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
        else:
            ax.annotate("", xy=(x_inter-0.002, y_[16]+0.012), xytext=(x_inter+0.002, y_[16]+0.012),
                arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 0.5, width= 10.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')

        if national_rate.values[-1]>national_rate.values[-2]:
            ax.annotate("", xy=(x_inter+0.088, y_[16]+dy), xytext=(x_inter+0.088, y_[16]),
                arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
        elif national_rate.values[-1]<national_rate.values[-2]:
            ax.annotate("", xy=(x_inter+0.088, y_[16]), xytext=(x_inter+0.088, y_[16]+dy),
                arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
        else:
            ax.annotate("", xy=(x_inter-0.086, y_[16]+0.012), xytext=(x_inter+0.090, y_[16]+0.012),
                arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 0.5, width= 10.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')

        if region in subrep.index and third_column.iloc[17]['mean']>0:
            ax.annotate("", xy=(x_inter+0.177, y_[16]+dy), xytext=(x_inter+0.177, y_[16]),
                arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
        elif region in subrep.index and third_column.iloc[17]['mean']<0:
            ax.annotate("", xy=(x_inter+0.177, y_[16]), xytext=(x_inter+0.177, y_[16]+dy),
                arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
        else:
            ax.annotate("", xy=(x_inter+0.175, y_[16]+0.012), xytext=(x_inter+0.179, y_[16]+0.012),
                arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 0.5, width= 10.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
        pass

    def _arrow_summary_2(self, camas_prev, camas_now, ax):

        third_column = camas_now['Uso VMI'] - camas_prev['Uso VMI']
        first_column = camas_now['Uso Intermedias'] - camas_prev['Uso Intermedias']
        second_column = camas_now['Uso Intensivas'] - camas_prev['Uso Intensivas']

        x_inter = 0.05
        y_ = np.linspace(0.802, 0.352, 16)
        dy = 0.025

        for region in range(16):
            if first_column[region]>0:
                ax.annotate("", xy=(x_inter, y_[region]+dy), xytext=(x_inter, y_[region]),
                    arrowprops=dict(facecolor='black', ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
            elif first_column[region]<0:
                ax.annotate("", xy=(x_inter, y_[region]), xytext=(x_inter, y_[region]+dy),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
            else:
                ax.annotate("", xy=(x_inter-0.007, y_[region]+0.012), xytext=(x_inter, y_[region]+0.012),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 0.5, width= 10.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')

            if second_column[region]>0:
                ax.annotate("", xy=(x_inter+0.195, y_[region]+dy), xytext=(x_inter+0.195, y_[region]),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
            elif second_column[region]<0:
                ax.annotate("", xy=(x_inter+0.195, y_[region]), xytext=(x_inter+0.195, y_[region]+dy),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')

            else:
                ax.annotate("", xy=(x_inter+0.188, y_[region]+0.012), xytext=(x_inter+0.195, y_[region]+0.012),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 0.5, width= 10.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')

            if third_column[region]>0:
                ax.annotate("", xy=(x_inter+0.395, y_[region]+dy), xytext=(x_inter+0.395, y_[region]),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
            elif third_column[region]<0:
                ax.annotate("", xy=(x_inter+0.395, y_[region]), xytext=(x_inter+0.395, y_[region]+dy),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 9.5, width= 3.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
            else:
                ax.annotate("", xy=(x_inter+0.388, y_[region]+0.012), xytext=(x_inter+0.395, y_[region]+0.012),
                    arrowprops=dict(facecolor='black',  ec='black',fc='darkgray' ,headlength = 5, headwidth = 0.5, width= 10.5, shrink=0.075),annotation_clip=False, xycoords='axes fraction')
        pass
