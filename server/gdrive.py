import requests
import re

def make_url(id):
	return f"https://docs.google.com/document/d/{id}/edit"

class GDrive:
	__slots__ = ['headers']

	def __init__(self, auth):
		self.headers = { 'Authorization': f"Bearer {auth['accessToken']}" }

	def upload_file(self, name, contents):
		resp = requests.post("https://docs.googleapis.com/v1/documents", json={'title': name}, headers=self.headers)
		resp.raise_for_status()
		doc = resp.json()
		update_url = f'https://docs.googleapis.com/v1/documents/{doc["documentId"]}:batchUpdate'
		write_control = { 'targetRevisionId': doc['revisionId'] }
		currently_inside_hyperlink = False
		doc = doc['documentId']
		current_position = 0
		while len(contents) > 0:
			segment_marker = ']' if currently_inside_hyperlink else '['
			split = contents.split(segment_marker, 1)
			if len(split) > 1:
				[segment, contents] = split
			else:
				segment = split[0]
				contents = ''
			if currently_inside_hyperlink:
				id = self.search_file_by_title(segment.strip())
				if id is not None:
					url = make_url(id)
					inner = [{
						'insertText': {
							'text': segment,
							'endOfSegmentLocation': {
								'segmentId': '',
							},
						}
					}, {
						'updateTextStyle': {
							'textStyle': {
								'link': {
									'url': url,
								},
							},
							'fields': 'link',
							'range': {
								'segmentId': '',
								'startIndex': current_position,
								'endIndex': current_position + len(segment),
							},
						}
					}]
					current_position += len(segment)
				else:
					inner = [{
						'insertText': {
							# put it back in brackets if the hyperlink creation failed
							'text': f'[{segment}]',
							'endOfSegmentLocation': {
								'segmentId': '',
							},
						}
					}]
					current_position += len(segment) + 2
			else:
				inner = [{
					'insertText': {
						'text': segment,
						'endOfSegmentLocation': {
							'segmentId': '',
						},
					}
				}]
				current_position += len(segment) + 2
			resp = requests.post(update_url, json={
				'requests': inner,
				'writeControl': write_control,
			}, headers=self.headers)
			resp.raise_for_status()
			write_control = resp.json()['writeControl']
			currently_inside_hyperlink = not currently_inside_hyperlink
		return doc

	def search_file_by_title(self, title):
		escaped_title = title.replace(r"'", r"\'")
		resp = requests.get('https://www.googleapis.com/drive/v3/files', params={ 'trashed': False, 'corpora': 'user', 'q': f"name = '{escaped_title}'", 'orderBy': 'recency' }, headers=self.headers)
		resp.raise_for_status()
		resp = resp.json()
		try:
			return resp['files'][0]['id']
		except IndexError:
			return None
