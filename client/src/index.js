import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { PersistGate } from 'redux-persist/integration/react'
import Router from './controller/router/router'

import store, { persistor } from './controller/redux/store'

import './controller/utils/reactotron'


render(
    <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
            <Router />
        </PersistGate>
    </Provider>,
    document.getElementById('root')
);
