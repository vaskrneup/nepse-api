# Nepse API

### usage

```
python
nepse_api = NepseApi()

# get data for particular date, must be a datetime.date object
# returns tuple of all share transactions and total transaction for that date
nepse_api.get_company_data_for_date(date:datetime.date)

# get data for range of dates, must be datetime.date object
# returns generator where each value is tuple of  all share transactions and total transaction for particular date
nepse_api.get_company_data_for_date_range(
    start_date:datetime.date, end_date:datetime.date
)
```
