import requests

class GDrive:
	__slots__ = ['headers']

	def __init__(self, auth):
		self.headers = { 'Authorization': f"Bearer {auth['accessToken']}" }

	def upload_file(self, name, contents):
		resp = requests.post("https://docs.googleapis.com/v1/documents", json={'title': name}, headers=self.headers)
		resp.raise_for_status()
		doc = resp.json()
		requests.post(f'https://docs.googleapis.com/v1/documents/{doc["documentId"]}:batchUpdate', json={
			'requests': [
				{
					'insertText': {
						'text': contents,
						'endOfSegmentLocation': {
							'segmentId': '',
						},
					}
				},
			],
			'writeControl': {
				'targetRevisionId': doc['revisionId'],
			},
		}, headers=self.headers).raise_for_status()

	def search_file_by_title(self, title):
		escaped_title = title.replace(r"'", r"\'")
		resp = requests.get('https://www.googleapis.com/drive/v3/files', params={ 'trashed': False, 'corpora': 'user', 'q': f"name = '{escaped_title}'", 'orderBy': 'recency' }, headers=self.headers)
		resp.raise_for_status()
		resp = resp.json()
		try:
			return resp['files'][0]['id']
		except IndexError:
			return None
