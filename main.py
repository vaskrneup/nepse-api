import requests
import datetime
from bs4 import BeautifulSoup


# UTILS FUNCTIONS !!
def datetime_range(start, end):
    single_day_time_delta = datetime.timedelta(days=1)

    while start < end:
        yield start
        start = start + single_day_time_delta


# MAIN SECTION !!
class NepseApi:
    """
        "date"
        "time"
        "sn"
        "traded_companies"
        "no_of_transaction"
        "max_price"
        "min_price"
        "closing_price"
        "traded_shares"
        "amount"
        "previous_closing"
        "difference"
    """

    def __init__(self, base_url="http://nepalstock.com.np/todaysprice",
                 default_params="startDate={YEAR}-{MONTH}-{DAY}&stock-symbol=&_limit=500"):
        self.base_url = base_url
        self.default_params = default_params

    def get_data_url(self, date: datetime.date) -> str:
        share_params = {
            "YEAR": str(date.year),
            "MONTH": str(date.month),
            "DAY": str(date.day)
        }
        return f"{self.base_url}?{self.default_params.format(**share_params)}"

    def get_resp_for_date(self, date: datetime.date) -> requests.get:
        return requests.get(self.get_data_url(date))

    def get_soup_for_date(self, date: datetime.date) -> BeautifulSoup:
        resp = self.get_resp_for_date(date)
        return BeautifulSoup(resp.text, "lxml")

    def get_company_data_for_date(self, date: datetime.date):
        company_soup = self.get_soup_for_date(date)
        table_data = company_soup.select("table.table-condensed tr")
        date = f"{date.year}-{date.month}-{date.day}"
        time = "15:00:00"  # TODO: update with real time !!

        return (
            self.parse_share_main_data(table_data[2:-5], date, time),
            self.parse_share_aggregate_data(table_data[-3:], date, time)
        )

    def get_company_data_for_date_range(self, start_date: datetime.date, end_date: datetime.date) -> iter:
        """
        yields the data !!
        """
        for date in datetime_range(start_date, end_date):
            yield self.get_company_data_for_date(date)

    def parse_share_main_data(self, data, *args):
        return [
            [*args, *(
                self.check_and_make_float(stock_data.text.replace(",", "").strip()) for stock_data in
                company.select("td")
            )]
            for company in data
        ]

    def parse_share_aggregate_data(self, data, *args):
        return [
            *args, *(
                self.check_and_make_float(company.select("td")[1].text.strip().replace(",", ""))
                for company in data
            )
        ]

    @staticmethod
    def check_and_make_float(x) -> (str, float):
        try:
            return float(x)
        except ValueError:
            return x


if __name__ == "__main__":
    nepse_api = NepseApi()

    print(
        list(
            (
                nepse_api.get_company_data_for_date_range(
                    datetime.datetime.now() - datetime.timedelta(days=10),
                    datetime.datetime.now()
                )
            )
        )
    )
