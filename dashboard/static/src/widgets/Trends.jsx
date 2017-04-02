import React from 'react';
import { Grid, Dropdown, Header, Segment } from 'semantic-ui-react';
import { SingleDatePicker } from 'react-dates';
import * as moment from 'moment'
import 'react-dates/lib/css/_datepicker.css';

import TrendsTable from './TrendsTable.jsx';
import TrendsChart from './TrendsChart.jsx';

export default class Trends extends React.Component {
    constructor() {
        super();

        const mockItems = [{
            word: 'kite',
            enabled: true,
            change: '+12%'
        }, {
            word: 'jaja',
            enabled: true,
            change: '+8%'
        }, {
            word: 'humreti',
            enabled: true,
            change: '+5%'
        }, {
            word: 'bebo',
            enabled: true,
            change: '+3%'
        }, {
            word: 'kite2',
            enabled: true,
            change: '+12%'
        }, {
            word: 'jaja2',
            enabled: true,
            change: '+8%'
        }, {
            word: 'humreti2',
            enabled: true,
            change: '+5%'
        }, {
            word: 'bebo2',
            enabled: true,
            change: '+3%'
        }, {
            enabled: true,
            word: 'aaaa'
        }, {
            enabled: true,
            word: 'bbbb'
        }, {
            enabled: true,
            word: 'mock'
        }];

        this.state = {
            range: 'week',
            datePickerFocused: false,
            items: mockItems
        };

        this.onDateChange = this.onDateChange.bind(this);
        this.onDatePickerFocusChange = this.onDatePickerFocusChange.bind(this);
        this.onRangeChange = this.onRangeChange.bind(this);
        this.onSelectedRowChange = this.onSelectedRowChange.bind(this);
        this.onWordEnabledChange = this.onWordEnabledChange.bind(this);
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

    onWordEnabledChange(word, enabled) {
        console.log(this, word, enabled);
        this.setState({
            items: this.state.items.map(w => {
                if (w.word === word)
                    w.enabled = enabled;

                return { word: w.word, enabled: w.enabled };
            })
        });
    }

    render() {
        const { items, date, timeframe, datePickerFocused } = this.state;

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
                                onRowEnabledChange={this.onWordEnabledChange}
                                items={items} />
                        </Grid.Column>
                        <Grid.Column width={9}>
                            <TrendsChart
                                dates={[
                                    "01.04.2017",
                                    "30.10.2016",
                                    "30.12.2016",
                                    "30.12.2016",
                                    "30.11.2016"
                                ]}
                            />
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Segment>
            );
            }
            }
