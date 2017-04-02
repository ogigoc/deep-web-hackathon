import React from 'react';
import { Header, Segment } from 'semantic-ui-react';

export default class OpinionAnalysis extends React.Component {
    render() {
        return (
            <Segment className="widget" raised>
                <Header as='h3'>Opinion Analysis</Header>
            </Segment>
        );
    }
}
