import pytest
from unittest.mock import patch
from index import app

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("index.run_sql_raw")
def test_getCompanies_valid_industry(mock_run_sql, client):
    """Test the /getCompanies route with a valid industry."""

    # Make a GET request to the /getCompanies route
    response = client.get("/getCompanies?industry=Biofuels")

    assert response.status_code == 200
    assert response.json == '{"companies": ["Pervasive Commodities Ltd", "Clearway Energy Operating LLC", "Tulasee Bio-Ethanol Ltd", "Laxai Pharma Ltd", "Duke Energy Florida LLC", "Cardinal Ethanol LLC", "Red Trail Energy LLC", "Tsaker New Energy Tech Co Ltd", "Indo Acidatama Tbk PT", "Willing New Energy Co Ltd", "Global Bioenergies SA", "Asian Insulators PCL", "Able Global Bhd", "AI Energy PCL", "Borosil Renewables Ltd", "Granite Falls Energy LLC", "China New Energy Ltd", "Biosev SA", "Scandinavian Biogas Fuels International AB", "Cortus Energy AB", "Montauk Renewables Inc", "Global Clean Energy Holdings Inc", "Industry Source Consulting Inc", "Active Energy Group PLC", "Southern Online Bio Technologies Ltd", "Longyan Zhuoyue New Energy Co Ltd", "Leaf Resources Ltd", "Timah Resources Ltd", "Affinity Energy and Health Ltd", "Taronis Fuels Inc", "Solarvest Bioenergy Inc", "BBGI PCL", "808 Renewable Energy Corp", "Green Earth Institute Co Ltd", "Evolution Fuels Inc", "Renewal Fuels Inc", "StemCell Institute Inc", "Triboron International AB", "Aggregated Micro Power Holdings PLC", "Mission Newenergy Ltd", "New Global Energy Inc", "Archaea Energy Inc", "Crimson Bioenergy Ltd", "Duke Energy Progress LLC", "Bluefire Renewables Inc", "Duke Energy Indiana LLC", "Western Asset Variable Rate Strategic Fund Inc", "Western Asset Emerging Markets Debt Fund Inc", "C2e Energy Inc", "GeoBio Energy Inc", "Verbio Vereinigte Bioenergie AG", "Alto Ingredients Inc", "Energy Absolute PCL", "CropEnergies AG", "Enviva Inc", "Gevo Inc", "Raizen SA", "Misen Energy AB (publ)", "Asia Biomass PCL", "Heron Lake BioEnergy LLC", "Fintec Global Bhd", "Velocys PLC", "Wave Sync Corp", "Blackstone Senior Floating Rate 2027 Term Fund"]}'

def test_getCompanies_no_industry(client):
    """Test the /getCompanies route with no industry."""
    # Make a GET request to the /getCompanies route with no industry
    response = client.get("/getCompanies")

    assert response.status_code == 400
    assert response.data.decode() == (
        "Invalid params, please specify an industry. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/964329628/Available+Companies+and+Industries for allowed industries."
    )

def test_getCompanies_invalid_industry(client):
    """Test the /getCompanies route with an invalid industry."""

    # Make a GET request to the /getCompanies route with an invalid industry
    response = client.get("/getCompanies?industry=CABANA")

    assert response.status_code == 400
    assert response.data.decode() == "No companies found for 'CABANA'. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/964329628/Available+Companies+and+Industries for allowed industries"
