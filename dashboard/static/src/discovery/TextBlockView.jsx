import React from 'react';
import { Header, Table } from 'semantic-ui-react';
import * as Moment from 'moment';
import { extendMoment } from 'moment-range';

const moment = extendMoment(Moment)

function truncate(text, len) {
    if (text.length > len) {
        return text.substring(0, len) + "...";
    } else {
        return text;
    }
}


function myrand(x) {
    return('0.'+Math.sin(x).toString().substr(6));
}

function sanitize_date(date) {
    const ts = date * 1000;
    date = moment.utc(date * 1000);
    const start = new Date(2011, 1, 1),
          end = new Date(2017, 4, 1),
          range = moment.range(start, end);

      if (range.contains(date)) {
          return date.format("YYYY/MM/DD");
      } else {
          let ts1 = start.getTime();
          let ts2 = end.getTime();
          let x = moment.utc(Math.floor(myrand(ts) * (ts2 - ts1)) + ts1).format("YYYY/MM/DD");

          return x;
      }
}

export default class TextBlockView extends React.Component {
    render() {
        const { selectedRow, textBlocks } = this.props;

        return (
            <div>
                <Header id="hdr" as='h3'>Text View</Header>
                <Table celled striped>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell width={2}>Time</Table.HeaderCell>
                            <Table.HeaderCell width={14}>Text</Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {textBlocks.length > 0 ? textBlocks.map(textBlock => (
                            <Table.Row key={textBlock.sha1}>
                                <Table.Cell>{sanitize_date(textBlock.time)}</Table.Cell>
                                <Table.Cell>{truncate(textBlock.text, 300)}</Table.Cell>
                            </Table.Row>
                        )) : <Table.Row><Table.Cell></Table.Cell><Table.Cell>No data to show.</Table.Cell></Table.Row>}
                    </Table.Body>
                </Table>
            </div>
        );
    }
}
