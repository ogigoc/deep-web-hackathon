import React from 'react';
import { Loader, Dimmer, Header, Segment } from 'semantic-ui-react';
import { Tooltip, CircleMarker, Map, Marker, Popup, TileLayer } from 'react-leaflet';
import { getGeoSentiment } from '../api/Api.js';

import GeoSentimentPopup from './GeoSentimentPopup.jsx';

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function blendHex(a, b, alpha) {
    let result = [ 0, 0, 0 ];
    for (let i = 0; i < 3; i++) {
        result[i] = Math.floor(b[i] * alpha) + Math.floor(a[i] * (1.0 - alpha));
    }

    return rgbToHex(result[0], result[1], result[2]);
}

function getColor(sentiment) {
    const negative = [ 170, 0, 0 ],
        neutral = [ 255, 190, 0 ],
        positive = [ 0, 170, 0 ];

    if (sentiment < 0) {
        return blendHex(negative, neutral, 1.0 - Math.abs(sentiment));
    } else {
        return blendHex(neutral, positive, sentiment);
    }
}

export default class GeoSentiment extends React.Component {
    constructor() {
        super();
        this.state = {
            loading: true,
            geo: []
        };
    }

    fetchData() {
        this.setState({
            loading: true
        });

        getGeoSentiment()
            .then(response => {
                this.setState({
                    geo: response,
                    loading: false
                });
            });
    }

    componentWillMount() {
        this.fetchData();
    }

    render() {
        const { geo, loading } = this.state;

        return (
            <Segment className="widget" raised>
                <Header as='h3'>Geographical Sentiment</Header>
                <Map id="geo-sentiment-map" center={[34.5, -94.16]} zoom={1}>
                    <TileLayer
                        url='http://{s}.tile.osm.org/{z}/{x}/{y}.png'
                        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors' />
                    {geo.map(country => (
                        <CircleMarker
                            key={country.name}
                            center={{lat: country.lat, lng: country.lng}}
                            stroke={false}
                            fill={true}
                            fillColor={getColor(country.sentiment)}
                            radius={Math.abs(country.sentiment) * 10 + 10}
                            fillOpacity={0.9}
                        >
                            <GeoSentimentPopup country={country} />
                        </CircleMarker>
                    ))}
                </Map> <Dimmer inverted active={loading}>
                    {loading ? <Loader /> : null}
                </Dimmer>
            </Segment>
        );
    }
}
