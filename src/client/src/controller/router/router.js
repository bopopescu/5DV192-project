import React from "react";
import { Route, Router, Switch } from "react-router-dom";

import PublicRoute from "./public-route";
import history from "../utils/history";


import Home from "../../view/containers/home";
import ErrorNotFound from "../../view/containers/error-not-found";


class CustomRouter extends React.PureComponent {

    render() {

        return (
            <Router history={history}>
                <Switch>

                    <Route exact path="/" component={Home} />

                    <PublicRoute exact path="/convert" component={Home} />

                    <Route component={ErrorNotFound} />

                </Switch>
            </Router>
        );

    }

}

export default CustomRouter;
