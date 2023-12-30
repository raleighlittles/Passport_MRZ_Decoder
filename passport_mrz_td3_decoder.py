import argparse
from mrz.checker.td3 import TD3CodeChecker
import datetime
import pdb
import sys
import os
import pytesseract
import typing

PASSPORT_MRZ_LINE_LENGTH = 44

def create_dict_from_result(mrz_result) -> dict:

    # Uses 2-digit years (no century) instead of the standard 4-digit year
    passport_date_fmt = "%y%m%d"

    passport_data = dict({"surname": mrz_result.surname, "name": mrz_result.name, "country_issued": mrz_result.country, "owner_nationality": mrz_result.nationality, "birth_date": datetime.datetime.strptime(mrz_result.birth_date, passport_date_fmt),
                         "expiration_date": datetime.datetime.strptime(mrz_result.expiry_date, passport_date_fmt), "owner_sex": mrz_result.sex, "document_type": mrz_result.document_type, "document_number": mrz_result.document_number, "optional_data": mrz_result.optional_data})
    hash_data = dict({"birth_date": mrz_result.birth_date_hash, "expiry_date": mrz_result.expiry_date_hash,
                     "document_number": mrz_result.document_number_hash, "optional_data": mrz_result.optional_data_hash, "final": mrz_result.final_hash})

    passport_data["hashes"] = hash_data

    return passport_data


def extract_mrz_from_passport_image(passport_image_filename: str) -> typing.List:

    # See the `config/` dir for more info
    raw_passport_text = pytesseract.image_to_string(
        passport_image_filename, lang='eng', config="--tessdata-dir config")

    # Only grab text lines that aren't empty
    passport_text_lines = [x for x in raw_passport_text.split("\n") if x]

    # remember, MRZ is always the bottom 2 lines of a passport
    return passport_text_lines[-2:]


def decode_passport_mrz(passport_mrz) -> dict:

    if len(passport_mrz) < (PASSPORT_MRZ_LINE_LENGTH * 2):
        raise ValueError(
            f"Passport MRZ received was incorrect length. Received={len(passport_mrz)}, Minimum required={PASSPORT_MRZ_LINE_LENGTH*2}")

    passport_checker_result = TD3CodeChecker(passport_mrz)

    if not passport_checker_result:
        print("Error: Passport was invalid!")
        sys.exit(1)

    return create_dict_from_result(passport_checker_result.fields())


if __name__ == "__main__":

    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument(
        "-1", "--line-1", type=str, help="The first line of the passport text")
    argparse_parser.add_argument(
        "-2", "--line-2", type=str, help="The second line of the passport text")

    argparse_parser.add_argument(
        "-t", "--text", type=str, help="The full text of the passport MRZ. Do not use this in conjunction with any other options.")

    # TODO
    argparse_parser.add_argument(
        "-i", "--image", type=str, help="The text image to parse passport MRZ from. Do not use this in conjunction with any other options")

    argparse_args = argparse_parser.parse_args()

    if argparse_args.line_1 and argparse_args.line_2:

        if len(argparse_args.line_1) == PASSPORT_MRZ_LINE_LENGTH and len(argparse_args.line_2) == PASSPORT_MRZ_LINE_LENGTH:
            result = decode_passport_mrz(
                f"{argparse_args.line_1}\n{argparse_args.line_2}")
            print(result)

        else:
            print(
                f"[ERROR] Either line 1 or line 2 were of incorrect length -- check that both strings have the length of {PASSPORT_MRZ_LINE_LENGTH}")

    elif os.path.exists(argparse_args.image):

        mrz_lines_from_img = extract_mrz_from_passport_image(
            argparse_args.image)

        result = decode_passport_mrz(
            f"{mrz_lines_from_img[0]}\n{mrz_lines_from_img[1]}")
