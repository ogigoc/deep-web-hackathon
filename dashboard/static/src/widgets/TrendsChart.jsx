import React from 'react';
import * as moment from 'moment';
import { XYPlot, HorizontalGridLines, LineSeries, XAxis, YAxis } from 'react-vis';

export default class TrendsChart extends React.Component {
    computeData(dates) {
        var dateCounts = {};
        for (const date of dates) {
            if (typeof dateCounts[date] === "undefined") {
                dateCounts[date] = 1;
            } else {
                dateCounts[date]++;
            }
        }

        let result = [];
        for (const date in dateCounts) {
            result.push({ x: moment.default(date, "DD.MM.YYYY").toDate(), y: dateCounts[date] });
        }
        result.sort((a, b) => a.x - b.x);

        console.log(result);
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
                (data.map(series =>
                    <LineSeries data={this.computeData(series.dates)} />
                ))
                <XAxis />
                <YAxis />
            </XYPlot>
        );
    }
}
