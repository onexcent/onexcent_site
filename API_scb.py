#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 12:45:52 2022

@author: final
"""


import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

session = requests.Session()


# ----------------------------------------------------------------------------

url_SB = "https://api.scb.se/OV0104/v1/doris/en/ssd/START/NR/NR0103/NR0103C/SektorENS2010Kv"

post_SB = {
  "query": [
    {
      "code": "Transaktionspost",
      "selection": {
        "filter": "agg:SAMTL_1",
        "values": [
          "III.1.2.B9"
        ]
      }
    }
  ],
  "response": {
    "format": "json"
  }
}




# ----------------------------------------------------------------------------


url_GDP = 'https://api.scb.se/OV0104/v1/doris/en/ssd/START/NR/NR0103/NR0103B/NR0103ENS2010T10SKv'


post_GDP = {
  "query": [
    {
      "code": "ContentsCode",
      "selection": {
        "filter": "item",
        "values": [
          "NR0103CG"
        ]
      }
    }
  ],
  "response": {
    "format": "json"
  }
}



# ----------------------------------------------------------------------------


url_DIR = 'https://api.scb.se/OV0104/v1/doris/en/ssd/START/NR/NR0103/NR0103C/SektorENS2010KvKeyIn'


post_DIR = {
  "query": [
    {
      "code": "Sektor",
      "selection": {
        "filter": "item",
        "values": [
          "S14+15"
        ]
      }
    }
  ],
  "response": {
    "format": "json"
  }
}




# ----------------------------------------------------------------------------


url_DI = 'https://api.scb.se/OV0104/v1/doris/en/ssd/START/NR/NR0103/NR0103C/HusDispInkENS2010Kv'


post_DI = {
  "query": [
    {
      "code": "Transaktionspost",
      "selection": {
        "filter": "item",
        "values": [
          "B6n",
          "B6real"
        ]
      }
    },
    {
      "code": "ContentsCode",
      "selection": {
        "filter": "item",
        "values": [
          "NR0103DQ"
        ]
      }
    }
  ],
  "response": {
    "format": "json"
  }
}



# ----------------------------------------------------------------------------


url_U = 'https://api.scb.se/OV0104/v1/doris/en/ssd/START/AM/AM0401/AM0401A/NAKUBefolkning2K'


post_U = {
  "query": [
    {
      "code": "Kon",
      "selection": {
        "filter": "item",
        "values": [
          "1+2"
        ]
      }
    },
    {
      "code": "Alder",
      "selection": {
        "filter": "item",
        "values": [
          "tot16-64"
        ]
      }
    },
    {
      "code": "Arbetskraftstillh",
      "selection": {
        "filter": "item",
        "values": [
          "SYS",
          "ALÖS"
        ]
      }
    },
    {
      "code": "ContentsCode",
      "selection": {
        "filter": "item",
        "values": [
          "000001BX"
        ]
      }
    }
  ],
  "response": {
    "format": "json"
  }
}



# ----------------------------------------------------------------------------





## Get data via JSON post 


# sectoral balances

response_SB = session.post(url=url_SB, json=post_SB)

response_SB_json = json.loads(response_SB.content.decode('utf-8-sig'))


dd = pd.DataFrame(response_SB_json["data"])

dd.insert(dd.ndim, "var", [None] *len(dd))
dd.insert(dd.ndim, "date", [None] *len(dd))

dd["var"] = [dd["key"][x][0] for x in range(len(dd))]
dd["date"] = [dd["key"][x][2] for x in range(len(dd))]
dd["values"] = [float(dd["values"][x][0].replace("..", "0")) for x in range(len(dd))]

# dd = dd.replace("..", "0")


# get unique macro factor names
mf_name = dd["var"].unique()

# get unique quarters
quarters = dd["date"].unique()

# define new transposed matrix
ddT_SB = (np.zeros( (len(quarters), len(mf_name)) ) )
for i in range(len(mf_name)):
    ddT_SB[range(len(quarters)), i] = dd["values"][dd["var"] == mf_name[i]]

ddT_SB = pd.DataFrame(ddT_SB, columns = mf_name, index = quarters)

# Transform to quarterly moving average

ddT_SB = ddT_SB.rolling(4, axis=0).mean()



# GDP

response_GDP = session.post(url=url_GDP, json=post_GDP)

response_GDP_json = json.loads(response_GDP.content.decode('utf-8-sig'))


dd = pd.DataFrame(response_GDP_json["data"])

dd.insert(dd.ndim, "var", [None] *len(dd))
dd.insert(dd.ndim, "date", [None] *len(dd))

dd["var"] = [dd["key"][x][0] for x in range(len(dd))]
dd["date"] = [dd["key"][x][1] for x in range(len(dd))]
dd["values"] = [float(dd["values"][x][0].replace("..", "0")) for x in range(len(dd))]


# get unique macro factor names
mf_name = dd["var"].unique()

# get unique quarters
quarters = dd["date"].unique()

# define new transposed matrix
ddT_GDP = (np.zeros( (len(quarters), len(mf_name)) ) )
for i in range(len(mf_name)):
    ddT_GDP[range(len(quarters)), i] = dd["values"][dd["var"] == mf_name[i]]

ddT_GDP = pd.DataFrame(ddT_GDP, columns = mf_name, index = quarters)





# disposable income

response_DI = session.post(url=url_DI, json=post_DI)

response_DI_json = json.loads(response_DI.content.decode('utf-8-sig'))



dd = pd.DataFrame(response_DI_json["data"])

dd.insert(dd.ndim, "var", [None] *len(dd))
dd.insert(dd.ndim, "date", [None] *len(dd))

dd["var"] = [dd["key"][x][0] for x in range(len(dd))]
dd["date"] = [dd["key"][x][1] for x in range(len(dd))]
dd["values"] = [float(dd["values"][x][0].replace("..", "0")) for x in range(len(dd))]


# get unique macro factor names
mf_name = dd["var"].unique()

# get unique quarters
quarters = dd["date"].unique()

# define new transposed matrix
ddT_DI = (np.zeros( (len(quarters), len(mf_name)) ) )
for i in range(len(mf_name)):
    ddT_DI[range(len(quarters)), i] = dd["values"][dd["var"] == mf_name[i]]

ddT_DI = pd.DataFrame(ddT_DI, columns = mf_name, index = quarters)

ddT_DI = ddT_DI.diff(1, axis = 1)



# disposable income ratio

response_DIR = session.post(url=url_DIR, json=post_DIR)

response_DIR_json = json.loads(response_DIR.content.decode('utf-8-sig'))



dd = pd.DataFrame(response_DIR_json["data"])

dd.insert(dd.ndim, "var", [None] *len(dd))
dd.insert(dd.ndim, "date", [None] *len(dd))

dd["var"] = [dd["key"][x][1] for x in range(len(dd))]
dd["date"] = [dd["key"][x][2] for x in range(len(dd))]
dd["values"] = [float(dd["values"][x][0].replace("..", "0")) for x in range(len(dd))]


# get unique macro factor names
mf_name = dd["var"].unique()

# get unique quarters
quarters = dd["date"].unique()

# define new transposed matrix
ddT_DIR = (np.zeros( (len(quarters), len(mf_name)) ) )
for i in range(len(mf_name)):
    ddT_DIR[range(len(quarters)), i] = dd["values"][dd["var"] == mf_name[i]]

ddT_DIR = pd.DataFrame(ddT_DIR, columns = mf_name, index = quarters)

ddT_DIR = ddT_DIR.rolling(4, axis=0).mean()


# unemployment

response_U = session.post(url=url_U, json=post_U)

response_U_json = json.loads(response_U.content.decode('utf-8-sig'))



dd = pd.DataFrame(response_U_json["data"])

dd.insert(dd.ndim, "var", [None] *len(dd))
dd.insert(dd.ndim, "date", [None] *len(dd))

dd["var"] = [dd["key"][x][2] for x in range(len(dd))]
dd["date"] = [dd["key"][x][3] for x in range(len(dd))]
dd["values"] = [float(dd["values"][x][0].replace("..", "0")) for x in range(len(dd))]


# get unique macro factor names
mf_name = dd["var"].unique()

# get unique quarters
quarters = dd["date"].unique()

# define new transposed matrix
ddT_U = (np.zeros( (len(quarters), len(mf_name)) ) )
for i in range(len(mf_name)):
    ddT_U[range(len(quarters)), i] = dd["values"][dd["var"] == mf_name[i]]

ddT_U = pd.DataFrame(ddT_U, columns = mf_name, index = quarters)










# merge together all the sub tables

macroVars = ddT_SB.join(ddT_GDP)
macroVars = macroVars.join(ddT_DI)
macroVars = macroVars.join(ddT_DIR)
macroVars = macroVars.join(ddT_U)

macroVars = macroVars[24:]


# Aggregate per sector

sumSector = pd.DataFrame(np.zeros((len(macroVars), 12))
                         , index=macroVars.index
                         ,columns= [
                             "DomesticPrivate"
                             ,"DomesticPublic"
                             ,"DomesticPrivateRatio"
                             ,"DomesticPublicRatio"                             
                             ,"Households"
                             ,"DomesticPrivateCorp"
                             ,"DomesticPrivateFin"
                             ,"DomesticPrivateNonFin"
                             ,"Foreign"
                             ,"DisposableIncome"
                             ,"NetLendingRatio"
                             ,"NetSavingRatio"
                             ]
                         )


# domestic private
sumSector["DomesticPrivate"] = macroVars[["S11", "S12", "S14", "S15"]].apply(sum, axis=1) / macroVars["BNPM"]

sumSector["DomesticPrivateRatio"] = sumSector["DomesticPrivate"] / sumSector["DomesticPrivate"].shift(4) - 1

# domestic private financial
sumSector["DomesticPrivateFin"] = macroVars["S12"] / macroVars["BNPM"]

# domestic private non financial
sumSector["DomesticPrivateNonFin"] = macroVars["S11"] / macroVars["BNPM"]

# domestic private corporate
sumSector["DomesticPrivateCorp"] = macroVars[["S11", "S12"]].apply(sum, axis=1) / macroVars["BNPM"]

# domestic private household
sumSector["Households"] = macroVars[["S14", "S15"]].apply(sum, axis=1) / macroVars["BNPM"]

# domestic public
sumSector["DomesticPublic"] = macroVars["S13"] / macroVars["BNPM"]

sumSector["DomesticPublicRatio"] = sumSector["DomesticPublic"] / sumSector["DomesticPublic"].shift(4) - 1

# foreign 
sumSector["Foreign"] = macroVars["S2"] / macroVars["BNPM"]

# net lending ratio 
sumSector["NetLendingRatio"] = macroVars["B9RatioB6nD8"]/100

# net saving ration
sumSector["NetSavingRatio"] = macroVars["B8nRatioB6nD8net"]/100

# disposable income
sumSector["DisposableIncome"] = macroVars["B8nRatioB6nD8net"]/100



plt.close("all")

plt.figure()

sumSector[["DomesticPrivate","DomesticPublic","Foreign"]].plot.bar(stacked=True, color=["g","r","b"])

sumSector[["Households","DomesticPrivateCorp","DomesticPublic","Foreign"]].plot.bar(stacked=True, color=["g","y","r","b"])



sumSector[["DomesticPrivate","DomesticPublic","Foreign"]].plot(color=["g","r","b"])


sumSector[["DomesticPrivateRatio","DomesticPublicRatio"]].plot(color=["g","r"])


sumSector[["DomesticPrivate","DomesticPublic","NetLendingRatio", "NetSavingRatio"]].plot()



sumSector.to_csv("sectoralBalancesSwe20224.csv")




factor_name ={
    "S1"	:"Total economy",
    "S11"	:"Non-financial corporations",
    "S12"	:"Financial corporations",
    "S13"	:"General government",
    "S1311"	:"Central government",
    "S1311+1314":"Central government and social security funds",
    "S1313"	:"Local government",
    "S13131"	 :"Municipalities´ etc.",
    "S13132"	 :"County councils",
    "S13133"	 :"Church of Sweden (until 1999)",
    "S1314"	:"Social security funds",
    "S14"	:"Households",
    "S14+15"	 :"Households and NPISH",
    "S15"	:"Non-profit institutions serving households: NPISH",
    "S151+1522"	:"Non-profit institutions serving households except church of Sweden",
    "S1521"	:"Church of Sweden (from 2000)",
    "S1N"	:"Not specified sector",
    "S2"	:"Rest of the world"
    }












