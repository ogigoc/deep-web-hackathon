import React from 'react';
import { Header, Menu, Segment } from 'semantic-ui-react';

export default class NavMenu extends React.Component {
    constructor() {
        super();
        this.onItemClick = this.onItemClick.bind(this);
    }

    onItemClick(e, { name }) {
        if (this.props.onChange) {
            this.props.onChange(e, name);
        }
    }

    render() {
        return (
            <Menu id="main-menu" size="large" inverted pointing>
                <Menu.Item><Header inverted as='h1'>EXCADRILL</Header></Menu.Item>
                {this.props.items.map(p =>
                    <Menu.Item key={p.name} name={p.name} active={this.props.activeItem === p.name} onClick={this.onItemClick}>
                        {p.title}
                    </Menu.Item>)}
            </Menu>
        );
    }
}
