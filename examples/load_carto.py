import requests
import http.client

CARTO_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRVNGNZTHAwaThjYn' \
              'VMNkd0LTE0diJ9.eyJodHRwOi8vYXBwLmNhcnRvLmNvbS9hY2NvdW50X2lkIjo' \
              'iYWNfc3RhZ3F6ZTgiLCJodHRwOi8vYXBwLmNhcnRvLmNvbS9hY3RpbmdfYXMiO' \
              'iJhdXRoMHw2M2E0MTM5ODA1M2Y1NmFiMjkxN2RlZmMiLCJpc3MiOiJodHRwczo' \
              'vL2F1dGguY2FydG8uY29tLyIsInN1YiI6IjZ2bHFhaW5NcDJlSmw2UGtIZzR3V' \
              'nZNUkhHR2ZhTko0QGNsaWVudHMiLCJhdWQiOiJjYXJ0by1jbG91ZC1uYXRpdmU' \
              'tYXBpIiwiaWF0IjoxNjcyMjM5MzAwLCJleHAiOjE2NzIzMjU3MDAsImF6cCI6I' \
              'jZ2bHFhaW5NcDJlSmw2UGtIZzR3VnZNUkhHR2ZhTko0Iiwic2NvcGUiOiJyZWF' \
              'kOnRva2VucyB3cml0ZTp0b2tlbnMgcmVhZDppbXBvcnRzIHdyaXRlOmltcG9yd' \
              'HMgcmVhZDpjb25uZWN0aW9ucyB3cml0ZTpjb25uZWN0aW9ucyIsImd0eSI6ImN' \
              'saWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInJlYWQ6dG9rZW5zI' \
              'iwid3JpdGU6dG9rZW5zIiwicmVhZDppbXBvcnRzIiwid3JpdGU6aW1wb3J0cyI' \
              'sInJlYWQ6Y29ubmVjdGlvbnMiLCJ3cml0ZTpjb25uZWN0aW9ucyJdfQ.o8idja' \
              '5RROS25KUp2nhO_EB6dGQmtG8MSZCMNdPwtSFwhISgFLZbKnOxIJdQLTp1NYQW' \
              'wnlwZP6eerKsS5r_mLoOWItKUda9ZeSFC4EXkVcG5hnQMrmgLGmKynLMlVL1EfL' \
              'wOnee60GTxwTh-unVP1Pj_HGhotfYCM9qjR-F82z8lprjlNe_63-cAr0gO7G_Dq' \
              'D5fBCCKktjb2tAyDtOPC3qKxpxw6NcoinIaxtn65LqtQd3cMMABUTCXRl7gjL7Q' \
              'h6vqKYSeH_eRW2t1-9BF0rTmOO8l_VnCMl16t_HeA1gaaOfSmxPwjVvdPdL2-1-' \
              'sGF6S23W9rJ6g3doubxi6Q'


def get_token_for_created_application():
    """
    Example of request to get authorization token for application (when we
    create application in carto service - we are getting "client_id" and
    "client_secret")
    """
    client_id = '6vlqainMp2eJl6PkHg4wVvMRHGGfaNJ4'
    client_secret = 'QFcMEL4dXC0EuOTeghnuqTT_y4msHNEysWNv3uuFdjW2bbSDn55ZJ95P0jeg-dOI'

    conn = http.client.HTTPSConnection("auth.carto.com")
    payload = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&audience=carto-cloud-native-api'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Cookie': 'did=s%3Av0%3A7a695eb0-868d-11ed-9e85-77f10e352eb4.oLHzAEIqlTfLZpvT8pI4gUr3InOf8%2Fz%2FgGwVlALNRX8; did_compat=s%3Av0%3A7a695eb0-868d-11ed-9e85-77f10e352eb4.oLHzAEIqlTfLZpvT8pI4gUr3InOf8%2Fz%2FgGwVlALNRX8'
    }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")

    print(data)
    return eval(data)['access_token']


def get_data_from_carto():
    """ Example how to request data from carto service """
    import requests

    url = "https://gcp-us-east1.api.carto.com/v3/maps/carto_dw/table?name=carto-demo-data.demo_tables.airports"

    payload = {}
    headers = {
        'Authorization': f'Bearer {get_token_for_created_application()}',
        'Cache-Control': 'max-age=300'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    get_data_from_carto()
