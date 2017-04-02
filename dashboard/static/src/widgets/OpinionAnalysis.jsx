import React from 'react';
import { Loader, Dimmer, Button, Input, Form, Grid, Dropdown, Header, Segment } from 'semantic-ui-react';
import { getOpinion } from '../api/Api.js';

import OpinionAnalysisResults from './OpinionAnalysisResults.jsx';

export default class OpinionAnalysis extends React.Component {
    constructor() {
        super();
        this.state = {
            loading: false,
            queryResults: null,
            query: ""
        };
        this.onQuery = this.onQuery.bind(this);
        this.onChangeQuery = this.onChangeQuery.bind(this);
    }

    fetchOpinion() {
        this.setState({
            loading: true
        });

        getOpinion(this.state.query)
            .then(response => {
                const result = {
                    verdict: response[0].opinions.length ? ((response[0].opinions.reduce((a, b) => a + b)) / response[0].opinions.length) : null,
                    opinions: {
                        stronglyNegative: response[0].opinions.filter(o => o < -0.5).length,
                        moderatelyNegative: response[0].opinions.filter(o => o >= -0.5 && o < 0.0).length,
                        moderatelyPositive: response[0].opinions.filter(o => o >= 0.0 && o < 0.5).length,
                        stronglyPositive: response[0].opinions.filter(o => o >= 0.5).length
                    }
                };

                this.setState({
                    loading: false,
                    queryResults: result
                });
            });
    }
    onChangeQuery(_, { value }) {
        this.setState({
            query: value
        });
    }

    onQuery(e, data) {
        this.fetchOpinion();

        e.preventDefault();
        return false;
    }

    render() {
        return (
            <Segment className="widget" raised>
                <Header as="h3">Opinion Analysis</Header>
                <Form onSubmit={this.onQuery}>
                    <Form.Group widths={16}>
                        <Form.Field width={16} onChange={this.onChangeQuery} control={Input} placeholder="Enter a term..." />
                        <Form.Field control={Button} color="teal">Query</Form.Field>
                    </Form.Group>
                </Form>
                {this.state.queryResults ? <OpinionAnalysisResults results={this.state.queryResults} /> : null}
                <Dimmer inverted active={this.state.loading}>
                    {this.state.loading ? <Loader /> : null}
                </Dimmer>
            </Segment>
        );
    }
}
