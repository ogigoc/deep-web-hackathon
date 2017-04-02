import React from 'react';
import { Header, Segment } from 'semantic-ui-react';

export default class Trends extends React.Component {
    render() {
        return (
            <Segment className="widget" raised>
                <Header as='h3'>Trends</Header>
            </Segment>
        );
    }
}
