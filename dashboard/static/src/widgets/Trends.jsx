import React from 'react';
import { Dimmer, Loader, Grid, Dropdown, Header, Segment } from 'semantic-ui-react';
import { SingleDatePicker } from 'react-dates';
import * as moment from 'moment'
import 'react-dates/lib/css/_datepicker.css';

import TrendsResults from './TrendsResults.jsx';

import { getTrends } from '../api/Api.js';

const COLORS = [
    "#db2828",
    "#f2711c",
    "#fbbd08",
    "#b5cc18",
    "#21ba45",
    "#00b5ad",
    "#2185d0",
    "#6435c9"
];

export default class Trends extends React.Component {
    constructor() {
        super();

        this.state = {
            range: 'week',
            date: moment.default(),
            datePickerFocused: false,
            loading: true,
            items: [],
            dates: []
        };

        this.onDateChange = this.onDateChange.bind(this);
        this.onDatePickerFocusChange = this.onDatePickerFocusChange.bind(this);
        this.onRangeChange = this.onRangeChange.bind(this);
        this.onWordEnabledChange = this.onWordEnabledChange.bind(this);
    }

    fetchTrends(date, range) {
        this.setState({
            loading: true
        });

        if (!date) {
            date = this.state.date;
        }

        if (!range) {
            range = this.state.range;
        }

        getTrends(date.toDate(), range, 11) .then(resp => {
            const items = resp.map((i, idx) => ({
                word: i.word,
                color: COLORS[idx % COLORS.length],
                enabled: true,
                dates: i.dates.map(d => new Date(d * 1000))
            }));

            this.setState({
                loading: false,
                items,
                dates: this.refilterDates(items)
            });
        });
    }

    refilterDates(words) {
        return words
            .filter(w => w.enabled)
            .map(w => ({
                dates: w.dates,
                color: w.color
            }));
    }

    onDateChange(date) {
        this.setState({ date });
        this.fetchTrends(date);
    }

    onDatePickerFocusChange({ focused }) {
        this.setState({ datePickerFocused: focused });
    }

    onRangeChange(_, data) {
        this.setState({ range: data.value });
        this.fetchTrends(undefined, data.value);
    }

    onWordEnabledChange(word, enabled) {
        const items = this.state.items.map(w => {
            if (w.word === word)
                return { ...w, enabled };
            else
                return { ...w };
        });

        this.setState({
            items,
            dates: this.refilterDates(items)
        });
    }

    componentWillMount() {
        this.fetchTrends();
    }

    render() {
        const { loading, items, date, dates, timeframe, datePickerFocused } = this.state;

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
                                isOutsideRange={() => false}
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
                                onChange={this.onRangeChange}
                                defaultValue='month'
                            />
                        </Grid.Column>
                    </Grid.Row>
                    {loading ?
                        <Dimmer inverted active>
                            <Loader />
                        </Dimmer> : null}
                    <TrendsResults
                        dates={dates}
                        items={items}
                        onRowEnabledChange={this.onWordEnabledChange}
                    />
                </Grid>
            </Segment>
        );
    }
}
