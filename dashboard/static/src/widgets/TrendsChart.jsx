import React from 'react';
import * as moment from 'moment';
import { XYPlot, HorizontalGridLines, LineSeries, XAxis, YAxis } from 'react-vis';

export default class TrendsChart extends React.Component {
    computeData(dates) {
        var dateCounts = {};
        for (const date of dates) {
            const timestamp = date.getTime();
            if (typeof dateCounts[timestamp] === "undefined") {
                dateCounts[timestamp] = 1;
            } else {
                dateCounts[timestamp]++;
            }
        }

        let result = [];
        for (const timestamp in dateCounts) {
            result.push({
                x: new Date(parseInt(timestamp)),
                y: dateCounts[timestamp],
            });
        }
        result.sort((a, b) => a.x - b.x);

        return result;
    }

    render() {
        const { data } = this.props;

        return (
            <XYPlot
                xType='time-utc'
                width={400}
                height={550}>
                <HorizontalGridLines />
                {data.map((series, i) =>
                    <LineSeries key={i} color={series.color} data={this.computeData(series.dates)} />
                )}
                <XAxis />
                <YAxis />
            </XYPlot>
        );
    }
}
