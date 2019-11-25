import * as constants from "../constants/user";
import { validatePayload } from "./validate.js";

const initialState = {
    payload: null,
    errors: null,
    success: null,
    isAuthenticated: null
};

export default function(state = initialState, action) {

    let errors = validatePayload(action.payload);

    switch (action.type) {

            // register

        case constants.USER_REGISTER_REQUEST:
            return {
                ...state,
                isFetched: false,
                success: null,
            };
        case constants.USER_REGISTER_SUCCESS:
            return {
                ...state,
                isFetched: true,
                errors: null,
                success: true,
                isAuthenticated: true
            };
        case constants.USER_REGISTER_FAILURE:
            return {
                ...state,
                isFetched: true,
                errors: errors,
                success: false,
                isAuthenticated: false,
            };

            // login

        case constants.USER_LOGIN_REQUEST:
            return {
                ...state,
                isFetched: false,
                success: null,
            };
        case constants.USER_LOGIN_SUCCESS:
            return {
                ...state,
                isFetched: true,
                errors: null,
                success: true,
                isAuthenticated: true
            };
        case constants.USER_LOGIN_FAILURE:
            return {
                ...state,
                isFetched: true,
                errors: errors,
                success: false,
                isAuthenticated: false,
            };

            // logout

        case constants.USER_LOGOUT_REQUEST:
            return {
                ...state,
                isFetched: false,
                success: null,
            };
        case constants.USER_LOGOUT_SUCCESS:
            return initialState;
        case constants.USER_LOGOUT_FAILURE:
            return {
                ...state,
                isFetched: true,
                errors: errors,
                success: false,
            };

            // logout

        case constants.USER_GET_REQUEST:
            return {
                ...state,
                isFetched: false,
                errors: null,
                success: null,
            };
        case constants.USER_GET_SUCCESS:
            return {
                ...state,
                account: action.payload,
                isFetched: true,
                errors: null,
                success: true,
                isAuthenticated: true
            };
        case constants.USER_GET_FAILURE:
            return {
                ...state,
                isFetched: true,
                errors: action.payload,
                success: false,
            };

            // set coins

        case constants.USER_SET_COINS_REQUEST:
            return {
                ...state,
                isFetched: false,
                errors: null,
                success: null,
            };
        case constants.USER_SET_COINS_SUCCESS:
            return {
                ...state,
                isFetched: true,
                errors: null,
                success: true,
            };
        case constants.USER_SET_COINS_FAILURE:
            return {
                ...state,
                isFetched: true,
                errors: action.payload,
                success: false,
            };

            // reset

        case constants.USER_RESET:
            return initialState;

        default:
            return state;
    }

}
