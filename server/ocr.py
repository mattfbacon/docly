from google.cloud import vision
import os, io
import base64
import string

class OCR:
	def __init__(self):
		self.client = vision.ImageAnnotatorClient()

	def get_info(self, bytes):
		img = self.get_img(bytes)
		response = self.client.document_text_detection(image=img)

		words = []
		bounds = []
		
		for page in response.full_text_annotation.pages:
			for block in page.blocks:
				for paragraph in block.paragraphs:
					for word in paragraph.words:
						if word.confidence > 0.8:
							word_text = ''.join([
			                        symbol.text for symbol in word.symbols
			                    ])
							words.append(word_text)
							bounds.append(word.bounding_box)

		for i in range(len(words)):
			try:
				if words[i+1].isalpha() or len(words[i+1]) > 1:
					words[i] += " "
			except IndexError:
				continue

		title=None
		found = False
		for i in range(1, len(bounds)):
			cur_vertices = bounds[i].vertices
			prev_vertices = bounds[i-1].vertices

			cur_height = abs(cur_vertices[0].y-cur_vertices[2].y)
			prev_height = abs(prev_vertices[0].y-prev_vertices[2].y)

			cur_y = cur_vertices[2].y
			prev_y = prev_vertices[2].y

			#print(words[i-1], prev_height-cur_height, cur_y-prev_y)
			if cur_y-prev_y > 20:
				if not found:
					if prev_height-cur_height > 15:
						found = True
						title = "".join(words[:i]).strip()

				words[i] = "\n" + words[i]
			
		text = "".join(words).strip()
		return (text, title)

	def get_img(self, bytes):
			content = base64.b64decode(bytes)
			return vision.Image(content=content)
			# file_name = os.path.abspath('test/test13.jpg')

			# with io.open(file_name, 'rb') as image_file:
			# 	content = image_file.read()

			# return vision.Image(content=content)
