
#!/bin/bash

# script "puente" para conectar el archivo api.py de gpu_api con la api de status apidemiologico

# nos situamos en el directorio correspondiente
cd /home/medusa/code/report-generator/epi_status/

# se desocupa el puerto 5001
fuser -k -n tcp 5001

# se reinicia la API con el nuevo reporte
export FLASK_APP=epi_status.py
nohup flask run --host=0.0.0.0 --port=5001 &