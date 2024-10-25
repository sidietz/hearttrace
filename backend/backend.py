import time
import psycopg

from statistics import fmean
from datetime import datetime
from collections import OrderedDict
from flask_cors import cross_origin
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hearttrace:N0m1596.@127.0.0.1/hearttrace'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

AREA_DICT = {0: "Ansbach", 1: "Potsdam", 2: "Aachen", 3:"Annaberg-Buchholz", 4: "Hamburg", 5: "Stuttgart"}

def get_db_connection():
    conn = psycopg.connect(host='localhost',
                            dbname='hearttrace',
                            user='hearttrace',
                            password='N0m1596.')
    return conn

'''
def select_fuel_from_row(fuel_type, row):
    date, group, diesel, e5, e10 = row

    if fuel_type == 'diesel':
        return [date, group, diesel]
    elif fuel_type == 'e5':
        return [date, group, e5]
    elif fuel_type == 'e10':
        return [date, group, e10]
    else:
        return [0, 0, 0]
'''
'''
def adjust_to_charts_day(raw_data, fuel_type='e5'):

    c3_columns = [[], [], [], [], [], []]
    first_column = ['x']

    for row in raw_data:
        # date, group, diesel, fuel, e10 = row
        date, group, fuel = select_fuel_from_row(fuel_type, row)
        if group == 0:
            first_column.append(date.strftime("%Y-%m-%d"))

        c3_columns[group].append(round(fuel, 5))
    
    for idx, groups in enumerate(c3_columns):
        groups.insert(0, AREA_DICT[idx])
    
    c3_columns.insert(0, first_column)

    return {'data': {'x': 'x', 'columns': c3_columns}}
'''


def adjust_to_charts_week_range(raw_data):

    c3_columns = [['x'], ['sys'], ['dia'], ['hr']]
    stmps = ['x']
    syss = ['sys']
    dias = ['dia']
    hrs = ['rate']
    deepdias = []
    deepsyss = []
    deephrs = []
    #first_column = ['x']

    stmps_dict = {}

    laststmp = 0

    j = -1

    for i, row in enumerate(raw_data):
        _, stmp, dia, sys, hr = row
        stmps.append(stmp)

        if stmp in stmps_dict:
            deepdias[j].append(dia)
            deepsyss[j].append(sys)
            deephrs[j].append(hr)
        else:
            stmps_dict[stmp] = j
            deepdias.append([dia])
            deepsyss.append([sys])
            deephrs.append([hr])
            j += 1

    for i, elem in enumerate(deepdias):

        maxd = max(elem)
        mind = min(elem)
        midd = elem[0]

        dias.append({'high': maxd, 'mid': midd, 'low': mind})

    for i, elem in enumerate(deepsyss):

        maxd = max(elem)
        mind = min(elem)
        midd = elem[0]

        syss.append({'high': maxd, 'mid': midd, 'low': mind})

    for i, elem in enumerate(deephrs):

        maxd = max(elem)
        mind = min(elem)
        midd = elem[0]

        hrs.append({'high': maxd, 'mid': midd, 'low': mind})


        #c3_columns[0].append(str(i))
        #dias.append(dia)
        #syss.append(sys)
        #hrs.append(hr)

    
    c3_columns = [stmps, syss, dias, hrs]
    #print(c3_columns)

    return {'data': {'x': 'x', 'columns': c3_columns, 'type': "area-spline-range" }}

def convTobb(adict):
    stmps = ['x']
    syss = ['sys']
    dias = ['dia']
    hrs = ['rate']
    
    for key, val in adict.items():
        tmpsys = []
        tmpdia = []
        tmprate = []
        for e in val:
            tmpsys.append(e[0])
            tmpdia.append(e[1])
            tmprate.append(e[2])
        stmps.append(key)
        syss.append({"high": max(tmpsys), "low": min(tmpsys), "mid": int(fmean(tmpsys))})
        dias.append({"high": max(tmpdia), "low": min(tmpdia), "mid": int(fmean(tmpdia))})
        hrs.append({"high": max(tmprate), "low": min(tmprate), "mid": int(fmean(tmprate))})
            
    resDict = [stmps, syss, dias, hrs]
    #print(resDict)
    return resDict

def adjust_to_charts_week_range2(raw_data):
    
    tmpD = OrderedDict()

    for i, elem in enumerate(raw_data):
        date = datetime.strptime(elem[1].strftime("%Y-%m-%d"), "%Y-%m-%d")
        if date in tmpD:
            try:
                testarr = tmpD[date]
                testarr.append([elem[2], elem[3], elem[4]])
            except ValueError:
                print("error")
        else:
            tmpD[date] = [[elem[2], elem[3], elem[4]]]
            
        #print(date)

    c3_columns = convTobb(tmpD)

    return {'data': {'x': 'x', 'columns': c3_columns, 'type': "area-spline-range" }}

def adjust_to_charts_week(raw_data, fuel_type='e5'):

    c3_columns = [['x'], ['dia'], ['sys'], ['hr']]
    stmps = ['x']
    syss = ['sys']
    dias = ['dia']
    hrs = ['rate']
    #first_column = ['x']

    for i, row in enumerate(raw_data):
        _, stmp, dia, sys, hr = row
        stmps.append(stmp)
        #c3_columns[0].append(str(i))
        dias.append(dia)
        syss.append(sys)
        hrs.append(hr)
    
    c3_columns = [stmps, syss, dias, hrs]

    data = c3_columns

    return {'data': {'x': 'x', 'columns': c3_columns}}


def adjust_to_rows(raw_data):

    data = []
    for row in raw_data:
        #Tue, 14 Oct 2024 00:00:00 GMT
        # datetime.strftime(

        #raise ValueError(row[1])

        try:
            data.append([row[0], datetime.strftime(datetime.strptime(str(row[1]), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"), row[2], row[3], row[4]])
        except ValueError:
            data.append([row[0], datetime.strftime(datetime.strptime(str(row[1]), "%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S"), row[2], row[3], row[4]])


    return data

'''
    for row in raw_data:
        date, dia, sys, heart_rate = row
        if group == 0:
            first_column.append(date)

        c3_columns[group].append(round(fuel, 5))
    
    #for idx, groups in enumerate(c3_columns):
    #    groups.insert(0, AREA_DICT[idx])
    
    c3_columns.insert(0, first_column)

    return {'data': {'x': 'x', 'columns': c3_columns}}
'''

def executeSelectSql(sql_query, formatter_method):

    sql_query = sql_query
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql_query)
    rows = cur.fetchall()
    data = formatter_method(rows)
    cur.close()
    conn.close()

    return data

def executeInsertSql(sql_query):

    sql_query = sql_query
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(sql_query)
    conn.commit()

@app.route('/v1/add/hearttrace', methods = ['POST'])
def add_hearttrace():
    if request.method == 'POST':
        data = request.json
        dia = data.get('dia')
        sys = data.get('sys')
        rate = data.get('rate')
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        data['time'] = time
        sql_query = "INSERT INTO hearttrace(id, date, dia, sys, heart_rate) VALUES (DEFAULT, " + "now()" + ", " + dia + ", " + sys + "," + rate + ");"
        executeInsertSql(sql_query)
        return data
    else:
        return None
    

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/time')
@cross_origin()
def get_current_time():
    return {'time': time.time()}

@app.route('/api/charts/day')
@cross_origin()
def get_charts_day():
    sql_query = "SELECT hearttrace.id, hearttrace.date::date, hearttrace.sys, hearttrace.dia, hearttrace.heart_rate FROM hearttrace;"
    data = executeSelectSql(sql_query, adjust_to_charts_week)

    return data

@app.route('/api/charts/day_range')
@cross_origin()
def get_charts_day_range():
    sql_query = "SELECT hearttrace.id, hearttrace.date::date, hearttrace.sys, hearttrace.dia, hearttrace.heart_rate FROM hearttrace;"
    data = executeSelectSql(sql_query, adjust_to_charts_week_range2)

    return data

@app.route('/api/allrows')
@cross_origin()
def get_allrows():
    sql_query = "SELECT hearttrace.id, hearttrace.date::timestamp, hearttrace.sys, hearttrace.dia, hearttrace.heart_rate FROM hearttrace;"
    data = executeSelectSql(sql_query, adjust_to_rows)

    return data

'''

@app.route('/charts/day/<fuel_type>')
@cross_origin()
def get_charts_day_fuel_selection(fuel_type):
    sql_query = "SELECT prices.changed_at::date, stations.area, avg(diesel) as diesel_avg, avg(e5) as avg_5, avg(e10) as avg_e10 from prices, stations WHERE prices.station_id = stations.station_id GROUP BY prices.changed_at::date, stations.area;"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql_query)
    prices = cur.fetchall()
    data = adjust_to_charts_day(prices, fuel_type)
    cur.close()
    conn.close()

    return data

@app.route('/charts/week/<fuel_type>')
@cross_origin()
def get_charts_week_fuel_selection(fuel_type):
    sql_query = "SELECT extract(week from prices.changed_at::date) as KW, stations.area, avg(diesel) as diesel_avg, avg(e5) as e5_avg, avg(e10) as e10_avg FROM prices, stations WHERE prices.station_id = stations.station_id GROUP BY KW, stations.area;"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql_query)
    prices = cur.fetchall()
    data = adjust_to_charts_week(prices, fuel_type)
    cur.close()
    conn.close()

    return data

@app.route('/charts/day')
@cross_origin()
def get_charts_day():
    sql_query = "SELECT prices.changed_at::date, stations.area, avg(diesel) as diesel_avg, avg(e5) as avg_5, avg(e10) as avg_e10 from prices, stations WHERE prices.station_id = stations.station_id GROUP BY prices.changed_at::date, stations.area;"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql_query)
    prices = cur.fetchall()
    data = adjust_to_charts_day(prices)
    cur.close()
    conn.close()

    return data

@app.route('/charts/week')
@cross_origin()
def get_charts_week():
    sql_query = "SELECT extract(week from prices.changed_at::date) as KW, stations.area, avg(diesel) as diesel_avg, avg(e5) as e5_avg, avg(e10) as e10_avg FROM prices, stations WHERE prices.station_id = stations.station_id GROUP BY KW, stations.area;"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql_query)
    prices = cur.fetchall()
    data = adjust_to_charts_week(prices)
    cur.close()
    conn.close()

    return data


@app.route('/week')
@cross_origin()
def get_weekly():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT extract(week from changed_at::date) as KW, avg(diesel) as diesel_avg, avg(e5) as e5_avg, avg(e10) as e10_avg FROM prices GROUP BY KW ORDER BY KW;")
    prices = cur.fetchall()
    cur.close()
    conn.close()

    return {'prices': [{'date': i[0], 'diesel': f'{i[1]:.5f}', 'e5': f'{i[2]:.5f}', 'e10': f'{i[3]:.5f}'} for i in prices]}


@app.route('/day')
@cross_origin()
def get_day():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("select changed_at::date as date, avg(diesel) as diesel_avg, avg(e5) as e5_avg, avg(e10) as e10_avg FROM prices GROUP BY date ORDER BY date;")
    prices = cur.fetchall()
    cur.close()
    conn.close()

    return {'prices': [{'date': i[0].strftime("%d.%m.%Y"), 'diesel': f'{i[1]:.5f}', 'e5': f'{i[2]:.5f}', 'e10': f'{i[3]:.5f}'} for i in prices]}


@app.route('/area/<area_number>/week')
@cross_origin()
def get_area_by_week(area_number):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT extract(week from changed_at::date) as KW, avg(diesel) as diesel_avg, avg(e5) as e5_avg, avg(e10) as e10_avg FROM (SELECT * FROM prices, stations WHERE prices.station_id = stations.station_id AND stations.area = %s) as prices_table GROUP BY KW ORDER BY KW;", (area_number))
    prices = cur.fetchall()
    cur.close()
    conn.close()

    return {'prices': [{'date': i[0], 'diesel': f'{i[1]:.5f}', 'e5': f'{i[2]:.5f}', 'e10': f'{i[3]:.5f}'} for i in prices]}


@app.route('/area/<area_number>/day')
@cross_origin()
def get_area_by_day(area_number):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT changed_at::date as date, AVG(diesel) as diesel_avg, AVG(e5) as e5_avg, AVG(e10) as e10_avg FROM (SELECT * FROM prices, stations WHERE prices.station_id = stations.station_id AND stations.area = %s) as prices_table GROUP BY date ORDER BY date;", (area_number))
    prices = cur.fetchall()
    cur.close()
    conn.close()

    return {'prices': [{'date': i[0].strftime("%d.%m.%Y"), 'diesel': f'{i[1]:.5f}', 'e5': f'{i[2]:.5f}', 'e10': f'{i[3]:.5f}'} for i in prices]}

'''


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=1024, debug=True)
