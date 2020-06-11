

import re
import importlib.util

from project.app.MySqlCon import MySqlCon
from MySqlCon import MySqlCon



class Variant():
    """Object representing an allele. The object contains the following attributes:
        chromosome (string): chromosome the allele is located on. E.g. 'Y' or '12'
        position (int): location on chromosome
        reference (string): nucleotide before mutation
        alternative (string): nucleotide(s) after mutation
        total_alleles (int): number of times the mutation has been observed in the population
        allele_frequency (float): observed frequemcy of the mutation within the population
        variant_type (string): type of mutation
        allele_type (string): type of mutation
        non_cancer_total_alleles (int): number of observed patients with the allele but without cancer
    """
    def __init__(self, chromosome, position, reference, alternative, total_alleles, allele_frequency,
                 variant_type, allele_type, non_cancer_total_alleles):
        self.__chromosome = chromosome
        self.__position = position
        self.__reference = reference
        self.__alternative = alternative
        self.__total_alleles = total_alleles
        self.__allele_frequency = allele_frequency
        self.__variant_type = variant_type
        self.__allele_type = allele_type
        self.__non_cancer_total_alleles = non_cancer_total_alleles

    def get_chromosome(self):
        return self.__chromosome

    def get_position(self):
        return self.__position

    def get_reference(self):
        return self.__reference

    def get_alternative(self):
        return self.__alternative

    def get_total_alleles(self):
        return self.__total_alleles

    def get_allele_frequency(self):
        return self.__allele_frequency

    def get_variant_type(self):
        return self.__variant_type

    def get_allele_type(self):
        return self.__allele_type

    def get_non_cancer_total_alleles(self):
        return self.__non_cancer_total_alleles


def main():
    # the following must happen, read in the file using a generator. Doing this per line is fine.
    # then check if it is not a comment, if not, check the frequency, should be lower than 1%. if so,
    # initialize Variant object and save data in it. Save the object in a list. When completed write data away
    # to a new file.
    path = "gnomad.exomes.r2.1.1.sites.Y.vcf"
    possible_pathogenic_variant_list = read_vcf_file(path)
    print("the amount of saved entries: " + str(len(possible_pathogenic_variant_list)))

    write_to_db(possible_pathogenic_variant_list)


def read_vcf_file(path):
    """Method for reading gnomAD VCF files containing allele data

    Args:
        path (string): path to VCF file

    Returns:
        list: list of allele objects that are possibly pathogenic, as they 1) occur in <1% of the population
              and 2) occur in patients with cancer
    """
    possible_pathogenic_variant_list = []
    is_done = False
    generator = read_line(path)
    try:
        while not is_done:
            line = next(generator)
            if is_comment(line) == False and is_potential_malignent(line) == True:
                possible_pathogenic_variant = create_Variant_object(line)
                possible_pathogenic_variant_list.append(possible_pathogenic_variant)
    except StopIteration:
        return possible_pathogenic_variant_list


def read_line(path):
    """Method creating a generator object for parsing a file

    Args:
        path (string): path to the file that is to be parsed

    Yields:
        string: line of file
    """
    for line in open(path):
        yield line.strip()


def is_comment(line):
    """Method for checking if a line is a comment (starts with #)

    Args:
        line (string): line of file

    Returns:
        boolean: True if line is a comment, False if it is not
    """
    if line.startswith("#"):
        return True
    else:
        return False


def is_potential_malignent(line):
    """Method for checking if a line containing allele information is possibly malignent

    Args:
        line (string): line of file to be checked

    Returns:
        boolean: True if allele is possibly malignent (occurs in <1% of population and patients with cancer have been observed to have this mutation)
    """
    variant_frequency = re.search("(AF=)([0-9]\.[0-9]*e\-[0-9]*|[0-9]\.[0-9]*)", line)
    # check if the variant has 0 users
    if None == variant_frequency:
        return False
    # check if the variant is possibly malignent
    if float(variant_frequency.group().split("=")[1]) <= 1.0:
        if int(int(re.search("(AN=)[0-9]*", line).group().split("=")[1]) - int(re.search("(non_cancer_AN=)[0-9]*", line).group().split("=")[1])) > 0:
            return True
    else:
        return False

def create_Variant_object(line):
    """Method for parsing a line containing allele information to a "Variant" object

    Args:
        line (string): line of VCF file containing allele information

    Returns:
        Variant: "Variant" object containing allele information
    """
    return Variant(line.split("\t")[0],
                   line.split("\t")[1],
                   line.split("\t")[3],
                   line.split("\t")[4],
                   re.search("(AN=)[0-9]*", line).group().split("=")[1],
                   re.search("(AF=)([0-9]\.[0-9]*e\-[0-9]*|[0-9]\.[0-9]*)", line).group().split("=")[1],
                   re.search("(variant_type=)([a-z-A-Z]*\-[a-zA-Z]*|[a-zA-Z]*)", line).group().split("=")[1],
                   re.search("(allele_type=)([a-z-A-Z]*\-[a-zA-Z]*|[a-zA-Z]*)", line).group().split("=")[1],
                   re.search("(non_cancer_AN=)[0-9]*", line).group().split("=")[1])



def write_to_db(ppvl):
    """Method for writing a list of "Variant" objects to the MySQL database

    Args:
        ppvl (list): list of "Variant" objects containing allele information
    """
    con = MySqlCon()
    query = 'INSERT INTO alleleDB.alleleVariants (chromosome, position, reference, alternative, total_alleles, allele_frequency, variant_type, allele_type, non_cancer_total_alleles) ' +\
            'VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8});'

    for variant in ppvl:
        print(query.format('\'' + variant.get_chromosome() + '\'', variant.get_position(), '\'' + variant.get_reference() + '\'', '\'' + variant.get_alternative() + '\'', variant.get_total_alleles(),
                                        '\'' + variant.get_allele_frequency() + '\'', '\'' + variant.get_variant_type() + '\'', '\'' + variant.get_allele_type() + '\'', variant.get_non_cancer_total_alleles()))
        con.execute_no_res(query.format('\'' + variant.get_chromosome() + '\'', variant.get_position(), '\'' + variant.get_reference() + '\'', '\'' + variant.get_alternative() + '\'', variant.get_total_alleles(),
                                        '\'' + variant.get_allele_frequency() + '\'', '\'' + variant.get_variant_type() + '\'', '\'' + variant.get_allele_type() + '\'', variant.get_non_cancer_total_alleles()))
    con.close()




main()
