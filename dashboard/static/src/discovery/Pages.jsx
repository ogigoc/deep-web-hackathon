import React from 'react';
import { Table } from 'semantic-ui-react';
import * as moment from 'moment';

function truncate(text, len) {
    if (text.length > len) {
        return text.substring(0, len) + "...";
    } else {
        return text;
    }
}

export default class Pages extends React.Component {
    constructor() {
        super();
        this.onClick = this.onClick.bind(this);
    }

    onClick(pageUrl) {
        if (this.props.onRowSelect) {
            this.props.onRowSelect(pageUrl);
        }
    }

    render() {
        const { pages } = this.props;

        return (
            <Table celled striped>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell width={3}>Time</Table.HeaderCell>
                        <Table.HeaderCell width={7}>URL</Table.HeaderCell>
                        <Table.HeaderCell width={6}>Title</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {pages.map(page => (
                        <Table.Row onClick={() => this.onClick(page.url)} active={page.url === this.props.selectedRow} key={page.url}>
                            <Table.Cell width={3}>{moment.utc(page.timestamp * 1000).format("YYYY/MM/DD HH:mm:ss")}</Table.Cell> <Table.Cell width={7}>{truncate(page.url, 70)}</Table.Cell>
                            <Table.Cell width={6}>{page.title}</Table.Cell>
                        </Table.Row>
                    ))}
                </Table.Body>
            </Table>
        );
    }
}
