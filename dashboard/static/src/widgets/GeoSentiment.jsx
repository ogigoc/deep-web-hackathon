import React from 'react';
import { Header, Segment } from 'semantic-ui-react';

export default class GeoSentiment extends React.Component {
    render() {
        return (
            <Segment className="widget" raised>
                <Header as='h3'>Geographical Sentiment</Header>
                <div id="geo-sentiment-map"></div>
            </Segment>
        );
    }
}
