from flask import Flask, Response, render_template, request, send_from_directory, redirect, Response
import requests, json
from report_data_loader import *
from report_main import report_gen
from zipfile import ZipFile
from Anexo import *
from os import path
from random import random
from datetime import timedelta, datetime

app = Flask(__name__)

app.config["reportes"] ='/reports/'
app.config["anexos"] = '/reports/'
app.config["pngs"] = '/reports/'
# request.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    tasks = [web_report()]
    if request.method == 'GET':
        return render_template('index.html', tasks=tasks )

    elif request.method == 'POST':
        tasks[0].user_date = request.form['user_selection']
        return render_template('index.html', tasks=tasks)
    else:
        return render_template('index.html', tasks=tasks)


@app.route('/reportegenerator/<date>', methods=['GET', 'POST'])
def reporte_generator(date = None):
    #by default the last day
    if date is not None:
        if date == 'latest':
            day, month = report_date()[1].split('/')
            date = '2022-'+month+'-'+day
        else:
            year, month, day = date.split('-')
    else:
        month, day = date.split('_')
        date = None

    if request.method == 'POST':
        pass

    if request.method == 'GET':
        name = 'reporte_'+day+'_'+month+'.zip'
        if date == 'latest':
            report_gen(date)
            return send_from_directory(app.config["reportes"], filename=name, as_attachment=True)

        if path.exists('reporte_'+day+'_'+month+'.zip'):

            return send_from_directory(app.config["reportes"], filename=name, as_attachment=True)

        else:
            report_gen(date)
            return send_from_directory(app.config["reportes"], filename=name, as_attachment=True)
#a
@app.route('/Anexo/<date>', methods=['GET'])
def Anexo(date):
    if date is not None:
        if date == 'latest':
            day, month = report_date()[1].split('/')
            date = '2021-'+month+'-'+day
        else:
            year, month, day = date.split('_')
    else:
        month, day = date.split('_')
        date = None

    if request.method == 'GET':
        name = 'Anexo_'+day+'_'+month+'.zip'
        if date == 'latest':
            plot_anexo_comunas(r_comunas_db(), day+'/'+month)
            return send_from_directory(app.config["anexos"], filename=name, as_attachment=True)

        try:
            return send_from_directory(app.config["anexos"], filename=name, as_attachment=True)

        except:
            plot_anexo_comunas(r_comunas_db(), day+'/'+month)
            return send_from_directory(app.config["anexos"], filename=name, as_attachment=True)


class web_report(object):
    """docstring for web_report."""

    def __init__(self):
        super(web_report, self).__init__()
        self.r_date = self.r_date()
        self.s_date = self.beds_date()
        self.report_date = self.report_date()
        self.user_date = self.report_date.replace("_", "-") # hacer 2, uno con - y otro con _

    def r_date(self):
        endpoint_R = requests.get('http://192.168.2.223:5006/getNationalEffectiveReproduction' )
        R = json.loads(endpoint_R.text)
        date = R['dates'][-1].split('T')[0]
        return str(date).replace("-","/")

    def report_date(self):
        endpoint_R = requests.get('http://192.168.2.223:5006/getNationalEffectiveReproduction' )
        R = json.loads(endpoint_R.text)
        year, month, day = str(R['dates'][-1].split('T')[0]).split('-')
        date = datetime(int(year),int(month),int(day))
        date += timedelta(days=1)
        return str(date).split(' ')[0].replace("-","_")

    def beds_date(self):
        url = 'http://192.168.2.223:5006/getRegionalIcuBedOccupation'
        endpoint = requests.get(url)
        data = json.loads(endpoint.text)
        date = data['dates'][-1].split('T')[0]
        return str(date).replace("-","/")

# if __name__=='__main__':
#     app.run(host="192.168.1.81",port=5000)
