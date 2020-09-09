import re
import requests
from retry import retry
from logging import warning, info
from utilities import constants


class Http:

    def __init__(self, session_builder):
        self.session = session_builder()

    @retry(requests.exceptions.ConnectionError or requests.exceptions.Timeout, delay=constants.Requests.retry_delay(),
           backoff=constants.Requests.retry_backoff(), tries=constants.Requests.retry_max_tries())
    def __get__(self, url):
        response = self.session.get(url, timeout=10)
        # rate limiting headers do not exist for all responses (i.e. cached responses)
        observed_header = "ratelimit-observed"
        limit_header = "ratelimit-limit"
        if observed_header and limit_header in response.headers.keys():
            self.__log_rate_limit_info__(response.headers[observed_header],
                                         response.headers[limit_header])

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
    def __log_rate_limit_info__(observed, limit):
        if (int(observed)/int(limit)) >= .9:
            info("[*] Rate Limit Usage: (%s/%s)", observed, limit)
