import React from 'react';
import { Icon, Checkbox, Table } from 'semantic-ui-react';

export default class TrendsTable extends React.Component {
    onEnabledChange(word, checked) {
        if (this.props.onRowEnabledChange) {
            this.props.onRowEnabledChange(word, checked);
        }
    }

    render() {
        const { selectedRow, items } = this.props;

        return (
            <Table className="trends" selectable striped>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell width={1}><Icon name="eye" /></Table.HeaderCell>
                        <Table.HeaderCell width={15}>Top terms</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {items.map(item =>
                        (<Table.Row active={selectedRow === item.word} key={item.word} >
                            <Table.Cell><Checkbox onChange={(_, { checked }) => this.onEnabledChange(item.word, checked)} checked={item.enabled} /></Table.Cell>
                            <Table.Cell><span className="top-word">{item.word}</span></Table.Cell>
                        </Table.Row>))}
                </Table.Body>
            </Table>
        );
    }


}
