import mysql.connector

def checkDatabase():
    """
    This function checks if the database exists with the right tables and if not creates them.
    :return:
    """
    config = {
        'user': 'root',
        'password': 'root',
        'port': '3306'
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES LIKE 'alleleDB';")

    if cursor.fetchall():
        cursor.execute('USE alleleDB')
        cursor.execute("SHOW TABLES LIKE 'alleleVariants'")
        if cursor.fetchall():
            pass
        else:
            cursor.execute("""CREATE TABLE alleleVariants (
            chromosome CHAR(100),
            location CHAR(100),
            reference CHAR(100),
            alternative CHAR(100),
            total_alleles CHAR(100),
            allele_frequency CHAR(100),
            variant_type CHAR(100),
            allele_type CHAR(100),
            non_cancer_total_alleles CHAR(100));

            """)

    else:
        cursor.execute('CREATE DATABASE alleleDB')
        cursor.execute('USE alleleDB')
        cursor.execute("""CREATE TABLE alleleVariants (
        chromosome CHAR(100),
        location CHAR(100),
        reference CHAR(100),
        alternative CHAR(100),
        total_alleles CHAR(100),
        allele_frequency CHAR(100),
        variant_type CHAR(100),
        allele_type CHAR(100),
        non_cancer_total_alleles CHAR(100));

        """)

        cursor.close()
        connection.close()