from html_writer import Html


class WebGenerator:
    def __init__(self):
        self.head = Html()
        self.body = Html()

    def generate_index(self, media_list):
        self.head = Html()
        self.body = Html()
        self.generate_html_header()
        self.generate_index_body_header()
        self.generate_index_search_form()
        self.generate_index_thumbnails(media_list)
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)

    def generate_media_page(self, media):
        self.head = Html()
        self.body = Html()
        self.generate_html_header()
        self.generate_media_page_sidebar("tags", media.tags)
        self.generate_media_page_sidebar("metadata", "")  # TODO: Add metadata to image object
        self.generate_media_page_media(media)
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)

    def generate_html_header(self):
        self.head.self_close_tag('meta', attributes=dict(charset='utf-8'))
        self.head.tag_with_content("Photo Stack Testing...", name='title')
        self.head.self_close_tag('link', attributes=dict(href="style.css", rel="stylesheet", type="text/css"))

    def generate_index_body_header(self):
        with self.body.tag('div', id_='"header"'):
            self.body.tag_with_content("Header Here", 'p')

    def generate_index_search_form(self):
        with self.body.tag('div', id_='"search"'):
            with self.body.tag('form', attributes=dict(action="")):
                self.body.self_close_tag('input', attributes=dict(type="text", placeholder="Search..", name="search"))
                self.body.tag_with_content("Search", 'button', attributes=dict(type="submit", text="search"))

    def generate_index_thumbnails(self, media_list):
        with self.body.tag('div', id_='"thumbnails"'):
            for media in media_list:
                with self.body.tag('a', attributes=dict(href="image=" + media.hash)):
                    self.body.self_close_tag('img', classes=["image"], attributes=dict(src="thumbs/" + media.hash))

    def generate_media_page_sidebar(self, div_id, list_elements):
        with self.body.tag('div', id_=div_id):
            with self.body.tag('ul'):
                for element in list_elements:
                    with self.body.tag('li'):
                        self.body.tag_with_content(element, 'a', attributes=dict(href="/?search=" + element))

    def generate_media_page_media(self, media):
        with self.body.tag('div', id_="media"):
            with self.body.tag('a', attributes=dict(href=media.path)):
                # TODO: Check for media type
                self.body.self_close_tag('img', attributes=dict(src=media.path))  # assuming everything is an image

