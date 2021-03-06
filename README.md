# Which country is the best at XX ? 
## An app to identify best practices in public policy

This app is aimed at public policy makers and analysts looking for inspiration from abroad on how to tackle specific issues. The site is accessible at <ADD URL>

For instance, typing "Financing SME innovation" or "Improving access to healthcare in rural areas" will return a list of countries which have implemented world-leading polciies in this regard, as reflected in the density of international organisations' literature on this country-topic pair.

The user can then dig deeper into those leads.

### Data source

In this first version, the database consists of only World Bank's Open Knowledge Repository publications (listed under the 'Knowledge Notes' and accessible at https://openknowledge.worldbank.org/handle/10986/9387) in the English language.

Later versions will diversify the sources to include publications from other international organizations (OECD, IMF, UN agencies, international development banks, think tanks...)


### Under the hood
#### Database
Our data is stored on a MongoDB, accessible at : BLABLABLA


#### Data collection
The data collection was done in two stages:
1. A first pass over the World Bank's Open Knowledge Repository to collect document metadata (title, abstract, publication date...) and collect the pdf report's download url.

2. A second pass over the data to download the reports and turn them into machine-readable text using Optical Character Recognition tools in the pytesseract library.

#### Data processing
1. Each document's abstract/summary is vectorized using the XXX model. The resulting vector is stored in the database.

2. A scan of the contents of each document is performed using Hugging Face Transformer's NER pipeline to identify how many times each country is mentioned in the document.

3. These country names are standardized (e.g. Myanmar = Burma, Macedonia = North Macedonia = FYR Macedonia...) using the FuzzyWuzzy library.

4. The number of occurrences of each country is stored in the database, on a per-document basis.

#### Search
1. The user's search query is transformed into a vector using the XXX library.
2. This vector is scanned against the vectorized abstracts of documents in the knowledge base to identify relevant documents. If the cosine similarity threshold is above XX, the document is deemed relevant.
3. Based on the number of mentions of each country in the relevant document corpus, a score is assigned to each country. The search engine then returns the top X countries by order of relevance (<AS WELL AS INFO ON THE BEST DOCUMENTS?>)


## Future developments

#### quick wins
1. Fix doublecounts : niger vs nigeria, congo vs congo kinshasa, fix list of countries (add some unrecognized territories, expand name variations list...)
2. Improve the data collection pipeline (faster, more robust, no duplicates...)
3. remove duplicates in the database
4. Improve suggestion results (see if country is overrepresented on a given topic as opposed to absolute mention figures)

#### medium complexity/efforts/ressources
3. Add/change data sources
4. add pipeline to update the database with new documents
5. Finetune a pretrained model on our corpus to improve accuracy
6. Restructure search code/data structure to make requests faster


#### higher complexity/efforts/ressources
7. Add a module to see if a country is mentioned as an example or counter example
8. Add subcountry (State, Land, Autonomous Territory...) granularity
