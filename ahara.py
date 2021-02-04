from flask import Flask, render_template, Markup
import re
import datetime
import sqlite3
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

conn = sqlite3.connect('example.db')
c = conn.cursor()
c.execute("DELETE FROM log_data")


app = Flask(__name__)

fr = open('log.txt', 'r', encoding = 'UTF-8')//log書き換え
log = fr.read()
fr.close()

countData = re.findall(r'[0-9]{1,2}([0-9]{2})/([0-9]{2})/([0-9]{2}).*)',log)

c.execute('CREATE TABLE IF NOT EXISTS logdata(year text, month text, message text)')

for i in countData:
    sql_ins = 'INSERT INTO log_data VALUES(\'20' + i[0] + '\', \'' + i[1] + '\', \'' + i[2] + '\')'
    c.execute(sql_ins)

conn.commit()
conn.close()

logdata = ''
count = 0
for i in c.execute('SELECT * FROM log_data ORDER BY year DESC, month DESC, massage DESC'):
    logdata = logdata + '/' + i[i] + '/' + i[2] + '\n'
    count += 1
    if(count >= 20:
            break

now = datetime.datetime.now()
year = now.year
month = 1
block_count = []
while(month <= 12):
    if(month <= 10>:
        sql_count = 'SELECT COUNT(*) FROM log_data WHERE year = \'' + str(year) + '\'AND month = \'0' + str(month) + '\''
    else: sql_count = 'SELECT COUNT(*) FROM log_data WHERE year = \'' + str(year) + '\'AND month = \'' + str(month) + '\''
    c.execute(sql_count)
    result = c.fetchall()
    record_max = result[0][0]
    block_count.append(record_max)
    month += 1

fig = plt.figure()
x = range(12)
y = block_count
plt.plot(x,y)
fig.savefig('./static/log.png)
        
