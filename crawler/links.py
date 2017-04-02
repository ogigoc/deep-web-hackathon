import requests
import crawler.CONSTANTS as CONST

extensions_file = open('unknown_extensions.ogi', 'a')

def url_priority(url):
    return 50000 if '?' not in url else 100000

def parse_link(l, url):
    sol = ""

    #leads to the same page
    if l.startswith('http://') or l.startswith('https://'):
        sol = l
    elif l.startswith('//'):
        if url.startswith('http://'):
            sol = 'http://' + l[2:]
        elif url.startswith('https://'):
            sol = 'https://' + l[2:]
    elif l[0] == '/':
        sol = base(url) + l[1:]
    elif l[0] == '?':
        i = l.rfind('/')
        if i == -1:
            sol = ""
        else:
            sol = l[:i + 1] + l
    else:
    	sol = ""

    if len(sol) > 255:
        sol = ""
    """
    if sol != "":
            regex = re.compile(r'\.([^/?=.]+)$')
            ex = regex.search(l)

            if ex and ex.group() not in CONSTANTS.ALLOWED_EXTENSIONS:
                    print(l.encode('utf-8'), file = f_ignored_urls)
                    return ""
    """
    return sol

def filter_invalid(links):
    good_links = [link for link in links if (link.startswith('http://') or link.startswith('https://')) \
    and '.onion' in link and link.split('.')[-1] not in CONST.IGNORED_EXTENSIONS]
    good_links = [link.split('#')[0] for link in good_links]

    for l in good_links:
        e = l.split('.')[-1]
        if len(e) < 7:
            print(e, file = extensions_file)

    return good_links

def filter_links(links, url):
    good_links = []
    for l in links:
            new_url = parse_link(l, url)
            if new_url != "":
                    good_links.append(new_url)
    return filter_invalid(good_links)

def base(url):
    pos = url.find('.onion')
    if pos == -1:
        return url
    else:
        return url[:pos + 7]