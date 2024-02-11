from flask import jsonify
import os, json, requests, logging, time
from pprint import pprint
from typing import Any

with open("/etc/monit/config.json") as f:
    config = json.load(f)

class Report: 
    def __init__(self, name: str, cpu: int, ram: int, disk: int, ports: str):
        self.name = name
        self.cpu = cpu
        self.ram = ram
        self.disk = disk
        self.ports = ports

    def __str__(self):
        return f""" {self.name} | ram : {self.ram} % | cpu : {self.cpu} % | disk : {self.disk} | ports : {self.ports}"""

    def push(self):
        
        file_path = os.path.join(config['rapport_dir'], self.name + '.rapport')
        with open(file_path, 'w') as rapport_file:
            json.dump({
                "name": self.name,
                "ram": self.ram,
                "cpu": self.cpu,
                "disk": self.disk,
                "ports": self.ports
            }, rapport_file)
            rapport_file.write('\n')

        return str(self)

