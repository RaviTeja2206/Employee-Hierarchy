import json
import mysql.connector

from pandas import DataFrame
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database='1_1'
)

cursor = db.cursor(dictionary=True)
cursor.execute("""WITH RECURSIVE cte AS
(
  SELECT employee_id, concat(first_name,' ',last_name,' (',job_id,')') as employee_name, CAST(employee_id AS CHAR(200)) AS path, 0 as level
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT c.employee_id, concat(c.first_name,' ',c.last_name,' (',job_id,')'), CONCAT(cte.path, ",", c.employee_id), cte.level+1
  FROM employees c JOIN cte ON cte.employee_id=c.manager_id
)
SELECT * FROM cte ORDER BY path""")

result = cursor.fetchall()






az='  '
ar='└──'
aq='│   └──'

ax='├──'

ad='│'
dep=0
for x in result:
    #print(x)
    print()

    if x.get('level')>dep:
        
        print(az*(x.get('level')),ax,x.get('employee_name'))
        dep=x.get('level')
    elif x.get('level')<dep:
        dep=dep-2
        
        print(az*(x.get('level')),ax,x.get('employee_name'))
        dep=x.get('level')
    elif x.get('level')==0:
        print(x.get('employee_name'))
        dep=x.get('level')
    else:
        dep=dep-1
        print(az*(x.get('level')),ax,x.get('employee_name'))





