import React from 'react';
import { Popup } from 'react-leaflet';

export default class GeoSentimentPopup extends React.Component {
    render() {
        const { name, sentiment, num_occ } = this.props.country;

        return (
            <Popup>
                <div>
                    <div className="tooltip-title">{name}</div>
                    <div className="tooltip-label">Sentiment</div>
                    <div className="tooltip-entry">{Math.round(Math.abs(sentiment) * 100 * 100) / 100 + "% " + (sentiment < 0 ? 'negative' : 'positive')}</div>
                    <br />
                    <div className="tooltip-label">Occurences</div>
                    <div className="tooltip-entry">{num_occ}</div>
                </div>
            </Popup>
        );
    }
}
