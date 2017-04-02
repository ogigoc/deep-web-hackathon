import React from 'react';
import { Header, Grid } from 'semantic-ui-react';

import Pages from '../discovery/Pages.jsx';
import SearchSubmit from '../discovery/SearchSubmit.jsx';
import TextBlockView from '../discovery/TextBlockView.jsx';
import { getTextBlocks, getPages } from '../api/Api.js';


export default class Discovery extends React.Component {
    constructor() {
        super();
        this.state = {
            pages: []
        };

        this.onRowSelect = this.onRowSelect.bind(this);
    }

    fetchPages() {
        getPages(20).then(resp => this.setState({ pages: resp }));
    }

    fetchTextBlocks(pageUrl) {
        getTextBlocks(pageUrl).then(resp => this.setState({ textBlocks: resp.filter(resp => resp.text.length > 50).slice(0, 6) }));
    }

    componentWillMount() {
        this.fetchPages();
        setInterval(() => this.fetchPages(), 1000);
    }

    onRowSelect(pageUrl) {
        this.setState({
            selectedRow: pageUrl
        });
        this.fetchTextBlocks(pageUrl);
    }

    render() {
        const { selectedRow, textBlocks, pages } = this.state;

        return (
            <div className={this.props.className}>
                <Grid>
                    <Grid.Row>
                        <Grid.Column width={11}>
                            <Pages onRowSelect={this.onRowSelect} selectedRow={selectedRow} pages={pages} />
                        </Grid.Column>
                        <Grid.Column width={5}>
                            <SearchSubmit />
                            {textBlocks ? <TextBlockView textBlocks={textBlocks} /> : <Header as='h5'>Odaberite stranicu kako biste videli detalje.</Header>}
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </div>
        );
    }
}
