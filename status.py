import GPUtil as gputil
import psutil
import datetime
import argparse
import psycopg2

db_params = {
    "host": "****",
    "database": "****",
    "user": "****",
    "password": "****",
}

def connect(params_dic):
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(end=" ")
    #print("Connection successful PostgreSQL")
    return conn

def getStatus(mall):
    res = dict()
    gpu = gputil.getGPUs()
    
    res["id_cc"] = mall
    res["cpu_usage"] = f"{psutil.cpu_percent(interval=None)}%"
    res["cpu_memory"] = f"{round(psutil.virtual_memory().used/(1024**3))}GiB"
    res["disk_free"] = f"{round(psutil.disk_usage('/').free/(1024**3))}GiB"

    for item in gpu:
        res["gpu_usage"] = f"{round(item.load*100)}%"
        res["gpu_memory"] = f"{round(item.memoryUsed)}MiB"
        res["gpu_temp"] = f"{item.temperature}C"
    res["fecha"] = getTimestamp()
    res["hora"] = getTimestamp(False)

    return res

def getTimestamp(date=True):
    if date:
        return datetime.datetime.now().strftime("%d-%m-%Y")
    return datetime.datetime.now().strftime("%H:%M:%S")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Report server status in postgreSQL database ')
    parser.add_argument('-m', '--id_cc', type=str, required=True, help='id of mall to report')

    args = parser.parse_args()

    status = getStatus(args.id_cc)   

    query = "INSERT INTO estado_server(id_cc, uso_cpu, ram_cpu, espacio_en_disco, uso_gpu, ram_gpu, temperatura_gpu, fecha, hora) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    try:
        conn = connect(db_params)
        if conn is None:
            raise ValueError('Error when trying to connect to the DB ...')
        cur = conn.cursor()
        cur.execute(query, tuple(status.values()))
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()

