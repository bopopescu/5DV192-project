import { connect } from 'react-redux'
import Home from '../components/home'
import * as transcoderActions from "../../controller/redux/actions/transcoder";

const mapStateToProps = state => ({
    transcoder: state.transcoder
});

const mapDispatchToProps = {
    actionTranscoderSend: transcoderActions.actionTranscoderSend,
    actionTranscoderReset: transcoderActions.actionTranscoderReset,
};

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Home)
