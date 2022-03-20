from google.cloud import vision
import base64

class OCR:
	def __init__(self):
		self.client = vision.ImageAnnotatorClient()

	def get_info(self, bytes):
		img = self.get_img(bytes)
		return (self.get_text(img), self.get_title(img))
		

	def get_text(self, img):
		response = client.document_text_detection(image=image)
			words = self.get_words(response)

			for i in range(len(words)):
				try:
					if words[i+1].isalpha() or len(words[i+1]) > 1:
						words[i] += " "
				except IndexError:
					continue

			return "".join(words)
			
	def get_title(self, img):
		response = client.text_detection(image=image)
		texts = response.text_annotations

		for text in texts:
			vertices = text.bounding_poly.vertices


		
	def get_words(self, response):
		words = []
		for page in response.full_text_annotation.pages:
			for block in page.blocks:
				for paragraph in block.paragraphs:
					print("AAA")
					for word in paragraph.words:
						if word.confidence > 0.9:
							word_text = ''.join([
			                        symbol.text for symbol in word.symbols
			                    ])
							words.append(word_text)
		return words



	def get_img(self, bytes):
		content = base64.b64decode(bytes)
		return vision.Image(content=content)


"""
response = client.text_detection(image=image)
texts = response.text_annotations

for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
"""