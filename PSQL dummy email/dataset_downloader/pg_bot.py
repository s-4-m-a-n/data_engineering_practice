import psycopg2
import os
# config
HOST = "139.162.7.175"
DB = "nthrow_db"
USER = "nthrow_reader"
PASSWORD = "nthrow_reader_pw"
PORT = "5433"
OUTPUT_FILE_PATH = "../"

# downloaders
def downloader(cursor,query,file_name):
    print(f"building {file_name}")
    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
    file_path = os.path.join(OUTPUT_FILE_PATH, file_name)
    
    with open(file_path, 'w') as f:
        cursor.copy_expert(outputquery, f)



def run():
    """Downloads email, phone and social link into csv format from pg """
    #queries
    social_query = "select jsonb_array_elements(data->\
                                                'full'->'profile')->>'entity'\
                                                as primary_social from sites_2"

    phone_query = "select data#>'{phone,primary}' as primary_phone ,\
                   data#>'{phone,secondary}' as secondary_phone\
                    from sites_2 where data#>'{phone,primary}' !='[]'\
                     OR data#>'{phone,secondary}' != '[]'"

    email_query = " select data#>'{email,primary}' as primary_email ,\
                     data#>'{email,secondary}' as secondary_email\
                    from sites_2 where data#>'{email,primary}' !='[]'\
                     OR data#>'{email,secondary}' != '[]'"

    # connection establish
    con = None
    cursor = None
    try:
        con = psycopg2.connect(host=HOST, database=DB, user=USER, password=PASSWORD, port=PORT)
        cursor = con.cursor()

        downloader(cursor, email_query,"email.csv")
        downloader(cursor, phone_query, "phone.csv")
        downloader(cursor, social_query, "social.csv")
        
        cursor.close()
        con.close()
    except Exception as e:
        print(f"status: oops!! error => {e}")

    finally :
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()

    print("status: successfully downloaded")


if __name__ == "__main__":
    run()
