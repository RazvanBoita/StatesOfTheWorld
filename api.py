from flask import Flask, Blueprint, jsonify, request
from services.country_service import CountryService

country_service = CountryService()
app = Flask(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api/countries')


@api_bp.route('/', methods=['GET'])
def get_all_countries():
    countries = country_service.get_all_countries()
    return jsonify(countries), 200



@api_bp.route('/top-population/<int:n>', methods=['GET'])
@api_bp.route('/top-population', methods=['GET'])
def top_countries_by_population(n=10):
    countries = country_service.get_top_by_population(n)
    return jsonify(countries), 200


@api_bp.route('/top-density/<int:n>', methods=['GET'])
@api_bp.route('/top-density', methods=['GET'])
def top_countries_by_density(n=10):
    countries = country_service.get_top_by_density(n)
    return jsonify(countries), 200

@api_bp.route('/speaking', methods=['GET'])
def countries_speaking_language():
    language = request.args.get('language') 
    if not language:
        return jsonify({"error": "Language parameter is required."}), 400
    
    countries = country_service.get_by_language(language)
    return jsonify(countries), 200

@api_bp.route('/timezone', methods=['GET'])
def countries_by_timezone():
    timezone = request.args.get('timezone') 

    if not timezone:
        return jsonify({"error": "Timezone parameter is required."}), 400
    
    
    countries = country_service.get_by_timezone(timezone)
    return jsonify(countries), 200

@api_bp.route('/political', methods=['GET'])
def countries_by_regime():
    regime = request.args.get('regime')
    if not regime:
        return jsonify({"error": "Regime parameter is required."}), 400
    
    regime_mapping = {
        "Presidential Republic": "presidential republic",
        "Parliamentary Republic": "parliamentary republic",
        "Constitutional Monarchy": "constitutional monarchy",
        "Absolute Monarchy": "absolute monarchy",
        "Theocracy": "theocratic",
        "Socialist Republic": "socialist republic",
        "Federal Republic": "federal",
        "Military Junta": "military junta",
        "Authoritarian State": "authoritarian",
        "Transitional Government": "transitional government"
    }
    
    if regime not in regime_mapping:
        return jsonify({"error": "Invalid regime type."}), 400
    
    regime_query = regime_mapping[regime]
    countries = country_service.get_by_regime(regime_query) 
    return jsonify(countries), 200



app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
