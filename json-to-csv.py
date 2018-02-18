import json
import csv
import re

python_obj = json.load(open('pred.json'))
with open('pred.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for time, [val] in python_obj:
        time = re.sub(r'(\d+)/(\d+)/(\d+) (\d+):(\d+)', 
                r'20\3-0\1-\2 \4:\5:00', time)
        writer.writerow([time, val])
