import React from 'react';
import { Route } from 'react-router-dom';
import store from '../redux/store'

const PublicRoute = ({component: Component, ...rest}) => {

    return (
        <Route {...rest} render={(props) => <Component {...props} />} />
    )

};

export default PublicRoute;