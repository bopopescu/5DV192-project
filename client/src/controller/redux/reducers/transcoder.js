import * as constants from "../constants/transcoder";

const initialState = {
    payload: null,
    errors: null,
    success: null
};

export default function(state = initialState, action) {

    switch (action.type) {

        case constants.TRANSCODE_SEND_REQUEST:
            return {
                ...state,
                isFetched: false,
                success: null,
            };
        case constants.TRANSCODE_SEND_SUCCESS:
            return {
                ...state,
                isFetched: true,
                payload: action.payload,
                errors: null,
                success: true,
            };
        case constants.TRANSCODE_SEND_FAILURE:
            return {
                ...state,
                isFetched: true,
                errors: action.payload,
                success: false,
            };


        default:
            return state;

    }

}
