import React from 'react';
import NavMenu from './NavMenu.jsx'
import Analytics from '../pages/Analytics.jsx'
import Discovery from '../pages/Discovery.jsx'
require('../sass/index.scss');

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
                <div id="content">
                    <Analytics className={activeItem === 'analytics' ? '' : 'hidden'} />
                    <Discovery className={activeItem === 'discovery' ? '' : 'hidden'} />
                </div>
            </div>
        );
    }
}
