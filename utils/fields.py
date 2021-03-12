import ast
from PIL import Image
from wtforms.widgets import html_params, HTMLString
from wtforms.utils import unset_value
from flask_admin.helpers import get_url
from flask_admin.form.upload import ImageUploadField
from flask_admin._compat import string_types, urljoin
from path import FILE_UPLOAD_DIR

class MultipleImageUploadInput(object):
    empty_template = "<input %(file)s multiple>"

    # display multiple images in edit view of flask-admin
    data_template = ("<div class='image-thumbnail'>"
                     "   %(images)s"
                     "</div>"
                     "<input %(file)s multiple>")

    def __call__(self, field, **kwargs):

        kwargs.setdefault("id", field.id)
        kwargs.setdefault("name", field.name)

        args = {
            "file": html_params(type="file", **kwargs),
        }

        if field.data and isinstance(field.data, string_types):

            attributes = self.get_attributes(field)
            args["images"] = "&emsp;".join(["<img src='{}' /><input type='checkbox' name='{}-delete'>Delete</input>"
                                            .format('../../.' + FILE_UPLOAD_DIR + filename, filename) for src, filename in attributes])
            print(args["images"]) 
             
            template = self.data_template  

        else:
            template = self.empty_template

        return HTMLString(template % args)

    def get_attributes(self, field):

        for item in ast.literal_eval(field.data):

            filename = item

            if field.thumbnail_size:
                filename = field.thumbnail_fn(item)
            else:
                filename = item

            if field.url_relative_path:
                filename = urljoin(field.url_relative_path, filename)

            yield get_url(field.endpoint, filename=filename), item

class MultipleImageUploadField(ImageUploadField):

    widget = MultipleImageUploadInput()

    def process(self, formdata, data=unset_value):

        self.formdata = formdata  # get the formdata to delete images
        return super(MultipleImageUploadField, self).process(formdata, data)

    def process_formdata(self, valuelist):

        self.data = list()

        for value in valuelist:
            if self._is_uploaded_file(value):
                self.data.append(value)

    def populate_obj(self, obj, name):

        field = getattr(obj, name, None)

        if field:

            filenames = ast.literal_eval(field)

            for filename in filenames[:]:
                if filename + "-delete" in self.formdata:
                    self._delete_file(filename)
                    filenames.remove(filename)
        else:
            filenames = list()

        for data in self.data:
            if self._is_uploaded_file(data):

                self.image = Image.open(data)

                filename = self.generate_name(obj, data)
                filename = self._save_file(data, filename)

                data.filename = filename

                filenames.append(filename)

        setattr(obj, name, str(filenames))