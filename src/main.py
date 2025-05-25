import argparse
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

NAME_TO_GENDER_PROBABILITY_CSV = pathlib.Path(
    "../src/irs990_parser/first_name_gender_probabilities.csv"
)


def get_year_from_url(url: str) -> int:
    """Retrieve year from IRS URL

    :param url: A URL that leads to an IRS asset
    :type url: str
    :return: The year within the URL
    :rtype: int
    """
    return int(url.split("/")[7])


def get_irs_month_from_url(url: str) -> str:
    """Retrieve month from IRS URL. The month will be the number on the
    Julian calendar appended by an A.

    :param url: A URL that leads to an IRS asset
    :type url: str
    :return: The irs month within the URL
    :rtype: str
    """
    separate_by_forward_slash = url.split("/")
    separate_by_underscore = separate_by_forward_slash[-1].split("_")
    separate_by_period = separate_by_underscore[-1].split(".")
    return separate_by_period[0]


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--start-year", type=int, required=True)
    arg_parser.add_argument("--end-year", type=int, required=True)
    arg_parser.add_argument("--credentials-file", type=str, required=True)
    args = arg_parser.parse_args()

    start_year = args.start_year
    end_year = args.end_year
    credentials_file = pathlib.Path(args.credentials_file)
    irs_990_links = link_retriever.IRS990LinkRetriever(
        start_year, end_year
    ).get_zip_links()

    guesser = gender_guesser.GenderGuesser(NAME_TO_GENDER_PROBABILITY_CSV)

    data_loader = loader.Loader(credentials_file)

    for url in irs_990_links:
        irs_month = get_irs_month_from_url(url)
        year = get_year_from_url(url)
        with tempfile.TemporaryDirectory() as temp_dir_path:
            zip_file_extractor = extractor.IRSZipFileExtractor()

            # zip file directory (irs_990_dir) > the only file unzipped (directory_containing_xml_files) > xml files
            irs_990_dir = zip_file_extractor.extract_zip(
                url, pathlib.Path(temp_dir_path)
            )
            directory_containing_xml_files = os.listdir(irs_990_dir)[0]
            xml_files_dir = os.path.join(irs_990_dir, directory_containing_xml_files)

            monthly_org_data = []
            for xml_file_name in tqdm.tqdm(os.listdir(xml_files_dir)):
                xml_file_path = os.path.join(xml_files_dir, xml_file_name)
                with open(xml_file_path, "r", encoding="utf-8") as f:
                    xml_file = f.read()
                    file_name = os.path.basename(xml_file)
                    parsed_xml = bs4.BeautifulSoup(xml_file, "xml")

                    ein = irs_field_extractor.EINEXtractor(
                        file_name, parsed_xml
                    ).extract()

                    org_name = irs_field_extractor.OrgNameExtractor(
                        file_name, parsed_xml
                    ).extract()

                    whistleblower_policy = (
                        irs_field_extractor.WhistleblowerPolicyExtractor(
                            file_name, parsed_xml
                        )
                    ).extract()

                    ceo_compensation_review = (
                        irs_field_extractor.CEOCompensationReviewExtractor(
                            file_name, parsed_xml
                        ).extract()
                    )

                    other_compensation_review = (
                        irs_field_extractor.OtherCompensationReviewExtractor(
                            file_name, parsed_xml
                        ).extract()
                    )

                    trustee_stuff = irs_field_extractor.TrusteeExtractor(
                        file_name, parsed_xml, guesser
                    )

                    key_employer_stuff = irs_field_extractor.KeyEmployeeExtractor(
                        file_name, parsed_xml, guesser
                    )

                    org_data = irs_field_extractor.OrganizationDataModel(
                        ein=ein,
                        instnm=org_name,
                        irs_month=irs_month,
                        year=year,
                        percentage_women_trustees=trustee_stuff.calculate_trustee_female_percentage(),
                        percentage_women_key_employees=key_employer_stuff.calculate_key_employee_female_percentage(),
                        whistleblower_policy=whistleblower_policy,
                        ceo_reviewed_compensation=ceo_compensation_review,
                        other_reviewed_compensation=other_compensation_review,
                        male_to_female_pay_ratio=key_employer_stuff.calculate_male_to_female_pay_ratio(),
                        president_to_average_pay_ratio=key_employer_stuff.calculate_president_to_average_pay_ratio(),
                    )
                    monthly_org_data.append(org_data)

            data_loader.load_into_db(monthly_org_data)
