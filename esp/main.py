def web_page(conn):
    html = """
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
        body {
            text-align: center;
            font-family: "Trebuchet MS", Arial;
            background-color:#323232;
            color: lightgrey;
        }
        table {
            border-collapse: collapse;
            width: 35%;
            margin-left: auto;
            margin-right: auto;
        }
        th {
            padding: 12px;
            background-color: #0043af;
            color: white;
        }
        tr {
            border: 1px solid #ddd;
            padding: 12px;
        }
        tr:hover {
            background-color: #bcbcbc;
        }
        td {
            border: none;
            padding: 12px;
        }
        .sensor {
            color: white;
            font-weight: bold;
            padding: 1px;
        }
    </style>
</head>
<body>
    <h1>VivPi Sensors</h1>
    <table id="data"></table>


<script>
    async function refresh() {
        const table = document.querySelector('#data')
        const response = await fetch(`/res.json`)
        const json = await response.json()
  
        console.log(json)

        table.innerHTML = `
            <tr>
                <th>MEASUREMENT</th>
                <th>VALUE</th>
            </tr>
            <tr>
                <td>WarmTemperature</td>
                <td><span class="sensor warmTemperature">${json.warmTemperature}C</span></td>
            </tr>
            <tr>
                <td>WarmPressure</td>
                <td><span class="sensor warmPressure">${json.warmPressure}hPa</span></td>
            </tr>
            <tr>
                <td>WarmHumudity</td>
                <td><span class="sensor warmHumidity">${json.warmHumidity}%</span></td>
            </tr>
            <tr>
                <td>ColdTemperature</td>
                <td><span class="sensor coldTemperature">${json.coldTemperature}C</span></td>
            </tr>
            <tr>
                <td>ColdPressure</td>
                <td><span class="sensor coldPressure">${json.coldPressure}hPa</span></td>
            </tr>
            <tr>
                <td>ColdHumidity</td>
                <td><span class="sensor coldHumidity">${json.coldHumidity}%</span></td>
            </tr>
        `
        setTimeout(refresh, 5000)
    }
    refresh() 
</script>

</body>
</html>
"""
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    #conn.send('Content-Length: %s\n' % len(html))
    #conn.send('Connection: close\n\n')
    conn.sendall(html)
    conn.close()

def json(conn):  
    dict = {}
    if warmError = 0:
        dict['warmTemperature'] = float(warmSensor.temperature)
        dict['warmPressure'] = float(warmSensor.pressure)
        dict['warmHumidity'] = float(warmSensor.humidity)
    else:
        dict['warmTemperature'] = float(0)
        dict['warmPressure'] = float(0)
        dict['warmHumidity'] = float(0)
    if coldError = 0:
        dict['coldTemperature'] = float(coldSensor.temperature)
        dict['coldPressure'] = float(coldSensor.pressure)
        dict['coldHumidity'] = float(coldSensor.humidity)
    else:
        dict['coldTemperature'] = float(0)
        dict['coldPressure'] = float(0)
        dict['coldHumidity'] = float(0)
    json = ujson.dumps(dict)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: application/json\n\n')
    #conn.send('Content-Length: %s\n' % len(json))
    #conn.send('Connection: close\n\n')
    conn.sendall(json)
    conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

warmError = 0
coldError = 0

try:
    warmSensor = BME280.BME280(i2c=warmSens)
    print('Loaded warm sensor')
except:
    warmError = 1
    print('Warm sensor failed. Using bad data to alert')

try:
    coldSensor = BME280.BME280(i2c=coldSens)
    print('Loaded cold sensor')
except:
    coldError = 1
    print('Cold sensor failed. Using bad data to alert')

print('Server ready')
while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print(request)
    url = request.decode('utf-8').split(' ')[1]
    if url.endswith(".json"):
        json(conn)
    else:
        web_page(conn)
    conn.settimeout(None)
  except OSError as e:
    conn.close()
    print('Connection closed %s ' % e)

