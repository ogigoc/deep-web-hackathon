import React from 'react';
import NavMenu from './NavMenu.jsx'
import Analytics from './Analytics.jsx'
import Discovery from './Discovery.jsx'
require('./sass/index.scss');

export default class Root extends React.Component {
    constructor() {
        super();
        this.state = {
            activeItem: 'analytics'
        };

        this.onActiveItemChange = this.onActiveItemChange.bind(this);
    }

    onActiveItemChange(e, newItemName) {
        this.setState({
            activeItem: newItemName
        });
    }
    render() {
        const { activeItem } = this.state;
        const items = [
            {
                name: 'analytics',
                title: 'Analytics'
            },
            {
                name: 'discovery',
                title: 'Discovery'
            }
        ];

        console.log(activeItem === 'analytics' ? '' : 'hidden');
        return (
            <div id="page">
                <NavMenu activeItem={activeItem} onChange={this.onActiveItemChange} items={items} />
                <Analytics className={activeItem === 'analytics' ? '' : 'hidden'} />
                <Discovery className={activeItem === 'discovery' ? '' : 'hidden'} />
            </div>
        );
    }
}
