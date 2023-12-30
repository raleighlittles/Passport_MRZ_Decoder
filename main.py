import flask
import flask_helper
import web_form
import sys

flask_app = flask.Flask(flask_helper.generate_instance_id(), static_folder="static")

# needed for CSRF
flask_app.config['SECRET_KEY'] = flask_helper.generate_secret_key(16)

@flask_app.route("/decode", methods=["GET", "POST"])
def decode_passport_mrz():
    
    flask_app.logger.info("decode_passport_mrz() called")

    form = web_form.SubmitPassportMRZForm()

    if flask.request.method == "GET":
        return flask.render_template("submit.html", form=form)
    
    elif flask.request.method == "POST":
        pass

    else:
        flask_app.logger.error("Received invalid HTTP request verb")

        