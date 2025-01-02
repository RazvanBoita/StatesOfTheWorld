from services.country_service import CountryService 


def make_space():
    print("\n" * 4)

country_service = CountryService()
top_countries_by_population = country_service.get_top_by_population()
i = 1
print("Top 10 countries by population:")
for country in top_countries_by_population:
    print(f"{i}. {country.name} with population {country.population}")
    i += 1

top_countries_by_density = country_service.get_top_by_density()

make_space()

i = 1
print("Top 10 countries by density:")
for country in top_countries_by_density:
    print(f"{i}. {country.name} with density {country.density}")
    i += 1


make_space()

english_speaking_countries = country_service.get_by_language('English')
print("English speaking countries:")
for country in english_speaking_countries:
    print(country.name)