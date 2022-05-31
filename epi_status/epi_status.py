
"""
El módulo fitz viene del paquete PyMuPDF
Es importante instalarlo a través de pip, porque desde apt-get chocan los fitz.h
Las últimas versiones de PyMuPDF dan error.
La versión que sirve es PyMuPDF-1.16.14 (pip install PyMuPDF==1.16.14)
"""


from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
import datetime as dt
import fitz
import os
import glob

app = Flask(__name__)
CORS(app)

absPath = os.getcwd()
# print("absPath", absPath)
reportList = glob.glob("*.pdf")
# print("reportList", reportList)

# SE deja únicamente el reporte más reciente
if len(reportList) > 1:
    i = 0
    while i < (len(reportList) - 1):
        # print(reportList[i])
        os.remove(reportList[i])
        i += 1

pdf_doc = glob.glob("*.pdf")[0]
# print("pdf_doc", pdf_doc)

documento = fitz.open(pdf_doc)

@app.route("/epidemiologic_status", methods = ['GET'])
def epiStatus():

    page = documento.loadPage(2)
    text = page.getText("text")

    prevPais          = text.split("Prevalencia País: ")[1].split(" / Tasa país: ")
    tasaPais          = prevPais[1].split("\nEstimación de infectados sintomáticos detectados: ")
    infectDetected    = tasaPais[1].split(" (")
    infectDetected_r1 = infectDetected[1].split(" - ")
    infectDetected_r2 = infectDetected_r1[1].split(")\nInfectados activos: ")
    infectActive      = infectDetected_r2[1].split(" / Inf. Act. Probables: ")
    infActProb_r1     = infectActive[1].split(" ~ ")
    infActProb_r2     = infActProb_r1[1].split("\n")


    dict_tmp = {
        "national_prevalence": prevPais[0],
        "national_infection_rate": tasaPais[0],
        "active_infected": infectDetected[0],
        "symptomatic_infected": infectDetected_r1[0],
        "symptomatic_infected_lowRate": infectDetected_r2[0],
        "symptomatic_infected_hightRate": infectActive[0],
        "prob_active_infected_lowRate": infActProb_r1[0],
        "prob_active_infected_hightRate": infActProb_r2[0]
    }

    result = make_response(jsonify(dict_tmp))
    return result

if __name__ == '__main__':
      app.run(host = '0.0.0.0', port = 5001, debug = True)


