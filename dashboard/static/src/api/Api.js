function buildUrl(endpoint) {
    return "http://127.0.0.1:5000/" + endpoint;
}

export function getGeoSentiment() {
    return fetch(buildUrl("geo"))
        .then(response => response.json());
}

export function getTrends(timestamp, mode, limit) {
    const modeMap = {
        'week': 'W',
        'month': 'M',
        'year': 'Y'
    };

    return fetch(buildUrl(`trends?date=${Math.floor(timestamp.getTime() / 1000)}&limit=${limit}&mode=${modeMap[mode]}`))
        .then(response => response.json());
}

export function getOpinion(query) {
    return fetch(buildUrl(`opinion?text=${query}`))
        .then(response => response.json());
}

export function getPages(limit) {
    return fetch(buildUrl(`onions?limit=${limit}`))
        .then(response => response.json());
}

export function getTextBlocks(pageUrl) {
    return fetch(buildUrl(`textBlocks?url=${pageUrl}`))
        .then(response => response.json());
}

export function postSearch(query) {
    return fetch(buildUrl('seed'), {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({ query })
    }).then(response => response.json());
}
