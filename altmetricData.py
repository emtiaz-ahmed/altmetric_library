import requests
import json
import pandas as pd
import time

def read_data(inFile):
	data = pd.read_csv(inFile)
	return data

def get_search_content(doi):
	url = "https://api.altmetric.com/v1/doi/" + doi
	response = requests.get(url, headers={'Accept': 'application/json'})
	return response

def get_data(pdf):
	for i,element in pdf.iterrows():

		eids = []
		dois = []
		score = []
		altmetric_pos_percent = []
		same_age_pos = []
		same_age_source_pos = []

		eid = element['eids']
		doi = element['doi']
		response = get_search_content(doi)

		if response.status_code == 403:
			print("you are not authorized to this call")
			break
		elif response.status_code == 404:
			# print("Altmetric doesn't have any details for the article or set of articles you requested.")
			continue
		elif response.status_code == 429:
			print("Rate is limited and you finished your rate")
			time.sleep(3600)
			i = i-1
			continue
		elif response.status_code == 502:
			print("API under  maintenance")
			time.sleep(3600)			
			i = i-1
			continue
		
		else:
			try:
				result = json.loads(response.text.encode('utf-8'))
			except:
				print("no json available")
				continue

			score.append(result['score'])
			altmetric_pos_percent.append((result['context']['all']['rank']/result['context']['all']['count'])*100)
			same_age_pos.append(result['context']['similar_age_3m']['pct'])
			same_age_source_pos.append(result['context']['similar_age_journal_3m']['pct']) 


			print(score)
			print(altmetric_pos_percent)
			print(same_age_pos)
			print(same_age_source_pos)
			# print(result)
			break

		print("completed:",i)
		time.sleep(1)




	# print(response)

if __name__=="__main__":
	inputFile = "input/dois.csv"
	data = read_data(inputFile)
	get_data(data)
	# print(data)
