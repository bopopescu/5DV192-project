import * as constants from "../constants/user";
import api from "../../api";
import history from '../../utils/history'
import Cookies from "universal-cookie";

export function actionUserRegister(data) {

    return dispatch => {

        dispatch({
            type: constants.USER_REGISTER_REQUEST
        });

        return api.userRegister(data).then(response => {

            if (response.ok) {

                dispatch({
                    type: constants.USER_REGISTER_SUCCESS,
                    payload: response.data
                });

                const cookies = new Cookies();

                cookies.set('session', response.data.sessionKey, { path: '/', expires: new Date(Date.now()+31556926) });

                actionUserGet(response.data.sessionKey);

                history.push("/")

            } else {

                dispatch({
                    type: constants.USER_REGISTER_FAILURE,
                    payload: response.data
                });

            }

        });

    };

}

export function actionUserLogin(data) {

    return dispatch => {

        dispatch({
            type: constants.USER_LOGIN_REQUEST
        });

        return api.userLogin(data).then(response => {

            if (response.ok) {

                dispatch({
                    type: constants.USER_LOGIN_SUCCESS,
                    payload: response.data
                });

                const cookies = new Cookies();

                cookies.set('session', response.data.sessionKey, { path: '/', expires: new Date(Date.now()+31556926) });

                actionUserGet(response.data.sessionKey);

                history.push("/");

            } else {

                dispatch({
                    type: constants.USER_LOGIN_FAILURE,
                    payload: response.data
                });

            }

        });

    };

}

export function actionUserLogout() {

    return dispatch => {

        dispatch({
            type: constants.USER_LOGOUT_REQUEST
        });

        const cookies = new Cookies();
        let cookieSession = cookies.get('session');
        let data = { sessionKey: cookieSession };

        return api.userLogout(data).then(response => {

            if (response.ok) {
                dispatch({
                    type: constants.USER_LOGOUT_SUCCESS,
                    payload: response.data
                });
                history.push("/")
            } else {
                dispatch({
                    type: constants.USER_LOGOUT_FAILURE,
                    payload: response.data
                });
            }

        });

    };

}

export function actionUserGet(key) {

    return dispatch => {

        dispatch({
            type: constants.USER_GET_REQUEST
        });

        return api.userGet(key).then(response => {

            if (response.ok) {

                dispatch({
                    type: constants.USER_GET_SUCCESS,
                    payload: response.data
                });

            } else {

                // invalid session

                return actionUserReset();

            }

        });

    };

}

export function actionUserReset() {

    const cookies = new Cookies();
    cookies.remove('session', { path: '/' });

    return dispatch => {

        dispatch({
            type: constants.USER_RESET
        });

    };

}

export function actionUserSetCoins(coins) {

    return dispatch => {

        dispatch({
            type: constants.USER_SET_COINS_REQUEST
        });

        const cookies = new Cookies();
        let cookieSession = cookies.get('session');
        let data = { sessionKey: cookieSession, coins: coins };

        return api.userSetCoins(data).then(response => {

            if (response.ok) {
                dispatch({
                    type: constants.USER_SET_COINS_SUCCESS,
                    payload: response.data
                });
            } else {
                dispatch({
                    type: constants.USER_SET_COINS_FAILURE,
                    payload: response.data
                });
            }

        });

    };

}

export function actionUserGetUsers() {

    return dispatch => {

        dispatch({
            type: constants.USER_GET_USERS_REQUEST
        });

        return api.userGetUsers().then(response => {

            if (response.ok) {

                dispatch({
                    type: constants.USER_GET_USERS_SUCCESS,
                    payload: response.data
                });

            } else {

                dispatch({
                    type: constants.USER_GET_USERS_FAILURE,
                    payload: response.data
                });

            }

        });

    };

}