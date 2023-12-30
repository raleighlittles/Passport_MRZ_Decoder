import flask
import flask_helper
import web_form
import inspect
import os

# locals
import passport_mrz_td3_decoder

flask_app = flask.Flask(
    flask_helper.generate_instance_id(), static_folder="static")

# needed for CSRF
flask_app.config['SECRET_KEY'] = flask_helper.generate_secret_key(16)


@flask_app.route("/decode", methods=["GET", "POST"])
def decode_passport_mrz():

    curr_function_name = inspect.stack()[0][3]

    flask_app.logger.info("%s() called", curr_function_name)

    form = web_form.SubmitPassportMRZForm()

    if flask.request.method == "GET":
        return flask.render_template("submit.html", form=form)

    elif flask.request.method == "POST":

        if not form.validate():
            # Reload the page to the user and let them try again
            flask.flash("Error must submit fields!")
            return flask.render_template("submit.html", form=form)

        else:  # form passes validation
            mrz_line_1, mrz_line_2 = form.mrz_line_1.data, form.mrz_line_2.data
            flask_app.logger.info(
                "User submitted an MRZ of '%s\n%s'", mrz_line_1, mrz_line_2)

            uploaded_photo = form.passport_img_file.data

            if uploaded_photo is not None:
                # User uploaded a picture of their passport. Save it to a local file, then run processing on it

                # TODO why is size always 0?
                flask_app.logger.info(
                    f"User submitted a passport photo: '{uploaded_photo.filename}' with size {uploaded_photo.content_length}")

                temp_file_path = os.path.join(
                    os.getcwd(), uploaded_photo.filename)

                uploaded_photo.save(temp_file_path)

                mrz_lines_from_img = passport_mrz_td3_decoder.extract_mrz_from_passport_image(
                    temp_file_path)

                flask_app.logger.info(
                    f"Decoded text from file: {mrz_lines_from_img}")
                result = passport_mrz_td3_decoder.decode_passport_mrz(
                    f"{mrz_lines_from_img[0]}\n{mrz_lines_from_img[1]}")
                

                flask_app.logger.debug("Decoded passport info: \r\n %s", result)

                # cleanup file
                os.remove(temp_file_path)

                # Show results of parsing
                return flask.render_template("submission_successful.html", surname=result.get("surname"), first_name=result.get("first_name"), country_issued=result.get("country_issued"), owner_nationality=result.get("owner_nationality"), birth_date=result.get("birth_date").strftime("%Y-%m-%d"), expiration_date=result.get("expiration_date").strftime('%Y-%m-%d'), owner_sex=result.get("owner_sex"), document_type=result.get("document_type"), document_number=result.get("document_number"), optional_data=result.get("optional_data"), birth_date_checksum=result["hashes"].get("birth_date"), expiration_date_checksum=result["hashes"].get("expiry_date"), document_number_checksum=result["hashes"].get("document_number"), optional_data_checksum=result["hashes"].get("optional_data"), final_checksum=result["hashes"].get("final"))

            elif form.mrz_line_1 is not None and form.mrz_line_2 is not None:

                result = passport_mrz_td3_decoder.decode_passport_mrz(
                    f"{mrz_line_1}\n{mrz_line_2}")
                
                flask_app.logger.debug("Decoded passport info: \r\n %s", result)

                return flask.render_template("submission_successful.html", surname=result.get("surname"), first_name=result.get("first_name"), country_issued=result.get("country_issued"), owner_nationality=result.get("owner_nationality"), birth_date=result.get("birth_date").strftime("%Y-%m-%d"), expiration_date=result.get("expiration_date").strftime('%Y-%m-%d'), owner_sex=result.get("owner_sex"), document_type=result.get("document_type"), document_number=result.get("document_number"), optional_data=result.get("optional_data"), birth_date_checksum=result["hashes"].get("birth_date"), expiration_date_checksum=result["hashes"].get("expiry_date"), document_number_checksum=result["hashes"].get("document_number"), optional_data_checksum=result["hashes"].get("optional_data"), final_checksum=result["hashes"].get("final"))

    else:
        flask_app.logger.error(
            "Received invalid HTTP request verb: %s", flask.request.method)
