function buildUrl(endpoint) {
    return "http://10.120.193.147:5000/" + endpoint;
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
