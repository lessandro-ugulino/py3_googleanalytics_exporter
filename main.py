#!/usr/bin/env python3

# import packages
from apiclient.discovery import build
from google.oauth2.service_account import Credentials
import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import os

KEY_FILE_LOCATION = '/app/ga_creds.json'
metrics = ['ga:sessions'] # metrics & dimensions
PUSHGWIP = os.environ['PUSHGWIP']
VIEW_ID = os.environ['VIEW_ID']

def get_service():

    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    credentials = Credentials.from_service_account_file(
        KEY_FILE_LOCATION, scopes=SCOPES
    )
    service = build(serviceName='analyticsreporting', version='v4', credentials=credentials)
    return service

def get_report(service, view_id, start_date, end_date, metrics=[]):
    return service.reports().batchGet(
            body={
                'reportRequests': [{
                    'viewId': view_id,
                    'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                    'metrics': [{'expression': m} for m in metrics],
                }]
            }).execute()

start_date, end_date = 'today', 'today'
service = get_service()
response = get_report(service, VIEW_ID,start_date, end_date,metrics)

def collect_data(response):
    qtd_daily = response["reports"][0]["data"]["totals"][0]
    data = qtd_daily["values"][0]
    return data

def print_my_data():
    collect_data(response)

def prometheus_gg(num):
    registry = CollectorRegistry()
    g = Gauge("gg_daily", "Google Analytic Daily", registry=registry)
    g.set(num)
    return registry

def push_status():
    registry = prometheus_gg(collect_data(response))
    push_to_gateway(f"{PUSHGWIP}:9091", job="gg_analytics", registry=registry)

def main():
    push_status()

if __name__ == '__main__':
    main()