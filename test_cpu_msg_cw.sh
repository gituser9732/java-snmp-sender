#!/bin/sh
#
CDATE=`date +%s`
msg1='{"TimeStamp": 1548719033, "Source": "AWS/EC2", "SubCategory": "CPUUtilization", "Summary": "5 CPU Utilization - Reverse Test uid: b595df79-455f-41a1-b765-e3acdb2d34cd", "Detail": "Threshold Crossed: 1 datapoint was less than the threshold (10.0). @ [3.5593220339575 (28/01/19 23:41:00)]", "Region": "US West (Oregon)", "MonitorName": "usw2-mrm-pcrpt1-cpu.cw-alarm", "Severity": 5, "NodeAlias": "usw2-mrm-pcrpt1", "SupportGroup": "BIA"} '
msg1='{"TimeStamp": "{DDATE}", "Source": "AWS/EC2", "SubCategory": "CPUUtilization", "Summary": "5 CPU Utilization - Reverse Test uid: b595df79-455f-41a1-b765-e3acdb2d34cd", "Detail": "Threshold Crossed: 1 datapoint was less than the threshold (10.0). @ [3.5593220339575 (28/01/19 23:41:00)]", "Region": "US West (Oregon)", "MonitorName": "usw2-mrm-pcrpt1-cpu.cw-alarm", "Severity": 5, "NodeAlias": "usw2-mrm-pcrpt1", "SupportGroup": "BIA"} '

echo $msg1 | sed 's/"/\\"/g' |sed "s/{DDATE}/$CDATE/g"

