from html_writer import Html

class webgenerator:
    def __init__(self):
        self.head = Html()
        self.body = Html()

    def generate(self, databaseManager):
        self.generateHTMLHeader()
        self.generateBody(databaseManager)
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)

    def generateHTMLHeader(self):
        self.head.self_close_tag('meta', attributes=dict(charset='utf-8'))
        self.head.tag_with_content("Photo Stack Testing...", name='title')
        self.head.self_close_tag('link', attributes=dict(href="style.css", rel="stylesheet", type="text/css"))

    def generateBody(self, databaseManager):
        self.generateBodyHeader()
        self.generateSearchForm()
        self.generateImages(databaseManager)

    def generateBodyHeader(self):
        with self.body.tag('div', id_='"header"'):
            self.body.tag_with_content("Header Here", 'p')

    def generateSearchForm(self):
        with self.body.tag('div', id_='"search"'):
            with self.body.tag('form', attributes=dict(action="")):
                self.body.self_close_tag('input', attributes=dict(type="text", placeholder="Search..", name="search"))
                self.body.tag_with_content("Search", 'button', attributes=dict(type="submit", text="search"))

    def generateImages(self, databaseManager):
        with self.body.tag('div', id_='"images"'):
            databaseManager.cursor.execute("SELECT * FROM imagedata")
            for row in databaseManager.cursor.fetchall():
                self.addImageToBody(row[0], row[1])

    def addImageToBody(self, imageHash, imagePath):
        with self.body.tag('a', attributes=dict(href=imagePath)):
            self.body.self_close_tag('img', classes=["image"], attributes=dict(src="thumbs/" + imageHash))
