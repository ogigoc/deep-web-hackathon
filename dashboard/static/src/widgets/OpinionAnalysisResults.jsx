import React from 'react';
import { Grid, Statistic } from 'semantic-ui-react';
import { RadialChart } from 'react-vis';
import LegendColor from './LegendColor.jsx';

const COLORS = [
    '#004258',
    '#03A6BB',
    '#1FBA70',
    '#BFDB39',
    '#FEE119'
];

export default class OpinionAnalysisResults extends React.Component {
    render() {
        const r = this.props.results;
        const percent = Math.abs(Math.round(r.verdict * 100)) + "%";

        let color = 'yellow';
        if (r.verdict < -0.25) {
            color = 'red';
        } else if (r.verdict > 0.25) {
            color = 'green';
        }

        const opinionStr = r.verdict < 0 ? 'Negative' : 'Positive';
        const data = [
            { angle: r.opinions.stronglyNegative, label: 'strongly negative' },
            { angle: r.opinions.moderatelyNegative, label: 'moderately negative' },
            { angle: r.opinions.moderatelyPositive, label: 'moderately positive' },
            { angle: r.opinions.stronglyPositive, label: 'strongly positive' }
        ];
        const angleSum = data.reduce((a, b) => a + b.angle, 0);
        console.log(angleSum);
        data.sort((a, b) => a.angle - b.angle);

        for (let i = 0; i < data.length; i++) {
            data[i].color = COLORS[4 - i];
        }

        return (
            <Grid centered>
                <Grid.Row>
                    <Grid.Column width={4}>
                        <Statistic id="opinion-result" size="huge" value={percent} label={opinionStr} color={color} />
                    </Grid.Column>
                    <Grid.Column width={7}>
                        <RadialChart innerRadius={70} angleType="category" colorType="literal" width={300} height={300} data={data} />
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row>
                    <Grid.Column width={16}>
                        {data.map(d => (
                            <span key={d.label}>
                                <LegendColor show color={d.color} />
                                <span className="legend-label">{d.label}</span>
                                <span className="legend-number">{" (" + Math.round(100 * d.angle / angleSum) + "%)"}</span>
                            </span>
                        ))}
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );
    }
}
