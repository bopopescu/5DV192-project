import { createStore, compose, applyMiddleware } from 'redux'
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import thunkMiddleware from 'redux-thunk'
import rootReducer from './reducers/index'
import Reactotron from '../utils/reactotron'

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const persistConfig = {
    key: 'root',
    storage
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

const store = createStore(
    persistedReducer,
    composeEnhancers(
        applyMiddleware(thunkMiddleware),
        Reactotron.createEnhancer()
    )
);

export const persistor = persistStore(store);
export default store
