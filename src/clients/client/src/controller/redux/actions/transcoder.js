import * as constants from "../constants/transcoder";
import api from "../../api";

const debug = false;

export function actionTranscoderSend(data) {

    for (let pair of data.entries()) {
        console.log(pair[0] + ', ' + pair[1]);
    }

    let port;
    if(debug) {
        port = "5001";
    } else {
        port = "5000";
    }

    return dispatch => {

        dispatch({
            type: constants.TRANSCODE_SEND_REQUEST
        });

        // transcode request

        return api.transcodeRequest(null).then(response => {

            if (response.ok) {

                console.log(response.data.ip);
                data.url = "http://" + response.data.ip  + ":" + port;

                // transcode upload

                return api.transcodeUpload(data).then(response2 => {

                    if (response2.ok) {

                        console.log(response2.data);

                        return api.transcodeRetrieve(response2.data).then(response3 => {

                            if (response3.ok) {

                                console.log(response3.data)

                                dispatch({
                                    type: constants.TRANSCODE_SEND_SUCCESS,
                                    payload: response3.data
                                });

                            } else {

                                dispatch({
                                    type: constants.TRANSCODE_SEND_FAILURE,
                                    payload: response.data
                                });

                            }

                        });

                    } else {

                        dispatch({
                            type: constants.TRANSCODE_SEND_FAILURE,
                            payload: response.data
                        });

                    }

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

export function actionTranscoderReset() {

    return dispatch => {

        dispatch({
            type: constants.TRANSCODE_RESET
        });

    };

}
