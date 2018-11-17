# Web page Downloader

import sys
import urllib.request
import urllib.error
import re
import os
import argparse
# TODO: adding concurrent.futures to do threadingpool and downloading sim

timeout_time = 2
search_level = 1
url = ""
file_formats = ""
files_to_download = set()
save_directory = 'pyGrabber'


def is_sutable_for_download(file, format):
    if file.endswith(format):
        return True
    return False


def get_sutable_links(the_set, format):
    return set(filter(lambda x: is_sutable_for_download(x), the_set))


def find_links_of(url, search_level):
    print('\t' * search_level * (search_level-1) / 2)
    print(url)
    try:
        links = urllib.request.urlopen(url, timeout=timeout_time)
        links = links.read().decode('utf-8', 'ignore')
        link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|\
                        (?:%[0-9a-fA-F][0-9a-fA-F]))+'
        links = re.findall(link_pattern, links)
        links = set(links)
        return links
    except urllib.error.URLError:
        print('\t' * search_level * (search_level-1) / 2)
        print("Passing the link because of URL is unreachable")
        return set()
    except KeyboardInterrupt:
        if input('\nAre you sure you want to quit (y/n)? : ') == 'y':
            sys.exit(0)
        print("Continue:")
        return set()
    except TimeoutError:
        print('\t' * search_level * (search_level-1) / 2)
        print("The read operation timed out")
        return set()


def is_url(__str__):
    if re.match(r'https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})\
                  (?:/[\w&%?#-]{1,300})?', __str__):
        return True
    return False


def url_file_size(url):
    try:
        url_request = urllib.request.urlopen(url, timeout=timeout_time)
        url_meta = url_request.info()
        url_size_in_bytes = url_meta.get(name="Content-Length")
        url_request.close()
        url_size_in_bytes = int(url_size_in_bytes)
        return url_size_in_bytes
    except ValueError as e:
        print("Cannot convert file size into int, there should be a \
               problem in headers")
        print(f"got this error: {e}")
    except TimeoutError as e:
        print(f"request timed out\n{e}")


def partial_download(start: int, end: int, url: str, step: int = 1024*100):
    total_size = end
    response = bytearray()
    current_size = start
    while current_size < total_size:
        if (total_size - current_size) < step:
            step = total_size - current_size
        req = urllib.request.Request(url)
        req.headers['Range'] = f'bytes={current_size}-{current_size + step}'
        with urllib.request.urlopen(req) as server_resp:
            response.append(server_resp.read())
        current_size += step
    return response


def download(link):
    pass
    file_size = url_file_size(link)
    file_size_parted = dict(zip(range(file_size//8), [file_size/8]*file_size//8))
    start_points = []
    for key, value in file_size_parted.items():
        start_points.append(key * value)
    print(start_points)


def downloading(all, reqs, save_dir):
    if len(all) == 0 or len(reqs) == 0:
        print('nothing found')
        sys.exit(0)
    print('from:')
    print(all)
    print('downloading:')
    print(reqs)
    print("total of ", end='')
    print(len(reqs), end='')
    if input("files will be downloaded start download (y/n) ?") == 'y':
        for x in reqs:
            print("downloading : ", end='')
            print(x)
            print('\tas : ', end='')
            print(x[x.rfind("/")+1:] + '\n')
            try:
                urllib.request.urlretrieve(x, save_dir + '/' +
                                           x[x.rfind("/")+1:])
            except urllib.error as e:
                print('Download Failed' + str(e))


def handle_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--format', required=True, type=str,
                        nargs='+', help='list of file formats \
                                        to be downloaded')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.2')
    parser.add_argument('-l', '--level', type=int, choices=range(1, 10),
                        default=1, help='level of searching in websites for \
                        downloading-default is one level search')
    parser.add_argument('-d', '--directory', default=os.path.join(os.getcwd(),
                        'pyGrabber'), help='path to save files')
    parser.add_argument('-u', '--url', required=True, type=str, help='website \
                        url that should be downloaded from')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = handle_arguments()
    url = args.url
    search_level = args.level
    file_formats = args.format
    save_directory = args.directory
    for format in file_formats:
        os.makedirs(os.path.join(save_directory, format), exist_ok=True)

    file_content = {url}
    append_file_content = set()
    all_of_links = set()

    for x in range(search_level):
        all_of_links = all_of_links.union(file_content)
        files_to_download = files_to_download.union(get_sutable_links(
                    file_content, file_formats))
        for y in file_content:
            new_links = find_links_of(y, x)
            append_file_content = append_file_content.union(new_links)

        append_file_content.discard(all_of_links)
        file_content = append_file_content
        append_file_content = set()

# downloading(file_content , files_to_download , save_directory)
    # partial_download(url="http://ipv4.download.thinkbroadband.com/5MB.zip")
# print(handle_arguments())
