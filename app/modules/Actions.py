import psutil, socket, json, os
import logging, time, requests, datetime
from classes.Report import Report

with open("/etc/monit/config.json") as f:
    config = json.load(f)

UserSystem = {
    "cpu": psutil.cpu_percent(interval=1, percpu=True),
    "ram": psutil.virtual_memory()[2],
    "disk": psutil.disk_usage('/')[3],
    "ports": ', '.join(map(str, [p for p in config['ports'] if not socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(('localhost', p))]))
}

def getAllInfos():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    report_name = f'monit-{timestamp}'
    if config['local_api_mode'] == True :
        requests.post('http://localhost:8085/api/data/post', json=Report(report_name, UserSystem['cpu'], UserSystem['ram'], UserSystem['disk'], UserSystem['ports']).__dict__)
        return Report(report_name, UserSystem['cpu'], UserSystem['ram'], UserSystem['disk'], UserSystem['ports']).push()
    else:
        return Report(report_name, UserSystem['cpu'], UserSystem['ram'], UserSystem['disk'], UserSystem['ports']).push()

def listReports():
    reports = []
    print('to access reports, go to /var/monit/reports/ \n')
    files_sorted = sorted(os.listdir(config['rapport_dir']), key=lambda f: os.path.getctime(os.path.join(config['rapport_dir'], f)), reverse=True)

    for filename in files_sorted:
       reports.append(filename)
       
    return reports

def getLastReport():
    print('to access reports, go to /var/monit/reports/ \n')
    latest_report = None
    latest_creation_time = 0
    for filename in os.listdir(config['rapport_dir']):
        file_path = os.path.join(config['rapport_dir'], filename)
        creation_time = os.path.getctime(file_path)
        if creation_time > latest_creation_time:
            latest_creation_time = creation_time
            latest_report = filename
    
    if latest_report:
        with open(os.path.join(config['rapport_dir'], latest_report), 'r') as file:
            report_content = file.read()
            print(report_content)
    else:
        print("No reports available.")

        
def isWithinLastHours(report_id, last_x_hours):
    report_file = os.path.join('/var/monit/reports/', report_id)
    with open(report_file, "r") as report_file:
        report_data = json.load(report_file)

    if "name" in report_data:
        report_name = report_data['name']
        report_time = datetime.datetime.strptime(report_name.split('-', 1)[1], "%Y%m%d-%H%M%S")
        time_difference = datetime.datetime.now() - report_time

        return time_difference.total_seconds() / 3600 <= last_x_hours
    else:
        logging.warning("Report %s does not contain a timestamp.", report_id)
        return False

import psutil

def getAverage(last_x_hours):
    reports = listReports()
    recent_reports = [
        report_id for report_id in reports if isWithinLastHours(report_id, last_x_hours)
    ]

    if recent_reports:
        total_reports = len(recent_reports)
        num_cores = len(psutil.cpu_percent(interval=1, percpu=True))
        cpu_percent_data = [0] * num_cores
        sum_ram = sum_disk = 0

        for report_id in recent_reports:
            report_file = os.path.join(config['rapport_dir'], report_id)
            with open(report_file, "r") as report_file:
                report_data = json.load(report_file)

            cpu_values = report_data["cpu"]
            for i, core_value in enumerate(cpu_values):
                cpu_percent_data[i] += core_value

            sum_ram += report_data["ram"]
            sum_disk += report_data["disk"]

            rounded_cpu_percent_data = [round(core_total / total_reports, 1) for core_total in cpu_percent_data]

        average_report = {
            "cpu": rounded_cpu_percent_data,
            "ram": round(sum_ram / total_reports, 1),
            "disk": round(sum_disk / total_reports, 1)
        }

        logging.info("Calculated the average report for the last %d hours.", last_x_hours)
        print(average_report)  
        return average_report
    else:
        logging.warning("No reports available in the specified time range.")
        return None