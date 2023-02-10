import pandas as pd
import datetime
import math

defaultValue = 0
dates = ["2019-12-01", "2022-12-31"]
startDate, endDate = [datetime.datetime.strptime(_, "%Y-%m-%d") for _ in dates]
 
monthList = [datetime.datetime.strptime('%2.2d-%2.2d' % (year, month), '%Y-%m').strftime('%B-%Y')
    for year in range(startDate.year, endDate.year+1)
    for month in range(startDate.month if year == startDate.year else 1,
                       endDate.month+1 if year == endDate.year else 13)]

monthValues = {}.fromkeys(monthList, defaultValue)

events = ["event_1|December-2019", "event_2|January-2020", "event_3a|March-2020", "event_3b|April-2020", "event_4a|May-2020", "event_4b|June-2020", "event_5|July-2020", "event_6|August-2020", "event_7|December-2020"]
eventValues = {}.fromkeys(events, defaultValue)

# dateMarker1 = datetime.datetime.strptime("12-2019", "%m-%Y")
# alpha_betaMarker = datetime.datetime.strptime("12-18-2020", "%m-%d-%Y")

variants = [
    "alpha_beta|December-18-2020",
    "gamma|January-11-2021",
    "delta|May-11-2021" ,
    "omicron|October-26-2021",
    "alpha_beta_gamma_2|March-09-2022",
    "delta_2|June-07-2022"
]
variantValues = {}.fromkeys(variants, defaultValue)

markerCounters = []
dates = pd.read_csv('LitQuery_2.csv')
dates = dates[dates['Pandemic'].isin(['COVID-19', 'COVID-19, Zika virus'])]

print(len(dates))

# read each date and starting checking within ranges for Publication Dates
for index, row in dates.iterrows():
    print(index,"/", dates.shape[0], end='\r')
    publicationDate = str(row['New Publication Date'])
    researchStartDate = str(row['Start Dates of Research'])
    researchEndDate = str(row['End Dates of Research'])

    if(publicationDate != 'nan'):
        publicationDate = datetime.datetime.strptime(publicationDate, "%m/%d/%Y")
        for event in events:
            eventDate = event.split('|')[1]
            eventDateTransformed = datetime.datetime.strptime(eventDate, "%B-%Y")
            # if date is within range dateMarker:
            if(publicationDate.month == eventDateTransformed.month and publicationDate.year == eventDateTransformed.year):
                #  count++
                eventValues[event] += 1

        for month in monthList:
            monthTransformed = datetime.datetime.strptime(month, "%B-%Y")
            if(publicationDate.month == monthTransformed.month and publicationDate.year == monthTransformed.year):
                #  count++
                monthValues[month] += 1

    if(researchEndDate != 'nan' and researchStartDate != 'nan'):
        researchStartDate = datetime.datetime.strptime(researchStartDate, "%m/%d/%Y")
        researchEndDate = datetime.datetime.strptime(researchEndDate, "%m/%d/%Y")
        
        for variant in variants:
            variantDate = variant.split('|')[1]
            variantDateTransformed = datetime.datetime.strptime(variantDate, "%B-%d-%Y")

            if(researchStartDate<variantDateTransformed<researchEndDate):
                variantValues[variant] += 1



print(eventValues, monthValues, variantValues)




# read each date and starting checking within ranges for Research Dates




