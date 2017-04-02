import React from 'react';
import { Button, Input, Dimmer, Loader, Form, Message, Header, Segment } from 'semantic-ui-react';

import { postSearch } from '../api/Api.js';

export default class SearchSubmit extends React.Component {
    constructor() {
        super();
        this.state = {
            loading: false,
            messageQuery: null,
            query: ''
        };

        this.onQuery = this.onQuery.bind(this);
        this.onChangeQuery = this.onChangeQuery.bind(this);
    }

    postSearch(query) {
        this.setState({
            loading: true,
            messageQuery: null
        });

        postSearch(query)
            .then(resp => {
                this.setState({
                    loading: false,
                    messageQuery: query
                });

                setTimeout(() => this.setState({
                    messageQuery: null
                }), 10000);
            });
    }

    onQuery(e) {
        this.postSearch(this.state.query);

        e.preventDefault();
        return false;
    }

    onChangeQuery(_, { value }) {
        this.setState({
            query: value
        });
    }

    render() {
        const { loading, messageQuery } = this.state;

        return (
            <Segment raised>
                <Header as='h3'>Start a Search</Header>
                {messageQuery ?
                    <Message
                        success
                        header="Your search was queued!"
                        content="You should start seeing the pages crawled soon." />
                    : null}
                <Form onSubmit={this.onQuery}>
                    <Form.Group widths={16}>
                        <Form.Field width={16} onChange={this.onChangeQuery} control={Input} placeholder="Enter your search query..." />
                        <Form.Field control={Button} primary>Enqueue</Form.Field>
                    </Form.Group>
                </Form>
                <Dimmer inverted active={loading}>
                    {this.state.loading ? <Loader>Enqueuing, this might take a while...</Loader> : null}
                </Dimmer>
            </Segment>
        );
    }
}
