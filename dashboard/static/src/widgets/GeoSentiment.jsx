import React from 'react';
import { Header, Segment } from 'semantic-ui-react';
import { Map, Marker, Popup, TileLayer } from 'react-leaflet';

export default class GeoSentiment extends React.Component {
    render() {
        return (
            <Segment className="widget" raised>
                <Header as='h3'>Geographical Sentiment</Header>
                <Map id="geo-sentiment-map" center={[34.5, -94.16]} zoom={1}>
                    <TileLayer
                        url='http://{s}.tile.osm.org/{z}/{x}/{y}.png'
                        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors' />
                </Map>
            </Segment>
        );
    }
}
