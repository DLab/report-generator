from report_data_loader import last_data_day
from zipfile import ZipFile
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import os

day, report_day = last_data_day()

def plot_anexo_comunas(DataFrame, report_day):
    '''
    input: DataFrame = Re comunas
    '''
    day, month = report_day.split('/')
    logofcv = mpimg.imread('logos/logo_fcv.png')
    logos = mpimg.imread('logos/uss_cinv_udd.png')
    logo_sochimi = mpimg.imread('logos/logo_sochimi.png')
    logo_fcv = mpimg.imread('logos/logos.png')
    data = DataFrame
    data.index = pd.to_datetime(data['Fecha'])
    sns.set_context("paper", font_scale=.6)
    filenames = {}
    regiones_ = ['Arica y Parinacota',
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

    to_short_dict = {'Aysén del Gral. C. Ibáñez del Campo': 'Aysén', 'Magallanes y Antártica Chilena':'Magallanes',\
                     'Metropolitana de Santiago':'Metropolitana', "Lib. Gral. Bernardo O'Higgins":'O’Higgins', 'La Araucanía':'Araucanía'}
    DataFrame['region'].replace(to_short_dict, inplace = True)
    Anexos = []

    for r, region in enumerate(regiones_):
        Anexos.append(region + '_' + day + '_' + month + '.pdf')
        pdf = PdfPages(region + '_' + day + '_' + month + '.pdf')
        comunas_in_region = np.sort(data.comuna[data.region == region].unique())
        cc = 0 # Counting comunas already plotted or failed to plot
        filenames[region] = [] #Storing file names to unite them later
        zeros = 0

        for comuna in comunas_in_region:
            if np.sum(data[data.comuna == comuna]['MEAN'][1:]) == 0:
                zeros += 1
        apriori_files = len(comunas_in_region) - zeros
        total_pages = np.ceil(apriori_files / 8)

        for p, page in enumerate(range(int(total_pages))):
            fig = plt.figure(figsize = (8.5, 11))
            fig.text(0.1, 0.06, 'R_e calculado de acuerdo a Cori et al. (2019) https://doi.org/10.1016/j.epidem.2019.100356\nValor mostrado corresponde a promedio últimos 7 días (línea verde) y 14 días (línea violeta) respectivamente.\nDatos epidemiológicos https://github.com/MinCiencia/Datos-COVID19', ha = 'left')
            fig.text(0.9, 0.06, '©2022, Laboratorio de Biología Computacional, Fundación Ciencia & Vida', ha = 'right')

            ax_logo = fig.add_axes([.8, .875, .1, .1])
            ax_logo.imshow(logofcv)
            ax_logo.axis('off')
            ax_cinv = fig.add_axes([.06, .89, .25*0.8, .08*0.8])
            ax_sochi = fig.add_axes([.74, .9, .05, .05])
            ax_cinv.imshow(logos)
            ax_sochi.imshow(logo_sochimi)
            ax_cinv.axis('off')
            ax_sochi.axis('off')
            fig.text(.5, .935, 'Anexo {}: R efectivo región de {}'.format(r + 1, region),
                     horizontalalignment = 'center', verticalalignment = 'center', weight = 'bold', fontsize = 'x-large')

            i = 0
            while i < 8 : #Wait for 8 figures
                if cc >= apriori_files+zeros: break
                comuna = comunas_in_region[cc]
                datum = data[data.comuna == comuna]
                datum = datum.loc[~datum.index.duplicated(keep = 'first')]

                if np.sum(datum['MEAN'][1:]) == 0:
                    cc += 1
                    continue
                ax = fig.add_subplot(4, 2, i+1)

                ax.plot(datum['MEAN'][1:])
                ax.fill_between(datum.index[1:], datum['Low_95'][1:], datum['High_95'][1:], alpha = .4)
                ax.set_title(comuna)

                try:
                    if datum['MEAN'][-1] == 0:
                        ax.annotate('R_e = ND', (.7, .7), xycoords = 'axes fraction', color = 'k')
                    else:
                        ax.annotate('R_e inst. = {:.2f}'.format(datum['MEAN'][-1]), (.7, .6), xycoords = 'axes fraction', color = 'k')
                        if len(datum['MEAN']) > 6 :
                            ax.hlines(datum['MEAN'][-7:].mean(), datum.iloc[-7].name,datum.iloc[-1].name, color = 'C2')
                            ax.annotate('R_e 7d = {:.2f}'.format(datum['MEAN'][-7:].mean()), (.7, .7), xycoords = 'axes fraction', color = 'C2')
                        if len(datum['MEAN']) > 13 :
                            ax.hlines(datum['MEAN'][-14:].mean(), datum.iloc[-14].name,datum.iloc[-1].name, color = 'C4')
                            ax.annotate('R_e 14d = {:.2f}'.format(datum['MEAN'][-14:].mean()), (.7, .8), xycoords = 'axes fraction', color = 'C4')
                except:
                    pass
                ax.hlines(1, datum.iloc[1].name,datum.iloc[-1].name, ls = '--', color = 'k')

                ax.set_ylabel('R efectivo')
                ax.set_ylim([0,3])
                cc += 1
                i += 1

                ticks = [datum.index[1:][i]  for i in range(len(datum.index[1:])) if i%14==0]
                ticks_labels = [datum.index[1:][i].strftime("%d/%m")  for i in range(len(datum.index[1:])) if i%14==0]
                ax.set_xticks(ticks)
                plt.xticks(rotation = 45)
                ax.set_xticklabels(ticks_labels, fontdict = {'fontsize' : '6'})

            fig.autofmt_xdate()


            fig.subplots_adjust(hspace = .5)
            name_ = '{}_{}_RP{}.pdf'.format(region, report_day.replace('/','_'), p)
            #fig.savefig('Anexo/'+name_, dpi=1200)
            fig.savefig(pdf, format = 'pdf', dpi = 1200)
            #filenames[region].append('Anexo/'+name_)
            plt.close(fig)
        pdf.close()


    zipobj = ZipFile('Anexo_' + day + '_' + month + ".zip", 'w')

    for pdf in Anexos:
    	zipobj.write(pdf)
    zipobj.close()

    for pdf in Anexos:
        os.remove(pdf)
    pass
