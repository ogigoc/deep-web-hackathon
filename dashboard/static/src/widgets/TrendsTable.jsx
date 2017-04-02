import React from 'react';
import { Table } from 'semantic-ui-react';

export default class TrendsTable extends React.Component {
    onItemClick(newWord) {
        if (this.props.onChange) {
            this.props.onChange(newWord);
        }
    }

    render() {
        const { selectedRow, items } = this.props;

        return (
            <Table className="trends" selectable striped>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Top terms</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {items.map(item =>
                        (<Table.Row onClick={() => this.onItemClick(item.word)} active={selectedRow === item.word} key={item.word} >
                            <Table.Cell><span className="top-word">{item.word}</span></Table.Cell>
                        </Table.Row>))}
                </Table.Body>
            </Table>
        );
    }


}
