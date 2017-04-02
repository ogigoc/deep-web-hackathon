function buildUrl(endpoint) {
    return "http://10.120.193.147:5000/" + endpoint;
}

export function getTrends(timestamp, mode, limit) {
    const modeMap = {
        'week': 'W',
        'month': 'M',
        'year': 'Y'
    };

    return fetch(buildUrl(`trends?date=${Math.floor(timestamp.getTime() / 1000)}&limit=${limit}&mode=${modeMap[mode]}`))
        .then(function (response) {
            return response.json();
        });
}
