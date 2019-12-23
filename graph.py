#!/usr/bin/env python


import awspricing
import boto3
import os
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

os.environ['AWSPRICING_USE_CACHE']="1"
os.environ['AWSPRICING_CACHE_PATH']="./awspricing"

print("Start to download pricing cache...")
ec2_offer = awspricing.offer('AmazonEC2')
print("Done!")

def onDemand(instanceType):
    ec2_price= ec2_offer.ondemand_hourly(
      instance_type=instanceType,
      operating_system='Linux',
      region='us-east-1',
    )

    return ec2_price

def ReservedPrice(instanceType,term=1):
    term=str(term)
    reserved_price= ec2_offer.reserved_hourly(
      instance_type=instanceType,
      operating_system='Linux',
      lease_contract_length=term+'yr',
      offering_class='convertible',
      purchase_option='No Upfront',
      region='us-east-1',
    )

    return reserved_price


df = pd.read_csv('usage.csv')

plt.style.use('fivethirtyeight')
plt.style.use('seaborn')

instanceTypes = df.loc[df.UsageType.str.contains('BoxUsage')]
instanceTypes = instanceTypes.drop(columns=['Resource','Service','Operation','EndTime'])

items = []
for index, row in instanceTypes.iterrows():
    r = str(row.UsageType).split(':')[1]
    try:
        Reserved=float(ReservedPrice(r))*float(row.UsageValue)
    except:
        Reserved=float(onDemand(r))*float(row.UsageValue)
    items.append(Reserved)

instanceTypes['UsageCost'] = items

#items = []
#for index, row in instanceTypes.iterrows():
#    r = str(row.UsageType).split(':')[1]
#    try:
#        Reserved=float(onDemand(r))*float(row.UsageValue)
#    except:
#        Reserved=float(onDemand(r))*float(row.UsageValue)
#    items.append(Reserved)
#
#instanceTypes['DemandCost'] = items

plotting = instanceTypes.groupby(['StartTime']).sum().drop(columns=['UsageValue'])

quantile = plotting.UsageCost.quantile(.3)
#quantileDemand = plotting.DemandCost.quantile(.3)

title = "30 Percentile: " + str(quantile) 

items = []
for index, row in plotting.iterrows():
    output=quantile
    items.append(output)

plotting['SavingsPlan30\'th'] = items

plotting.plot()

plt.plot(marker='.')

plt.title(title)
plt.ylabel('Cost')
plt.xlabel('Date')
plt.show()
