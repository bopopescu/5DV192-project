import { combineReducers } from 'redux'
import reducerTranscoder from './transcoder'

export default combineReducers({
    transcoder: reducerTranscoder,
})