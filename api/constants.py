from dotenv import load_dotenv, find_dotenv
import os
import psycopg2

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

def get_industry(company):
    sql = """
    SELECT industry FROM industry
    WHERE company = '{}'
    """.format(company)
    return sql

found_companies = 0

load_dotenv(find_dotenv())
try:
    # Establish connection
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()

    for company in NASDAQ_100:
        sql = get_industry(company)
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print(f"No industry found for {company}")
        else:
            found_companies += 1
            print(f"Found companies: {found_companies}")

    # Close connection and return results
    cursor.close()
    conn.close()
    
except Exception as e:
    raise e
