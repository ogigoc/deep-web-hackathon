import React from 'react';

export default class LegendColor extends React.Component {
    render() {
        const { show, color } = this.props;

        let className = 'legend';
        if (show) {
            className += ' show';
        }

        return (
            <div className={className} style={{backgroundColor: color}}></div>
        );
    }
}
