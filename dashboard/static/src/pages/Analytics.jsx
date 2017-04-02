import React from 'react';
import { Grid } from 'semantic-ui-react';
import GeoSentiment from '../widgets/GeoSentiment.jsx'
import OpinionAnalysis from '../widgets/OpinionAnalysis.jsx'
import Trends from '../widgets/Trends.jsx'

export default class Analytics extends React.Component {
    render() {
        return (
            <div className={this.props.className}>
                <Grid columns={2}>
                    <Grid.Row>
                        <Grid.Column width={8}>
                            <GeoSentiment />
                            <OpinionAnalysis />
                        </Grid.Column>
                        <Grid.Column width={8}>
                            <Trends />
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </div>
        );
    }
}
