
def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)

# We collected 100 items of basic vocabulary from native speakers of a 
# diverse sample of Dravidian languages. Swadesh's 100-concept elicitation 
# list [27] was used to collect lexical data for 20 languages, 
def test_languages(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['LanguageTable'])) == 20


def test_sources(cldf_dataset, cldf_logger):
    assert len(cldf_dataset.sources) == 5


def test_parameters(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['ParameterTable'])) == 100

# The dataset contains 778 sites of which 91% are complete. 
def test_cognates(cldf_dataset, cldf_logger):
    cogsets = {c['Cognateset_ID'] for c in cldf_dataset['CognateTable']}
    assert len(cogsets) == 778


