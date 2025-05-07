from flask import Flask, jsonify, request
from flask_cors import CORS
from DataAgent import DataAgent
import os
from datetime import datetime

data_agent = DataAgent()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Hello from Firebase!"})

@app.route('/stock_historic_price', methods=['GET'])
def get_stock_price():

    symbol = request.args.get('symbol', default='missing_input', type=str)
    years = request.args.get('years', default=5, type=int)

    if symbol.strip == "" or symbol == "missing_input":
        return {"Error: Missing argument: 'symbol'"}

    historic_price = data_agent.queryStock(dataType='historic_price', symbol=symbol, years=years)

    return jsonify(historic_price=historic_price)

@app.route("/stock_info", methods=["GET"])
def get_stock_info():

    symbol = request.args.get('symbol', default='missing_input', type=str)

    if symbol.strip == "" or symbol == "missing_input":
        return {"Error: Missing argument: 'symbol'"}

    company_profile = data_agent.queryStock(dataType='company_profile', symbol=symbol)

    return jsonify(info=company_profile)


@app.route("/stock_key_figures", methods=["GET"])
def get_stock_key_figures():

    symbol = request.args.get('symbol', default='missing_input', type=str)

    if symbol.strip == "" or symbol == "missing_input":
        return {"Error: Missing argument: 'symbol'"}

    key_figures = data_agent.queryStock(dataType='key_figures', symbol=symbol)

    return jsonify(key_figures=key_figures)

@app.route("/country_data", methods=["GET"])
def get_country_data():

    country_code = request.args.get('country_code', default='missing_input', type=str)
    data_type = request.args.get('data_type', default='missing_input', type=str)
    start_year = request.args.get('start_year', default=1970, type=int)
    end_year = request.args.get('end_year', default=2030, type=int)

    if country_code.strip == "" or country_code == "missing_input":
        return {"Error: Missing argument: 'country_code'"}
    
    if data_type.strip == "" or data_type == "missing_input":
        return {"Error: Missing argument: 'data_type'"}

    country_data = data_agent.queryCountry(country_code=country_code, data_type=data_type, start_year=start_year, end_year=end_year)

    return jsonify(country_data)

@app.route("/historic_forex", methods=["GET"])
def get_historic_forex():

    base = request.args.get("base", default="missing_input", type=str).strip('"')
    quote = request.args.get("quote", default="missing_input", type=str).strip('"')
    start_date = request.args.get("start_date", default="missing_input", type=str).strip('"')

    try:
        data = data_agent.queryForexMajor(base=base, quote=quote, start_date=start_date)

    except:
        data = {"Input error"}

    return jsonify(data)

@app.route("/commodity", methods=["GET"])
def get_commodity():

    commodity_id = request.args.get("id", default="missing_input", type=str).strip('"')
    start_date = request.args.get("start_date", default="missing_input", type=str).strip('"')

    try:
        data = data_agent.queryCommodities(commodity_id=commodity_id, start_date=start_date)

    except:
        data = {"Input error"}

    return jsonify(data)

@app.route("/explain", methods=["GET"])
def get_explanation():

    to_explain = request.args.get("to_explain", default="missing_input", type=str).strip('"')

    try:
        data = data_agent.queryExplanation(to_explain=to_explain)

    except:
        data = {"Input error"}

    explanation = {'explanation': data}

    return jsonify(explanation)

@app.route("/get_report", methods=["GET"])
def get_report():

    report_type = request.args.get("report_type", default="missing_input", type=str).strip('"')
    code1 = request.args.get("code1", default="missing_input", type=str).strip('"')
    code2 = request.args.get("code2", default="missing_input", type=str).strip('"')

    try:
        report = data_agent.queryReport(report_type=report_type, code1=code1, code2=code2)

    except:
        report = {'Error generating report.'}

    report_dict = {'report': report}

    return jsonify(report_dict)

@app.route("/get_prediction", methods=["GET"])
def get_prediction():

    prediction_type = request.args.get("prediction_type", default="missing_input", type=str).strip('"')
    code1 = request.args.get("code1", default="missing_input", type=str).strip('"')
    code2 = request.args.get("code2", default="missing_input", type=str).strip('"')

    try:
        prediction = data_agent.queryPrediction(prediction_type=prediction_type, code1=code1, code2=code2)

    except:
        prediction = {'Error generating prediction.'}

    return jsonify(prediction)

@app.route("/get_pdf_url", methods=["GET"])
def get_pdf_url():

    report_type = request.args.get("report_type", default="missing_input", type=str).strip('"')
    code = request.args.get("code", default="missing_input", type=str).strip('"')
    report_subject = request.args.get("report_subject", default="missing_input", type=str).strip('"')

    overview_forex = request.args.get("overview_forex", default=1, type=int)
    if overview_forex == 1:
        overview_forex = True
    else:
        overview_forex = False

    key_figures_forex = request.args.get("key_figures_forex", default=1, type=int)
    if key_figures_forex == 1:
        key_figures_forex = True
    else:
        key_figures_forex = False

    recent_performance_forex = request.args.get("recent_performance_forex", default=1, type=int)
    if recent_performance_forex == 1:
        recent_performance_forex = True
    else:
        recent_performance_forex = False

    future_outlook_forex = request.args.get("future_outlook_forex", default=1, type=int)
    if future_outlook_forex == 1:
        future_outlook_forex = True
    else:
        future_outlook_forex = False

    forecast_forex = request.args.get("forecast_forex", default=1, type=int)
    if forecast_forex == 1:
        forecast_forex = True
    else:
        forecast_forex = False

    introduction_country = request.args.get("introduction_country", default=1, type=int)
    if introduction_country == 1:
        introduction_country = True
    else:
        introduction_country = False

    historic_economic_performance_country = request.args.get("historic_economic_performance_country", default=1, type=int)
    if historic_economic_performance_country == 1:
        historic_economic_performance_country = True
    else:
        historic_economic_performance_country = False

    historic_social_data_country = request.args.get("historic_social_data_country", default=1, type=int)
    if historic_social_data_country == 1:
        historic_social_data_country = True
    else:
        historic_social_data_country = False

    historic_environmental_data_country = request.args.get("historic_environmental_data_country", default=1, type=int)
    if historic_environmental_data_country == 1:
        historic_environmental_data_country = True
    else:
        historic_environmental_data_country = False

    future_economic_outlook_country = request.args.get("future_economic_outlook_country", default=1, type=int)
    if future_economic_outlook_country == 1:
        future_economic_outlook_country = True
    else:
        future_economic_outlook_country = False

    forecast_country = request.args.get("forecast_country", default=1, type=int)
    if forecast_country == 1:
        forecast_country = True
    else:
        forecast_country = False

    commodity_overview_commodity = request.args.get("commodity_overview_commodity", default=1, type=int)
    if commodity_overview_commodity == 1:
        commodity_overview_commodity = True
    else:
        commodity_overview_commodity = False

    historic_price_analysis_commodity = request.args.get("historic_price_analysis_commodity", default=1, type=int)
    if historic_price_analysis_commodity == 1:
        historic_price_analysis_commodity = True
    else:
        historic_price_analysis_commodity = False

    recent_price_trends_commodity = request.args.get("recent_price_trends_commodity", default=1, type=int)
    if recent_price_trends_commodity == 1:
        recent_price_trends_commodity = True
    else:
        recent_price_trends_commodity = False

    future_outlook_commodity = request.args.get("future_outlook_commodity", default=1, type=int)
    if future_outlook_commodity == 1:
        future_outlook_commodity = True
    else:
        future_outlook_commodity = False

    forecast_commodity = request.args.get("forecast_commodity", default=1, type=int)
    if forecast_commodity == 1:
        forecast_commodity = True
    else:
        forecast_commodity = False

    try:
        report_url = data_agent.queryRerportPDF(report_type=report_type, 
                                                type_id=code,
                                                overview_forex=overview_forex, 
                                                key_figures_forex=key_figures_forex, 
                                                recent_performance_forex=recent_performance_forex, 
                                                future_outlook_forex=future_outlook_forex,
                                                forecast_forex=forecast_forex,
                                                introduction_country=introduction_country,
                                                historic_economic_performance_country=historic_economic_performance_country,
                                                historic_social_data_country=historic_social_data_country,
                                                historic_environmental_data_country=historic_environmental_data_country,
                                                future_economic_outlook_country=future_economic_outlook_country,
                                                forecast_country=forecast_country,
                                                commodity_overview_commodity=commodity_overview_commodity,
                                                historic_price_analysis_commodity=historic_price_analysis_commodity,
                                                recent_price_trends_commodity=recent_price_trends_commodity,
                                                future_outlook_commodity=future_outlook_commodity,
                                                forecast_commodity=forecast_commodity)
        
        report_url['report_subject'] = report_subject
        now = datetime.now()
        current_time_str = now.strftime("%Y-%m-%d")
        report_url['generated_time'] = current_time_str

    except:
        report_url = {'Error generating report pdf.'}

    return jsonify(report_url)

# Don't call app.run here; gunicorn will take care of it.
if __name__ == '__main__':
    # Keep this for local testing (when running manually outside of Cloud Run)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
