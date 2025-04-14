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
    # Delete Duplicates not working for: 
    # "Linde PLC", "O''Reilly Automotive Inc", "Constellation Energy Corp", "Ge Healthcare Technologies", "GlobalFoundries Inc",

    "Apple Inc", "Microsoft Corp", "NVIDIA Corp", "Amazon.com Inc", "Broadcom Inc", "Meta Platforms Inc", "Costco Wholesale Corp", "Netflix Inc", "Tesla Inc", "Alphabet Inc", "T-Mobile US Inc", "Cisco Systems Inc", 
    "PepsiCo Inc", "Palantir Technologies Inc", "Intuitive Surgical Inc", "Amgen Inc", "Intuit Inc", "Adobe Inc",
    "Qualcomm Inc", "Booking Holdings Inc", "Advanced Micro Devices Inc", "Texas Instruments Inc", "Gilead Sciences Inc", "Comcast Corp", "Honeywell International Inc", "Vertex Pharmaceuticals Inc", "Automatic Data Processing Inc", "Applied Materials Inc",
    "Palo Alto Networks Inc", "MercadoLibre Inc", "Starbucks Corp", "Intel Corp", "Mondelez International Inc", "Analog Devices Inc",
    "Cintas Corp", "KLA Corp", "Lam Research Corp", "CrowdStrike Holdings Inc", "Micron Technology Inc", "Microstrategy Inc", "PDD Holdings Inc", "Applovin Corp", "Fortinet Inc", "DoorDash Inc", "Cadence Design Systems Inc", "Regeneron Pharmaceuticals Inc", 
    "Synopsys Inc", "Marriott International Inc", "Roper Technologies Inc", "PayPal Holdings Inc", "American Electric Power Company Inc", "Monster Beverage Corp", "ASML Holding NV", "Autodesk Inc", "Copart Inc", "Paychex Inc",
    "CSX Corp", "Charter Communications Inc", "Paccar Inc", "Workday Inc", "Airbnb Inc", "Keurig Dr Pepper Inc", "Exelon Corp", "Ross Stores Inc", "Marvell Technology Inc", "Fastenal Co",
    "NXP Semiconductors NV", "Verisk Analytics Inc", "AstraZeneca PLC", "Xcel Energy Inc", "Coca-Cola Europacific Partners PLC", "Axon Enterprise Inc", "Diamondback Energy Inc", "Kraft Heinz Co", "Electronic Arts Inc", "Baker Hughes Co",
    "Take-Two Interactive Software Inc", "Cognizant Technology Solutions Corp", "Old Dominion Freight Line Inc", "IDEXX Laboratories Inc", "Atlassian Corporation Ltd", "Lululemon Athletica Inc", "CoStar Group Inc", "Datadog Inc", "Zscaler Inc",
    "ANSYS Inc", "Dexcom Inc", "Trade Desk Inc", "Warner Bros Discovery Inc", "Microchip Technology Inc", "CDW Corp", "Biogen Inc", "ON Semiconductor Corp", "MongoDB Inc"
]

# 96 ESG Metrics available through our API
ESG_METRICS = [
    # Environmental Opportunity
    "ECO_DESIGN_PRODUCTS", "ENERGYUSETOTAL", "ENV_INVESTMENTS", "POLICY_EMISSIONS", "POLICY_SUSTAINABLE_PACKAGING", "POLICY_WATER_EFFICIENCY", "RENEWENERGYCONSUMED", "RENEWENERGYPRODUCED", "RENEWENERGYPURCHASED", "SUSTAINABLE_BUILDING_PRODUCTS",
    "TAKEBACK_RECYCLING_INITIATIVES", "TARGETS_EMISSIONS", "TARGETS_WATER_EFFICIENCY", "TRANALYTICRENEWENERGYUSE", "WASTE_RECYCLED", "WASTE_REDUCTION_TOTAL", "WATER_TECHNOLOGIES",
    # Environmental Risk
    "AIRPOLLUTANTS_DIRECT", "AIRPOLLUTANTS_INDIRECT", "CO2DIRECTSCOPE1", "CO2INDIRECTSCOPE2", "CO2INDIRECTSCOPE3", "CO2_NO_EQUIVALENTS", "HAZARDOUSWASTE", "NATURAL_RESOURCE_USE_DIRECT", "NOXEMISSIONS", "N_OXS_OX_EMISSIONS_REDUCTION",
    "PARTICULATE_MATTER_EMISSIONS", "SOXEMISSIONS", "TOXIC_CHEMICALS_REDUCTION", "VOCEMISSIONS", "VOC_EMISSIONS_REDUCTION", "WASTETOTAL", "WATERWITHDRAWALTOTAL", "WATER_USE_PAI_M10",
    # Governance Opportunity
    "ANALYTICAUDITCOMMIND", "ANALYTICBOARDFEMALE", "ANALYTICCEO_CHAIRMAN_SEPARATION", "ANALYTICCOMPCOMMIND", "ANALYTICINDEPBOARD", "ANALYTICNOMINATIONCOMMIND", "ANALYTICNONEXECBOARD", "ANALYTICQMS", "ANALYTICWASTERECYCLINGRATIO", "ANALYTIC_AUDIT_COMM_EXPERTISE",
    "ANALYTIC_VOTING_RIGHTS", "BOARDMEETINGATTENDANCEAVG", "COMMMEETINGSATTENDANCEAVG", "GLOBAL_COMPACT",
    # Governance Risk
    "ANALYTICNONAUDITAUDITFEESRATIO", "ANALYTIC_ANTI_TAKEOVER_DEVICES", "ANNUAL_MEDIAN_COMPENSATION", "AUDITCOMMNONEXECMEMBERS", "CALL_MEETINGS_LIMITED_RIGHTS", "CEO_ANNUAL_COMPENSATION", "CEO_PAY_RATIO_MEDIAN", "COMPCOMMNONEXECMEMBERS", "CSR_REPORTINGGRI", "CSR_REPORTING_EXTERNAL_AUDIT",
    "ELIMINATION_CUM_VOTING_RIGHTS",
    # Social Opportunity
    "ANALYTICCSR_COMP_INCENTIVES", "ANALYTICEMPLOYMENTCREATION", "ANALYTICTOTALDONATIONS", "ANIMAL_TESTING_REDUCTION", "AVGTRAININGHOURS", "CONFORMANCE_OECD_MNE", "CONFORMANCE_UN_GUID", "DAY_CARE_SERVICES", "GRIEVANCE_REPORTING_PROCESS", "HUMAN_RIGHTS_CONTRACTOR",
    "HUMAN_RIGHTS_POLICY_DUEDILIGENCE", "ISO14000", "LABELED_WOOD", "POLICY_FREEDOMOF_ASSOCIATION", "TARGETS_DIVERSITY_OPPORTUNITY", "TRADEUNIONREP", "WHISTLEBLOWER_PROTECTION", "WOMENEMPLOYEES", "WOMENMANAGERS",
    # Social Risk
    "BRIBERY_AND_CORRUPTION_PAI_INSUFFICIENT_ACTIONS", "EMPLOYEEFATALITIES", "EMPLOYEE_HEALTH_SAFETY_POLICY", "GENDER_PAY_GAP_PERCENTAGE", "HUMAN_RIGHTS_VIOLATION_PAI", "IMPROVEMENT_TOOLS_BUSINESS_ETHICS", "LOSTWORKINGDAYS", "POLICY_BOARD_DIVERSITY", "POLICY_BRIBERYAND_CORRUPTION", "POLICY_BUSINESS_ETHICS",
    "POLICY_CHILD_LABOR", "POLICY_DATA_PRIVACY", "POLICY_FORCED_LABOR", "POLICY_HUMAN_RIGHTS", "SUPPLY_CHAINHS_POLICY", "TIRTOTAL", "TURNOVEREMPLOYEES"
]

# ESG_METRICS Perfect (One value for each company)
ESG_METRICS_PERFECT = [
    'ENERGYUSETOTAL', 'POLICY_EMISSIONS', 'POLICY_WATER_EFFICIENCY', 'TARGETS_WATER_EFFICIENCY', 'CO2DIRECTSCOPE1', 'CO2INDIRECTSCOPE2', 'TOXIC_CHEMICALS_REDUCTION', 'WATERWITHDRAWALTOTAL', 'WATER_USE_PAI_M10', 'ANALYTICAUDITCOMMIND', 'ANALYTICBOARDFEMALE', 'ANALYTICCOMPCOMMIND', 'ANALYTICINDEPBOARD', 
    'ANALYTICNONEXECBOARD', 'ANALYTIC_AUDIT_COMM_EXPERTISE', 'ANALYTIC_VOTING_RIGHTS', 'AUDITCOMMNONEXECMEMBERS', 'COMPCOMMNONEXECMEMBERS', 'CSR_REPORTINGGRI', 'CSR_REPORTING_EXTERNAL_AUDIT', 'ANALYTICCSR_COMP_INCENTIVES', 'ANALYTICEMPLOYMENTCREATION', 'ANIMAL_TESTING_REDUCTION', 'CONFORMANCE_OECD_MNE', 
    'CONFORMANCE_UN_GUID', 'DAY_CARE_SERVICES', 'GRIEVANCE_REPORTING_PROCESS', 'HUMAN_RIGHTS_CONTRACTOR', 'ISO14000', 'LABELED_WOOD', 'POLICY_FREEDOMOF_ASSOCIATION', 'TARGETS_DIVERSITY_OPPORTUNITY', 'WHISTLEBLOWER_PROTECTION', 'BRIBERY_AND_CORRUPTION_PAI_INSUFFICIENT_ACTIONS', 'EMPLOYEE_HEALTH_SAFETY_POLICY', 
    'HUMAN_RIGHTS_VIOLATION_PAI', 'IMPROVEMENT_TOOLS_BUSINESS_ETHICS', 'POLICY_BOARD_DIVERSITY', 'POLICY_CHILD_LABOR', 'POLICY_DATA_PRIVACY', 'POLICY_FORCED_LABOR', 'POLICY_HUMAN_RIGHTS', 'SUPPLY_CHAINHS_POLICY'
]