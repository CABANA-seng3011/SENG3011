# Allowed categories for the /get function
ALLOWED_CATEGORIES = ["esg", "environmental_opportunity", "environmental_risk", "governance_opportunity", 
                      "governance_risk", "social_opportunity", "social_risk"]

# Allowed columns for the /get function
ALLOWED_COLUMNS = ["company_name", "perm_id", "data_type", "disclosure", "metric_description", "metric_name", "metric_unit",
                       "metric_value", "metric_year", "nb_points_of_observations", "metric_period", "provider_name", 
                       "reported_date", "pillar", "headquarter_country", "category"]

# Most companies in the NASDAQ 100, except ARM Holdings PLC ADR since our ESG data has no data for this
# As seen in: https://www.slickcharts.com/nasdaq100
NASDAQ_100 = [
    "Apple Inc", "Microsoft Corp", "NVIDIA Corp", "Amazon.com Inc", "Broadcom Inc", "Meta Platforms Inc", "Costco Wholesale Corp", "Netflix Inc", "Tesla Inc", "Alphabet Inc",
    "T-Mobile US Inc", "Cisco Systems Inc", "Linde PLC", "PepsiCo Inc", "Palantir Technologies Inc", "Intuitive Surgical Inc", "Amgen Inc", "Intuit Inc", "Adobe Inc",
    "Qualcomm Inc", "Booking Holdings Inc", "Advanced Micro Devices Inc", "Texas Instruments Inc", "Gilead Sciences Inc", "Comcast Corp", "Honeywell International Inc", "Vertex Pharmaceuticals Inc", "Automatic Data Processing Inc", "Applied Materials Inc",
    "Palo Alto Networks Inc", "MercadoLibre Inc", "Starbucks Corp", "Intel Corp", "Mondelez International Inc", "Analog Devices Inc", "O''Reilly Automotive Inc", "Cintas Corp", "KLA Corp", "Lam Research Corp",
    "CrowdStrike Holdings Inc", "Micron Technology Inc", "Microstrategy Inc", "PDD Holdings Inc", "Applovin Corp", "Fortinet Inc", "DoorDash Inc", "Cadence Design Systems Inc", "Regeneron Pharmaceuticals Inc", "Synopsys Inc",
    "Marriott International Inc", "Roper Technologies Inc", "PayPal Holdings Inc", "American Electric Power Company Inc", "Monster Beverage Corp", "ASML Holding NV", "Constellation Energy Corp", "Autodesk Inc", "Copart Inc", "Paychex Inc",
    "CSX Corp", "Charter Communications Inc", "Paccar Inc", "Workday Inc", "Airbnb Inc", "Keurig Dr Pepper Inc", "Exelon Corp", "Ross Stores Inc", "Marvell Technology Inc", "Fastenal Co",
    "NXP Semiconductors NV", "Verisk Analytics Inc", "AstraZeneca PLC", "Xcel Energy Inc", "Coca-Cola Europacific Partners PLC", "Axon Enterprise Inc", "Diamondback Energy Inc", "Kraft Heinz Co", "Electronic Arts Inc", "Baker Hughes Co",
    "Take-Two Interactive Software Inc", "Cognizant Technology Solutions Corp", "Old Dominion Freight Line Inc", "IDEXX Laboratories Inc", "Atlassian Corporation Ltd", "Lululemon Athletica Inc", "CoStar Group Inc", "Datadog Inc", "Ge Healthcare Technologies", "Zscaler Inc",
    "ANSYS Inc", "Dexcom Inc", "Trade Desk Inc", "Warner Bros Discovery Inc", "Microchip Technology Inc", "CDW Corp", "Biogen Inc", "GlobalFoundries Inc", "ON Semiconductor Corp", "MongoDB Inc"
]