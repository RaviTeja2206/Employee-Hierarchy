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



PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX2 = "│   "
PIPE_PREFIX = "│"
SPACE_PREFIX = "    "	



dep=0
h=''
for x in result:

    if x.get('level')==0:
        h=f"{SPACE_PREFIX*x.get('level')}{x.get('employee_name')}"
        
        dep=x.get('level')
    elif x.get('level')>dep:
        if dep>=2:
            
            for i in range(1,dep):
                
                h=h[:len(SPACE_PREFIX)*i]+PIPE_PREFIX+h[len(SPACE_PREFIX)*i+1:]
        
        h=h.replace(TEE,ELBOW)
        print(h)
        h=f"{SPACE_PREFIX*x.get('level')}{TEE}{x.get('employee_name')}"
        
        dep=x.get('level')
    elif x.get('level')<dep:
        if dep>=2:
          
            
            for i in range(1,dep-(dep-x.get('level'))+1):
                
                h=h[:len(SPACE_PREFIX)*i]+PIPE_PREFIX+h[len(SPACE_PREFIX)*i+1:]
        h=h.replace(TEE,ELBOW)
        print(h)
        h=f"{SPACE_PREFIX*x.get('level')}{TEE}{x.get('employee_name')}"
        dep=x.get('level')
    elif x.get('level')==dep:
        if dep>=2:
            
            for i in range(1,dep):
                
                h=h[:len(SPACE_PREFIX)*i]+PIPE_PREFIX+h[len(SPACE_PREFIX)*i+1:]
        print(h)
        h=f"{SPACE_PREFIX*x.get('level')}{TEE}{x.get('employee_name')}"
        dep=x.get('level')
        
    else:
        pass
h=h.replace(TEE,ELBOW)
print(h)
    



