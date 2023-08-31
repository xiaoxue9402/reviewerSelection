from selection.logic.pdf import PDF
from selection.logic.create_candidate_list import extract_refs, create_ref_csv
from selection.logic.merge_operation import merge_references_oaworks
from selection.logic.openalex_matching import rapidfuzz_match
import pandas as pd


#1 Link pdf to openalex
# Extraction and matching

#2 Create candidate list

#3 Select reviewers from candidate list


def pdf_matching(path: str):
    '''
    Input: Path to pdf file.
    Output: List of ids for each reference that was extracted out of the pdf
            and the pdf.
    -> ids (list), pdf (class object)
    '''
    # Extract the references out of the pdf
    pdf = PDF(path)
    extracted_references = pdf.references


    # Load the dataframe with all of the relevant works
    def load_data(path):
        return pd.read_csv(path)

    all_works_df = load_data('../../all_works_sociology.csv')


    # Fuzzymatch the works dataframe with the extracted references -> merge
    id_list = merge_references_oaworks(
        extracted_references=extracted_references,
        openalex_works=all_works_df,
        )

    return id_list, pdf


def candidate_df(id_list: list):
    '''
    Input: Id list of the references.
    Output: Dataframe of works that are candidates for being reviewers.
    -> Every work in references + every cited work inside of the referenced work
    '''

    # Get a list of dictionaries
    # Each dictionary represents on work
    extracted_works = extract_refs(id_list)

    # Turn list of dictionaries into DataFrame
    # columns=["oa_id", "journal_issnl", "authors", "abstracts"]
    candidate_df = create_ref_csv(extracted_works)

    return candidate_df


def select_reviewers(pdf: object, candidate_df: pd.DataFrame):
    '''
    Input: pdf class object and DataFrame with all the candidates
    Output: DataFrame with the top two matched abstracts
    '''

    # Get abstract of pdf
    pdf_abstract = pdf.abstract


    #Turn candidate DataFrame into list of candidate abstracts
    candidate_abstract_list = candidate_df['abstracts']


    # Match pdf abstract with candidate abstracts
    # Get df with top 2 matches
    match_df = rapidfuzz_match(pdf_abstract, candidate_abstract_list)

    return match_df

#Test 1
# matched_pdf = pdf_matching('/home/nklin/code/thisspider/reviewerSelection-data/EXAMPLE_MANUSCRIPT/AJS_2_Sugie2023.pdf')
# print(matched_pdf)

#Test 2
# df = pd.read_csv('/home/nklin/code/thisspider/reviewerSelection/canttype.csv')
# df_as_list = list(df['0'])
# curr_list = candidate_df(df_as_list)
# print(curr_list)
