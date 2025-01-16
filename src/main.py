import argparse
import logging
import os
import pathlib
import tempfile

import bs4
import tqdm

from irs990_parser import (
    extractor,
    gender_guesser,
    irs_field_extractor,
    link_retriever,
    loader,
)


def get_start_and_end_years():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--start-year", type=int, required=True)
    arg_parser.add_argument("--end-year", type=int, required=True)
    args = arg_parser.parse_args()

    return args.start_year, args.end_year


def get_year_from_url(url: str) -> int:
    return int(url.split("/")[7])


def store_bad_file(bad_files_dir: pathlib.Path, xml_string: str) -> None:
    with open(bad_files_dir, "w") as b:
        b.write(xml_string)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)

    bad_files_dir = pathlib.Path("bad_files")

    start_year, end_year = get_start_and_end_years()
    irs_990_links = link_retriever.IRS990LinkRetriever(
        start_year, end_year
    ).get_zip_links()

    guesser = gender_guesser.GenderGuesser(
        pathlib.Path("../src/irs990_parser/first_name_gender_probabilities.csv")
    )

    data_loader = loader.Loader(pathlib.Path("/home/rhit-shirakrk/db_config.ini"))

    for url in irs_990_links:
        year = get_year_from_url(url)
        with tempfile.TemporaryDirectory() as temp_dir_path:
            zip_file_extractor = extractor.IRSZipFileExtractor()
            irs_990_dir = zip_file_extractor.extract_zip(
                url, pathlib.Path(temp_dir_path)
            )
            print(f"Processing files for {os.path.basename(irs_990_dir)}")

            monthly_org_data = []
            for file in tqdm.tqdm(os.listdir(irs_990_dir)):
                with open(os.path.join(irs_990_dir, file), "r", encoding="utf-8") as f:
                    xml_file = f.read()
                    file_name = os.path.basename(xml_file)
                    parsed_xml = bs4.BeautifulSoup(xml_file, "xml")

                    try:
                        ein = irs_field_extractor.EINEXtractor(
                            file_name, parsed_xml
                        ).extract()
                    except:
                        logging.error(
                            f"File {file} in {irs_990_dir} had an error extracting ein"
                        )
                        store_bad_file(bad_files_dir, xml_file)
                        continue

                    try:
                        org_name = irs_field_extractor.OrgNameExtractor(
                            file_name, parsed_xml
                        ).extract()
                    except:
                        logging.error(
                            f"File {file} in {irs_990_dir} had an error extracting org name"
                        )
                        store_bad_file(bad_files_dir, xml_file)
                        continue

                    try:
                        whistleblower_policy = (
                            irs_field_extractor.WhistleblowerPolicyExtractor(
                                file_name, parsed_xml
                            )
                        ).extract()
                    except:
                        logging.error(
                            f"File {file} in {irs_990_dir} had an error extracting whistleblower policy"
                        )
                        store_bad_file(bad_files_dir, xml_file)
                        continue

                    try:
                        ceo_compensation_review = (
                            irs_field_extractor.CEOCompensationReviewExtractor(
                                file_name, parsed_xml
                            ).extract()
                        )
                    except:
                        logging.error(
                            f"File {file} in {irs_990_dir} had an error extracting ceo compensation review"
                        )
                        store_bad_file(bad_files_dir, xml_file)
                        continue

                    try:
                        other_compensation_review = (
                            irs_field_extractor.OtherCompensationReviewExtractor(
                                file_name, parsed_xml
                            ).extract()
                        )
                    except:
                        logging.error(
                            f"File {file} in {irs_990_dir} had an error extracting other compensation review"
                        )
                        store_bad_file(bad_files_dir, xml_file)
                        continue

                    trustee_info = irs_field_extractor.TrusteeExtractor(
                        file_name, parsed_xml, guesser
                    )
                    try:
                        percentage_women_trustees = (
                            trustee_info.calculate_trustee_female_percentage()
                        )
                    except:
                        logging.error(
                            f"File {file} in {irs_990_dir} had an error extracting percentage women trustees"
                        )
                        store_bad_file(bad_files_dir, xml_file)
                        continue

                    key_employer_info = irs_field_extractor.KeyEmployeeExtractor(
                        file_name, parsed_xml, guesser
                    )
                    try:
                        percentage_women_key_employees = (
                            key_employer_info.calculate_key_employee_female_percentage()
                        )
                    except:
                        logging.error(
                            f"File {file} in {irs_990_dir} had an error extracting percentage women key employees"
                        )
                        store_bad_file(bad_files_dir, xml_file)
                        continue

                    try:
                        male_to_female_pay_ratio = (
                            key_employer_info.calculate_male_to_female_pay_ratio()
                        )
                    except:
                        logging.error(
                            f"File {file} in {irs_990_dir} had an error extracting male to female ratio"
                        )
                        store_bad_file(bad_files_dir, xml_file)
                        continue

                    try:
                        president_to_average_pay_ratio = (
                            key_employer_info.calculate_president_to_average_pay_ratio()
                        )
                    except:
                        logging.error(
                            f"File {file} in {irs_990_dir} had an error extracting president to average ratio"
                        )
                        store_bad_file(bad_files_dir, xml_file)
                        continue

                    org_info = irs_field_extractor.OrganizationDataModel(
                        ein=ein,
                        instnm=org_name,
                        year=year,
                        percentage_women_trustees=percentage_women_trustees,
                        percentage_women_key_employees=percentage_women_key_employees,
                        whistleblower_policy=whistleblower_policy,
                        ceo_reviewed_compensation=ceo_compensation_review,
                        other_reviewed_compensation=other_compensation_review,
                        male_to_female_pay_ratio=male_to_female_pay_ratio,
                        president_to_average_pay_ratio=president_to_average_pay_ratio,
                    )
                    monthly_org_data.append(org_info)

            data_loader.load_into_db(monthly_org_data)
