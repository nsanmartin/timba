# use:
# $ source rav_historico.sh TICKER 

# curl -i -vvv -X POST \
#  https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos 
#  -d '{ especie: "AL30", fecha_inicio: "0000-00-00", fecha_fin: "2023-02-08" }' \
#      -H "Authorization: Bearer TOKEN "

# https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos
ENDPOINT="https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"
DATA='{ especie: "$1", fecha_inicio: "0000-00-00", fecha_fin: "2023-02-08" }'

TOKEN="access token here"


curl -X POST $ENDPOINT -d "$DATA" \
    -H "Authorization: Bearer $TOKEN"


