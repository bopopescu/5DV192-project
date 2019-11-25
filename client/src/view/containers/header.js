import { connect } from 'react-redux'
import Header from '../components/header'
import * as userActions from "../../controller/redux/actions/user";

const mapStateToProps = state => ({
    user: state.reducerUser
});

const mapDispatchToProps = {
    actionUserGet: userActions.actionUserGet,
    actionUserReset: userActions.actionUserReset,
};

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Header)
