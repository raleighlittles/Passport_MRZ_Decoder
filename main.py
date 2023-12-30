import flask
import flask_helper
import web_form
import sys
import os

import passport_mrz_td3_decoder

flask_app = flask.Flask(flask_helper.generate_instance_id(), static_folder="static")

num_passport_photos = 0

# needed for CSRF
flask_app.config['SECRET_KEY'] = flask_helper.generate_secret_key(16)

@flask_app.route("/decode", methods=["GET", "POST"])
def decode_passport_mrz():
    
    flask_app.logger.info("decode_passport_mrz() called")

    form = web_form.SubmitPassportMRZForm()

    if flask.request.method == "GET":
        return flask.render_template("submit.html", form=form)
    
    elif flask.request.method == "POST":
        
        if not form.validate():
            # Reload the page to the user and let them try again
            flask.flash("Error must submit fields!")
            return flask.render_template("submit.html", form=form)
        
        else: # form passes validation
            mrz_line_1, mrz_line_2 = form.mrz_line_1.data, form.mrz_line_2.data
            flask_app.logger.info("User submitted an MRZ of '%s\n%s'", mrz_line_1, mrz_line_2)

            uploaded_photo = form.passport_img_file.data

            if uploaded_photo is not None:

                flask_app.logger.info(f"User submitted a passport photo of size {uploaded_photo.content_length}")

                temp_file_path = os.path.join(flask_app.instance_path, f"{num_passport_photos}.jpg")

                uploaded_photo.save(temp_file_path)

                mrz_lines_from_img = passport_mrz_td3_decoder.extract_mrz_from_passport_image(temp_file_path)
                result = passport_mrz_td3_decoder.decode_passport_mrz(f"{mrz_lines_from_img[0]}\n{mrz_lines_from_img[1]}")

            elif form.mrz_line_1 is not None and form.mrz_line_2 is not None:

                result = passport_mrz_td3_decoder.decode_passport_mrz(f"{mrz_line_1}\n{mrz_line_2}")

                return flask.render_template("submission_successful.html", surname=result.get("surname"), first_name=result.get("first_name"), country_issued=result.get("country_issued"), owner_nationality=result.get("owner_nationality"), birth_date=result.get("birth_date").strftime("%Y-%m-%d"), expiration_date=result.get("expiration_date").strftime('%Y-%m-%d'), owner_sex=result.get("owner_sex"), document_type=result.get("document_type"), document_number=result.get("document_number"), optional_data=result.get("optional_data"))


    else:
        flask_app.logger.error("Received invalid HTTP request verb")

