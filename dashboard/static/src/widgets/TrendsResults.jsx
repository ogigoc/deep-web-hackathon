import React from 'react';
import { Grid } from 'semantic-ui-react';
import TrendsChart from './TrendsChart.jsx';
import TrendsTable from './TrendsTable.jsx';

export default class TrendsResults extends React.Component {
    render() {
        const { dates, items, children } = this.props;

        return (
            <Grid.Row>
                <Grid.Column width={7}>
                    <TrendsTable
                        onRowEnabledChange={this.props.onRowEnabledChange}
                        items={items}
                    />
                </Grid.Column>
                <Grid.Column width={9}>
                    <TrendsChart data={dates} />
                </Grid.Column>
                {children}
            </Grid.Row>
        );
    }
}
