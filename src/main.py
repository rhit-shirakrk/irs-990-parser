import argparse
import os
import pathlib
import tempfile

import bs4

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


if __name__ == "__main__":
    start_year, end_year = get_start_and_end_years()
    irs_990_links = link_retriever.IRS990LinkRetriever(
        start_year, end_year
    ).get_zip_links()

    for url in irs_990_links:
        year = get_year_from_url(url)
        with tempfile.TemporaryDirectory() as temp_dir_path:
            zip_file_extractor = extractor.IRSZipFileExtractor()
            irs_990_dir = zip_file_extractor.extract_zip(
                url, pathlib.Path(temp_dir_path)
            )
            print(f"Processing files for {os.path.basename(irs_990_dir)}")

            monthly_org_data = []
            for file in os.listdir(irs_990_dir):
                print(f"Processing file {file}")
                with open(os.path.join(irs_990_dir, file), "r", encoding="utf-8") as f:
                    xml_file = f.read()
                    file_name = os.path.basename(xml_file)
                    parsed_xml = bs4.BeautifulSoup(xml_file, "xml")

                    ein = irs_field_extractor.EINEXtractor(file_name, parsed_xml)

                    org_name = irs_field_extractor.OrgNameExtractor(
                        file_name, parsed_xml
                    )

                    total_compensation = irs_field_extractor.TotalCompensationExtractor(
                        file_name, parsed_xml
                    )

                    total_employees = irs_field_extractor.TotalEmployeesExtractor(
                        file_name, parsed_xml
                    )

                    whistleblower_policy = (
                        irs_field_extractor.WhistleblowerPolicyExtractor(
                            file_name, parsed_xml
                        )
                    )

                    ceo_compensation_review = (
                        irs_field_extractor.CEOCompensationReviewExtractor(
                            file_name, parsed_xml
                        )
                    )

                    other_compensation_review = (
                        irs_field_extractor.OtherCompensationReviewExtractor(
                            file_name, parsed_xml
                        )
                    )

                    guesser = gender_guesser.GenderGuesser(
                        pathlib.Path(
                            "../src/irs990_parser/first_name_gender_probabilities.csv"
                        )
                    )
                    trustee_stuff = irs_field_extractor.TrusteeExtractor(
                        file_name, parsed_xml, guesser
                    )

                    key_employer_stuff = irs_field_extractor.KeyEmployeeExtractor(
                        file_name, parsed_xml, guesser
                    )

                    org_info = irs_field_extractor.OrganizationDataModel(
                        ein=ein.extract(),
                        instnm=org_name.extract(),
                        year=year,
                        percentage_women_trustees=trustee_stuff.calculate_trustee_female_percentage(),
                        percentage_women_key_employees=key_employer_stuff.calculate_key_employee_female_percentage(),
                        ceo_reviewed_compensation=ceo_compensation_review.extract(),
                        other_reviewed_compensation=other_compensation_review.extract(),
                        male_to_female_pay_ratio=key_employer_stuff.calculate_male_to_female_pay_ratio(),
                        president_to_average_pay_ratio=key_employer_stuff.calculate_president_to_average_pay_ratio(),
                    )
                    monthly_org_data.append(org_info)

            data_loader = loader.Loader(monthly_org_data)
            data_loader.load_into_db(pathlib.Path("/home/rhit-shirakrk/db_creds.ini"))
