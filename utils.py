# _*_ coding: utf-8 _*_

import os


class HWMonitor(object):

    def __init__(self):
        # CPU information
        self.CPU_temp = self.get_CPU_temperature()
        # self.CPU_usage = self.get_CPU_usage()

        # RAM information
        RAM_stats = self.get_RAM_info()
        self.RAM_total = str(round(int(RAM_stats[0]) / 1024, 1)) + ' MB'
        self.RAM_used = str(round(int(RAM_stats[1]) / 1000, 1)) + ' MB'
        self.RAM_free = str(round(int(RAM_stats[2]) / 1000, 1)) + ' MB'

        # Disk information
        disk_stats = self.get_disk_space()
        self.disk_total = str(disk_stats[0]) + 'B'
        self.disk_used = str(disk_stats[1]) + 'B'
        self.disk_perc = str(disk_stats[3])

    @staticmethod
    def get_CPU_temperature():
        res = os.popen('vcgencmd measure_temp').readline()
        return (res.replace("temp=", "").replace("'C\n", ""))

    @staticmethod
    def get_RAM_info():
        p = os.popen('free')
        return p.readlines()[1].split()[1:4]

    @staticmethod
    def get_CPU_usage():
        return (str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))

    @staticmethod
    def get_disk_space():
        p = os.popen("df -h /")
        return p.readlines()[1].split()[1:5]
