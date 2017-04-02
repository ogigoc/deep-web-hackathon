import React from 'react';
import { Grid, Dropdown, Header, Segment } from 'semantic-ui-react';
import { SingleDatePicker } from 'react-dates';
import * as moment from 'moment'
import 'react-dates/lib/css/_datepicker.css';

export default class OpinionAnalysis extends React.Component {
    render() {
        return (
            <Segment className="widget" raised>
                <Header as="h3">Opinion Analysis</Header>
            </Segment>
        );
    }
}
