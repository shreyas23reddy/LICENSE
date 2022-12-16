import requests
import json
import yaml
import re
import time
import csv
import argparse
from datetime import datetime
import itertools


from auth_header import Authentication as auth
from operations import Operation
from license_class import getData
from license_class import postData
from query import queryPayload




if __name__=='__main__':

    while True:

        """ Adding cli via Arg parse """

        parser = argparse.ArgumentParser()

        parser.add_argument("-a","--address", help="vManage IP address")
        parser.add_argument("-p","--port", default=8443, help="vManage port")
        parser.add_argument("-u","--username", help="vManage username")
        parser.add_argument("-pw","--password", help="vManage password")



        subparser = parser.add_subparsers(dest='command',help="'all' - run script on all sites / 'sid' - run script on a specific site")

        """ 'all' will pull the detials from the all the sites in the overlay which are reachable
            'sid' will pull the detials from a specific site in the overlay """


        all = subparser.add_parser('all')
        sid = subparser.add_parser('sid')


        sid.add_argument('-id', type=str, required=True)


        args = parser.parse_args()

        vmanage_host = args.address
        vmanage_port = args.port
        username = args.username
        password = args.password


        """ GET the TOKEN from Authnetication call"""
        header= auth.get_header(vmanage_host, vmanage_port,username, password)


        """ """


        deviceInfo_data = {}

        now = datetime.now()

        if args.command == 'all':

            """
            To get the details of all the devices
             '/dataservice/device'
            """

            deviceInfo = getData.getDeviceIP(vmanage_host,vmanage_port,header)

            """
            iterate on the colleted info and create dict to collect information
            """

            for iter_deviceInfo in deviceInfo:

                """ check if the device is vedge add details to dictonary """

                if iter_deviceInfo["device-type"] == "vedge":
                    if iter_deviceInfo["site-id"] not in deviceInfo_data:
                        deviceInfo_data[iter_deviceInfo["site-id"]] = { "uuid":[],  "Aggregate" : 0,  "license Tier" : 'T0' }
                    if iter_deviceInfo["uuid"] not in deviceInfo_data[iter_deviceInfo["site-id"]]["uuid"]:
                        deviceInfo_data[iter_deviceInfo["site-id"]]["uuid"].append(iter_deviceInfo["uuid"])
                        deviceInfo_data[iter_deviceInfo["site-id"]][iter_deviceInfo["system-ip"]] = {}

                """
                if the device is reachable get WAN interfaces
                API '/dataservice/device/control/waninterface?deviceId='+str(deviceID)
                """

                if iter_deviceInfo["device-type"] == "vedge" and iter_deviceInfo["reachability"] == "reachable":
                    wanIFName = getData.getWANIfName(vmanage_host,vmanage_port,header,iter_deviceInfo["system-ip"])
                    print(f' Gathering the data from {iter_deviceInfo["uuid"]} - {iter_deviceInfo["system-ip"]} ')
                    cumBW = 0

                    """
                    if have a sub-interface strip the sub-interface tag
                    """

                    for iter_wanIFName in wanIFName:
                        TransportIfName = re.split(r"\.", iter_wanIFName["interface"])[0]
                        data = queryPayload.statsIFAgg(iter_deviceInfo["system-ip"] , TransportIfName)
                        time.sleep(2)

                        """
                        Get peak interface stats of a week which is aggegrated over 30 mins each
                        class queryPayload():
                            def statsIFAgg(systemIP, interface, duration = "168", interval = 30):
                        168 hours is 7 days
                        interval in mins
                        '/dataservice/statistics/interface/aggregation'
                        Aggregate TX + RX and pick the peak

                        """

                        interfaceStats = postData.getInterfaceStats(vmanage_host,vmanage_port,header,data)
                        maxagg = max(interfaceStats, key=lambda x: x["tx_kbps"]+ x["rx_kbps"])
                        deviceInfo_data[iter_deviceInfo["site-id"]][iter_deviceInfo["system-ip"]][TransportIfName] = maxagg["tx_kbps"]+maxagg["rx_kbps"]
                        cumBW += (maxagg["tx_kbps"]+maxagg["rx_kbps"])
                    deviceInfo_data[iter_deviceInfo["site-id"]]["Aggregate"] += cumBW





        elif args.command == 'sid':

            """
            To get the details of all the devices
             '/dataservice/device'
            """

            deviceInfo = getData.getDeviceIP(vmanage_host,vmanage_port,header)

            for iter_deviceInfo in deviceInfo:

                """
                check if the device is vedge add details to dictonary
                """

                if iter_deviceInfo["device-type"] == "vedge" and iter_deviceInfo["site-id"] == args.id :
                    if iter_deviceInfo["site-id"] not in deviceInfo_data:
                        deviceInfo_data[iter_deviceInfo["site-id"]] = { "uuid":[],  "Aggregate" : 0,  "license Tier" : 'T0' }
                    if iter_deviceInfo["uuid"] not in deviceInfo_data[iter_deviceInfo["site-id"]]["uuid"]:
                        deviceInfo_data[iter_deviceInfo["site-id"]]["uuid"].append(iter_deviceInfo["uuid"])
                        deviceInfo_data[iter_deviceInfo["site-id"]][iter_deviceInfo["system-ip"]] = {}

                """
                if the device is reachable get WAN interfaces
                API '/dataservice/device/control/waninterface?deviceId='+str(deviceID)
                """

                if (iter_deviceInfo["device-type"] == "vedge" and iter_deviceInfo["reachability"] == "reachable") and iter_deviceInfo["site-id"] == args.id:
                    wanIFName = getData.getWANIfName(vmanage_host,vmanage_port,header,iter_deviceInfo["system-ip"])
                    print(f' Gathering the data from {iter_deviceInfo["uuid"]} - {iter_deviceInfo["system-ip"]} ')
                    cumBW = 0


                    """
                    if have a sub-interface strip the sub-interface tag
                    """


                    for iter_wanIFName in wanIFName:
                        TransportIfName = re.split(r"\.", iter_wanIFName["interface"])[0]
                        data = queryPayload.statsIFAgg(iter_deviceInfo["system-ip"] , TransportIfName)
                        time.sleep(2)


                        """
                        Get peak interface stats of a week which is aggegrated over 30 mins each
                        class queryPayload():
                            def statsIFAgg(systemIP, interface, duration = "168", interval = 30):
                        168 hours is 7 days
                        interval in mins
                        '/dataservice/statistics/interface/aggregation'
                        Aggregate TX + RX and pick the peak
                        """


                        interfaceStats = postData.getInterfaceStats(vmanage_host,vmanage_port,header,data)
                        maxagg = max(interfaceStats, key=lambda x: x["tx_kbps"]+ x["rx_kbps"])
                        deviceInfo_data[iter_deviceInfo["site-id"]][iter_deviceInfo["system-ip"]][TransportIfName] = maxagg["tx_kbps"]+maxagg["rx_kbps"]
                        cumBW += (maxagg["tx_kbps"]+maxagg["rx_kbps"])
                    deviceInfo_data[iter_deviceInfo["site-id"]]["Aggregate"] += cumBW



        """ Calculate the LIcense tier based of
        https://www.cisco.com/c/en/us/products/collateral/software/one-wan-subscription/guide-c07-740642.html
        Bandwidth entitlement (Entitled throughput when selecting Bandwidth)
        """


        for iter_deviceInfo_data in deviceInfo_data:

            AggMbps = deviceInfo_data[iter_deviceInfo_data]["Aggregate"]/1000

            if AggMbps <= 50:
                deviceInfo_data[iter_deviceInfo_data]["license Tier"] = "T0"
            elif 50 < AggMbps <= 400:
                deviceInfo_data[iter_deviceInfo_data]["license Tier"] = "T1"
            elif 400 < AggMbps <= 2000:
                deviceInfo_data[iter_deviceInfo_data]["license Tier"] = "T2"
            elif 2000 < AggMbps <= 20000:
                deviceInfo_data[iter_deviceInfo_data]["license Tier"] = "T3"

        """
        Copying the DICT data to CSV
        """


        fields = [ 'Site-ID', 'uuid', 'Aggregate', 'license Tier' ]
        filename = f'license-{now.strftime("%m-%d-%Y_%H-%M-%S")}.csv'
        print(f"""
        Please view the {filename} for the license teir and aggregate info per site
        """)
        with open(filename,'w') as f:
            w = csv.DictWriter(f,fields)
            w.writeheader()
            for k in deviceInfo_data:
                w.writerow({field: deviceInfo_data[k].get(field) or k for field in fields})

        exit()
