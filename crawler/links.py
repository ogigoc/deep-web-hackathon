import requests
import crawler.CONSTANTS as CONST

#extensions_file = open('unknown_extensions.ogi', 'a')

def get_url_path(url):
    nodes = url.split('/')[2:] if url.startswith('http') else url.split('/')
    
    paths = []

    for i in range(len(nodes)):
        paths.append('/'.join(nodes[:i+1]))

    return paths

def get_url_base(url):
    return get_url_path(url)[0]

def get_url_depth(url):
    return len(get_url_path(url))

def is_base(url):
    return get_url_depth(url) == 1

def get_link_priority(url, link, utree, prios):
    b = get_url_base(link)
    if is_base(link):
        prios[b] = CONST.BASE_PRIORITY

        if b in utree:
            utree[b] += 1
        else:
            utree[b] = 1
        return CONST.BASE_PRIORITY

    if b in utree:
        utree[b] += 1
    else:
        utree[b] = 1

    if b not in prios:
        prios[b] = CONST.BASE_PRIORITY

    return prios[b] + utree[b] * CONST.PRIORITY_DECREMENT

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

    """
    for l in good_links:
        e = l.split('.')[-1]
        if len(e) < 7:
            print(e, file = extensions_file)
    """

    return good_links

def filter_links(links, url):
    good_links = []
    for l in links:
            new_url = parse_link(l, url)
            if new_url != "":
                    good_links.append(new_url)
    return filter_invalid(good_links)

def base(url):

    if 'redit.com' in url:
        return 'www.reddit.com/r/POLITIC/'

    pos = url.find('.onion')
    if pos == -1:
        return url
    else:
        return url[:pos + 7]