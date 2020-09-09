import re
import requests
from retry import retry
from logging import error, warning
from utilities import constants


class Http:

    def __init__(self, session_builder):
        self.session = session_builder()

    @retry(requests.exceptions.ConnectionError, delay=constants.Requests.retry_delay(),
           backoff=constants.Requests.retry_backoff(), tries=constants.Requests.retry_max_tries())
    def __get__(self, url):
        response = self.session.get(url, timeout=60)
        # rate limiting headers do not exist for all responses
        if "RateLimit-Observed" and "RateLimit-Limit" and "RateLimit-ResetTime" in response.headers.keys():
            self.log_rate_limit_info(response.headers["RateLimit-Observed"],
                                     response.headers["RateLimit-Limit"],
                                     response.headers["RateLimit-ResetTime"])
        return response

    @staticmethod
    def __adjust_paging__(original_url, page_size):
        if "?" not in original_url:
            return original_url + f"?per_page={page_size}"
        return re.sub(r'per_page=?\d{1,2}', f"per_page={page_size}", original_url)

    def get_with_retry_and_paging_adjustment(self, url):
        def log_or_raise_error(error_type, current_page_size, current_url):
            warning(f"[!] {error_type}:  request failed. Adjusting page size to {current_page_size} for GET on {current_url}")
            if page_size <= 1:
                raise e
        for page_size in [20, 10, 5, 1]:
            url = Http.__adjust_paging__(url, page_size)
            try:
                response = self.__get__(url)
            except requests.exceptions.ConnectionError as e:
                log_or_raise_error("ConnectionError", page_size, url)
                continue
            except requests.exceptions.Timeout as e:
                log_or_raise_error("Timeout", page_size, url)
                continue
            return response

    @staticmethod
    def log_rate_limit_info(observed, limit, reset_time):
        if int(observed) == int(limit):
            warning(f"[!] Rate limit observed ({observed}/{limit})!  Reset time: {reset_time}.")
