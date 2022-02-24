from random import expovariate
import psycopg2
import pandas as pd
import os
from datetime import date, timedelta
from pathlib import Path

def creativepull(bundle_id):
    def pull_from_redshift(query):
        """
        Executes a SQL query on Redshift and returns a Pandas DataFrame.
        :param query: the query to be executed, as a str type.
        """
        conn_redshift = psycopg2.connect(dbname='tm_data_warehouse',
                                        host='10.0.66.4', port='5439', user='solution.engineering', password='nKsdk4MCQf')
        cursor = conn_redshift.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        headers = []
        for item in cursor.description:
            headers.append(item[0])
        df = pd.DataFrame(data, columns=headers)
        return df
    
    yesterdays_date = date.today() - timedelta(days = 1)
    query = """
    select
        fci.campaign_id,
        fci.creative_id,
        sum(fci.client_cost) as Status
    from
        fact_campaign_insights fci
        inner join dim_campaign dc on fci.campaign_id = dc.campaign_id
    where
        date_action = '"""+ str(yesterdays_date) + """'
        and dc.bundle_identifier in ("""+ str(bundle_id) + """)
    group by
    1,2
    having
        Status > 0.1
    """
    df_live = pull_from_redshift(query)
    df_live = df_live.rename(columns={'campaign_id' : 'Campaign ID', 'creative_id' : 'Creative ID', 'status' : 'Status'})
    return df_live
