import React from 'react';
import { Grid, Dropdown, Header, Segment } from 'semantic-ui-react';
import { SingleDatePicker } from 'react-dates';
import * as moment from 'moment'
import 'react-dates/lib/css/_datepicker.css';

import TrendsTable from './TrendsTable.jsx';

export default class Trends extends React.Component {
    constructor() {
        super();

        this.state = {
            range: 'week',
            datePickerFocused: false,
            word: null
        };

        this.onDateChange = this.onDateChange.bind(this);
        this.onDatePickerFocusChange = this.onDatePickerFocusChange.bind(this);
        this.onRangeChange = this.onRangeChange.bind(this);
        this.onSelectedRowChange = this.onSelectedRowChange.bind(this);
    }

    onDateChange(date) {
        this.setState({ date });
    }

    onDatePickerFocusChange({ focused }) {
        this.setState({ datePickerFocused: focused });
    }

    onRangeChange(_, data) {
        console.log(data);
        this.setState({ range: data.value });
    }

    onSelectedRowChange(word) {
        this.setState({ word });
    }

    render() {
        const { date, timeframe, datePickerFocused } = this.state;
        const mockItems = [{
            word: 'kite',
            change: '+12%'
        }, {
            word: 'jaja',
            change: '+8%'
        }, {
            word: 'humreti',
            change: '+5%'
        }, {
            word: 'bebo',
            change: '+3%'
        }, {
            word: 'kite2',
            change: '+12%'
        }, {
            word: 'jaja2',
            change: '+8%'
        }, {
            word: 'humreti2',
            change: '+5%'
        }, {
            word: 'bebo2',
            change: '+3%'
        }, {
            word: 'aaaa'
        }, {
            word: 'bbbb'
        }, {
            word: 'mock'
        }];

        return (
            <Segment className="widget" raised>
                <Header as="h3">Trends</Header>
                <Grid columns={2}>
                    <Grid.Row>
                        <Grid.Column width={10}>
                            <SingleDatePicker
                                id="opinion-date-picker"
                                date={date}
                                onDateChange={this.onDateChange}
                                focused={datePickerFocused}
                                onFocusChange={this.onDatePickerFocusChange}
                                numberOfMonths={1}
                                placeholder="Pick a date..."
                            />
                        </Grid.Column>
                        <Grid.Column width={6}>
                            <Dropdown
                                id="range-picker"
                                fluid
                                selection
                                options={[{
                                    text: 'Surrounding week',
                                    value: 'week'
                                }, {
                                    text: 'Surrounding month',
                                    value: 'month'
                                }, {
                                    text: 'Surrounding year',
                                    value: 'year'
                                }]}
                                defaultValue='month'
                            />
                        </Grid.Column>
                    </Grid.Row>
                    <Grid.Row>
                        <Grid.Column width={7}>
                            <TrendsTable
                                onChange={this.onSelectedRowChange}
                                selectedRow={this.state.word}
                                items={mockItems} />
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Segment>
        );
    }
}
