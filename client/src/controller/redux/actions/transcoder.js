import * as constants from "../constants/transcoder";
import api from "../../api";
import history from '../../utils/history'
import Cookies from "universal-cookie";

export function actionTranscoderSend(data) {

    return dispatch => {

        dispatch({
            type: constants.TRANSCODE_SEND_REQUEST
        });

        return api.transcodeSend(data).then(response => {

            if (response.ok) {

                dispatch({
                    type: constants.TRANSCODE_SEND_SUCCESS,
                    payload: response.data
                });


            } else {

                dispatch({
                    type: constants.TRANSCODE_SEND_FAILURE,
                    payload: response.data
                });

            }

        });

    };

}
