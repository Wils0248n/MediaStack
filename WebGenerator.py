from html_writer import Html

class webgenerator:
    def __init__(self):
        self.head = Html()
        self.body = Html()

    def generateIndex(self, imageDataList):
        self.head = Html()
        self.body = Html()
        self.generateHTMLHeader()
        self.generateIndexBodyHeader()
        self.generateSearchForm()
        self.generateIndexBodyImages(imageDataList)
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)

    def generateImagePage(self, imageData, imageTags, imageMetadata):
        self.head = Html()
        self.body = Html()
        self.generateHTMLHeader()
        self.generateImagePageSideBar("tags", imageTags)
        self.generateImagePageSideBar("metadata", imageMetadata)
        self.generateImagePageImage(imageData[1])
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)

    def generateHTMLHeader(self):
        self.head.self_close_tag('meta', attributes=dict(charset='utf-8'))
        self.head.tag_with_content("Photo Stack Testing...", name='title')
        self.head.self_close_tag('link', attributes=dict(href="style.css", rel="stylesheet", type="text/css"))

    def generateIndexBodyHeader(self):
        with self.body.tag('div', id_='"header"'):
            self.body.tag_with_content("Header Here", 'p')

    def generateSearchForm(self):
        with self.body.tag('div', id_='"search"'):
            with self.body.tag('form', attributes=dict(action="")):
                self.body.self_close_tag('input', attributes=dict(type="text", placeholder="Search..", name="search"))
                self.body.tag_with_content("Search", 'button', attributes=dict(type="submit", text="search"))

    def generateIndexBodyImages(self, imageData):
        with self.body.tag('div', id_='"images"'):
            for row in imageData:
                self.addImageToIndexBody(row[0], row[1])

    def addImageToIndexBody(self, imageHash, imagePath):
        with self.body.tag('a', attributes=dict(href="image=" + imageHash)):
            self.body.self_close_tag('img', classes=["image"], attributes=dict(src="thumbs/" + imageHash))

    def generateImagePageSideBar(self, id, listElements):
        with self.body.tag('div', id_=id):
            with self.body.tag('ul'):
                for element in listElements:
                    with self.body.tag('li') as listElement:
                        self.body.tag_with_content(element, 'a', attributes=dict(href="/?search=" + element))

    def generateImagePageImage(self, image):
        with self.body.tag('div', id_="image"):
            with self.body.tag('a', attributes=dict(href=image)):
                self.body.self_close_tag('img', attributes=dict(src=image))

if __name__ == '__main__':
    print(webgenerator().generateImagePageSideBar("id", ["hello"]))