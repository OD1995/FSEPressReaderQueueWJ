import requests
from MyFunctions import get_df_from_sqlQuery
import logging
import time

while True:
    ## Query PressReaderScrapeQueue to see if any rows are in progress
    Q = """
    SELECT      *
    FROM        PressReaderScrapeQueue
    WHERE       ([Status] = 'In Progress') OR ([Status] IS NULL)
    ORDER BY    RowInsertedDateTime ASC
    """
    df = get_df_from_sqlQuery(
            sqlQuery=Q,
            database="PhotoTextTrack"
        )
    logging.info(f"df shape: {df.shape}")
    inProgressRows = df[df.Status=="In Progress"].shape[0]
    logging.info(f"inProgressRows: {inProgressRows}")
    if inProgressRows == 0:
        ## If not, query PressReaderScrapeQueue for the last added row with no status
        publicationCID = df.loc[0,"PublicationCID"]
        publicationDate = df.loc[0,"PublicationDate"]
        ## Trigger the function to scrape data for that publication/date combination
        params = {
                "publicationCID" : publicationCID,
                "publicationDate" : publicationDate
            }
        logging.info(f"params: {params}")
        r = requests.get(
            url="https://fsepressreaderscraper.azurewebsites.net/api/orchestrators/Orchestrator",
            params=params
        )
    ## Sleep for 10 seconds
    time.sleep(10)