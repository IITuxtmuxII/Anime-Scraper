#!/usr/bin/env python3
import requests
import time
import sys

delay = 0
def retry_on_fail(req, *args, **kwargs):
    global delay
    try:
        if "bakabt" not in args[0]:
            r = req(*args, **kwargs, allow_redirects=True, headers = {'User-agent': 'test'})
        else:
            r = req(*args, **kwargs, allow_redirects=True)
        if r.status_code == 404:
            return None
        if r.status_code not in range(100, 399):
            delay = delay * 2 + 5
            print('Connection error, retrying in {} seconds... '
                  '(HTTP {})'.format(delay, r.status_code), file=sys.stderr)
            if delay > 1800:
                print('Too many retry attempts.')
                exit(code=1)
            time.sleep(delay)
            return retry_on_fail(req, *args, **kwargs)
        else:
            delay = 0
            return r
    except requests.exceptions.RequestException as e:
        delay = delay * 2 + 5
        try:
            print('Connection error, retrying in {} seconds... ({})'.format(delay, e.args[0].args[0]), file=sys.stderr)
        except:
            if 'magnet' in str(e):
                try:
                    if 'magnet' in str(e).split("'")[1] and 'error' not in str(e):
                        return str(e).split("'")[1]
                    else:
                        print('Connection error (2) ({})'.format(e))
                except:
                    exit('CRITICAL: Magnet logic failed!')
            else:
                print('Connection error ({})'.format(e))
        time.sleep(delay)
        return retry_on_fail(req, *args, **kwargs)
    except requests.packages.urllib3.exceptions.ProtocolError as e:
        delay = delay * 2 + 5
        if delay > 1800:
           print('Too many retry attempts.')
           exit(code=1)
        print('Connection error, retrying in {} seconds... '
              '({})'.format(delay, e.args[1]), file=sys.stderr)
        time.sleep(delay)
        return retry_on_fail(req, *args, **kwargs)
